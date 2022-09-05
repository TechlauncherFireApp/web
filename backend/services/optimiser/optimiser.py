import minizinc
from sqlalchemy import orm

from domain import session_scope, AssetRequestVehicle, AssetRequestVolunteer
from repository.asset_request_volunteer_repository import add_shift
from services.optimiser.calculator import Calculator


class Optimiser:
    # The calculator generates data structures for the optimiser to solve. Separating these two concerns improves
    # readability of the code dramatically.
    calculator = None

    def __init__(self, session: orm.session, request_id: int, debug: bool):
        """
        @param session: The SQLAlchemy session to use.
        @param request_id: The request ID to solve.
        @param debug: If this should be executed in debug (printing) mode.
        """
        self.calculator = Calculator(session, request_id)
        self.debug = debug

    @staticmethod
    def generate_model_string():
        """
        Generate a the model string, factored out into a separete function only to increase readability.
        @return:
        """
        model_str = """
        
        % Simple Parameters
        int: A; 
        set of int: ASSETSHIFT = 1..A;

        int: R;
        set of int: ROLE = 1..R;

        int: P;
        set of int: POSITION = 1..P;

        int: V;
        set of int: VOLUNTEER = 1..V;

        int: Q;
        set of int: QUALIFICATION = 1..Q;

        % Supervisor Customisation
        array[ASSETSHIFT, POSITION, QUALIFICATION] of bool: qualrequirements;
        array[ASSETSHIFT, POSITION, ROLE] of bool: rolerequirements;
        array[POSITION, ASSETSHIFT] of bool: posrequirements;

        % Volunteer Abilities
        array[VOLUNTEER, QUALIFICATION] of bool: qualability;
        array[VOLUNTEER, ROLE] of bool: roleability;

        % Volunteer Availabilities
        array[VOLUNTEER, ASSETSHIFT] of bool: availability;
        array[ASSETSHIFT, ASSETSHIFT] of bool: clashes;

        % Decision Variable
        array[ASSETSHIFT, VOLUNTEER, POSITION] of var bool: assignment;


        % Constraints
        % The number of positions assigned should not exceed the number of positions needed for a shift.
        constraint forall(a in ASSETSHIFT)(
            sum(p in POSITION)(posrequirements[p, a]) >= sum(p in POSITION, v in VOLUNTEER)(bool2int(assignment[a, v, p]))
        );

        % A volunteer should be assigned to at most one position per shift.
        constraint forall(a in ASSETSHIFT, v in VOLUNTEER)(
            sum(p in POSITION)(bool2int(assignment[a, v, p])) <= 1
        );

        % A position should only be assigned to at most once for all shifts.
        constraint forall(p in POSITION)(
            sum(a in ASSETSHIFT, v in VOLUNTEER)(assignment[a, v, p]) <= 1
        );

        % If a volunteer either does not have the qualification or role for a position, then they should not be assigned to a shift.
        constraint forall(a in ASSETSHIFT, p in POSITION, v in VOLUNTEER, r in ROLE, q in QUALIFICATION where ((qualrequirements[a, p, q] == true /\ qualability[v, q] == false) \/ (rolerequirements[a, p, r] == true /\ roleability[v, r] == false)))(
            bool2int(assignment[a, v, p]) == 0
        );

        % If a volutneer is not available for a shift, they should not be assigned in the shift.
        constraint forall(v in VOLUNTEER, a in ASSETSHIFT where availability[v, a] == 0)(
            sum(p in POSITION)(assignment[a, v, p]) == 0 
        );

        % If a shift clashes with another shift, then the volunteer should not be assigned to both shifts.
        constraint forall(aone in ASSETSHIFT, v in VOLUNTEER)(
            forall(atwo in ASSETSHIFT where clashes[aone, atwo] == true)(
                not(sum(p in POSITION)(assignment[aone, v, p]) == true /\ sum(p in POSITION)(assignment[atwo, v, p]) == true)
            )
        );

        % Volunteers should only be assigned to a position that is needed for the shift. i.e. there should not be any positions assigned for a shift if it hasn't been 
        % intended by the supervisor through customisation.
        constraint forall(a in ASSETSHIFT, v in VOLUNTEER, p in POSITION)(
            not(assignment[a, v, p] == true /\ posrequirements[p, a] == false)
        );

        % Objective
        solve maximize sum(a in ASSETSHIFT, v in VOLUNTEER, p in POSITION)(assignment[a,v,p]);

        %~~~~~~~~~~~~~~~~~~~
        % OUTPUT
        output [ "Assignment: \n"] ++
                ["Asset Shift = " ++ show(a) ++ "\n"
                ++
                concat([ if show(assignment[a,v,p]) == "true"
                then "\tVolunteer = " ++ show(v) ++ ", \tPosition = " ++ show(p) ++ "\n"
                 endif
                | v in VOLUNTEER, p in POSITION])
                | a in ASSETSHIFT]
        """
        return model_str

    def solve(self):
        # Instantiate the model
        gecode = minizinc.Solver.lookup("coin-bc")
        model = minizinc.Model()
        model.add_string(Optimiser.generate_model_string())
        instance = minizinc.Instance(gecode, model)

        if self.debug:
            print(f"'A' = {self.calculator.get_number_of_vehicles()}")
            print(f"'C' = {self.calculator.get_number_of_vehicles()}")
            print(f"'R' = {self.calculator.get_number_of_volunteers()}")
            print(f"'S' = {self.calculator.get_number_of_roles()}")
            print(f"'clashing' = {self.calculator.calculate_clashes()}")
            print(f"'sreq' = {self.calculator.calculate_skill_requirement()}")
            print(f"'compatible' = {self.calculator.calculate_compatibility()}")
            print(f"'mastery' = {self.calculator.calculate_mastery()}")
            print(f'==========')
            print(f'roles= {[x.code for x in self.calculator.get_roles()]}')
            print(f'==========')

        # Add the model parameters
        instance["A"] = self.calculator.get_number_of_vehicles()
        instance["C"] = self.calculator.get_number_of_vehicles()
        instance["R"] = self.calculator.get_number_of_volunteers()
        instance["S"] = self.calculator.get_number_of_roles()
        instance["clashing"] = self.calculator.calculate_clashes()
        instance["sreq"] = self.calculator.calculate_skill_requirement()
        instance['compatible'] = self.calculator.calculate_compatibility()
        instance['mastery'] = self.calculator.calculate_mastery()

        return instance.solve()

    def save_result(self, session, result) -> None:
        """
        Save a model result to the database.
        @param session: SQL Alchemy session to use
        @param result: The model result
        """
        # Simple data structure to help find whats missing and whats populated from the decision variable
        persist = []
        for x in self.calculator.get_asset_requests():
            roles = {}
            for role in self.calculator.get_roles():
                roles[role.id] = {'count': self.calculator.get_role_count(x.asset_type.id, role.id), 'assigned': []}
            persist.append(roles)

        # Iterate over the results, adding them to our persistence data structure
        if result is not None:
            for asset_request_index, asset_request in enumerate(result['contrib']):
                for volunteer_index, volunteer in enumerate(asset_request):
                    for role_index, assigned in enumerate(volunteer):
                        if assigned:
                            role_domain = self.calculator.get_role_by_index(role_index)
                            user_domain = self.calculator.get_volunteer_by_index(volunteer_index)
                            asset_request_domain = self.calculator.get_asset_request_by_index(asset_request_index)
                            print(
                                f'Volunteer {user_domain.email} should be assigned to role {role_domain.code} on asset request {asset_request_domain.id}')
                            asset_request_obj = persist[asset_request_index]
                            role_map = asset_request_obj[role_domain.id]
                            role_map['assigned'].append(user_domain.id)

        # Now, actually persist it!
        for asset_request_index, _ in enumerate(persist):
            asset_request = self.calculator.get_asset_request_by_index(asset_request_index)
            asset_request_roles = persist[asset_request_index]
            for role_id in asset_request_roles:
                for assign_count in range(asset_request_roles[role_id]['count']):
                    if assign_count < len(asset_request_roles[role_id]['assigned']):
                        ar = AssetRequestVolunteer(user_id=asset_request_roles[role_id]['assigned'][assign_count],
                                                   vehicle_id=asset_request.id, role_id=role_id, status='pending')
                    else:
                        ar = AssetRequestVolunteer(user_id=None, vehicle_id=asset_request.id, role_id=role_id)
                    session.add(ar)
