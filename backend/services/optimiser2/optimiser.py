import minizinc
from sqlalchemy import orm

from domain import session_scope
from repository.asset_request_volunteer_repository import add_shift
from services.optimiser2.calculator import Calculator


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

    def generate_model_string(self, full: bool):
        """
        Generate a minizinc model from the requirements of asset types, roles and seats in the database.
        Sorry if its hard to follow, its just an outcome of generating a static model from dynamic requirements!
        @param full: If this is a full satisfaction or partial.
        @return:
        """
        model_str = "int: V;\nint: S;\nset of int: volunteers = 1..V;\nset of int: Shifts = 1..S;\n"
        model_str += "array[Shifts,volunteers] of bool: compatible;\n"
        model_str += "array[Shifts,Shifts] of bool: clashing;\n"
        model_str += "array[Shifts,volunteers] of var bool: assignments;\n"
        model_str += "array[volunteers] of int: preferredHours;\n"
        model_str += "array[Shifts] of int: shiftLength;\n\n"

        # We add one of these strings per asset to be scheduled; 'array[Shifts] of bool: isHeavy;'
        for asset_type in self.calculator.get_asset_types():
            model_str += f'array[Shifts] of bool: is{asset_type.code};\n'
        model_str += '\n'

        # We add one of these strings per role to be scheduled; 'array[volunteers] of bool: is<RoleCode>;'
        for role in self.calculator.get_roles():
            model_str += f'array[volunteers] of bool: is{role.code};\n'
        model_str += '\n'

        # We add one of these strings for up to the maximum number of required seats:
        #       'array[Shifts] of var volunteers: seat1;'
        for i in range(1, self.calculator.get_maximum_number_of_seats() + 1):
            model_str += f'array[Shifts] of var volunteers: seat{i};\n'
        model_str += '\n'

        # More constant strings
        model_str += "array[volunteers,Shifts] of var int: hoursOnAssignment;\n"
        model_str += "array[volunteers] of var int: totalHours;\n\n"
        model_str += "%volunteer availability check\n"
        model_str += "constraint forall(s in Shifts)(forall(v in volunteers)(if compatible[s,v] == false then assignments[s,v] == false endif));\n\n"
        model_str += "%volunteers cannot be assigned to 2 shifts at once\n"
        model_str += "constraint forall(s1 in Shifts)(forall(s2 in Shifts)(forall(v in volunteers)(if clashing[s1,s2] /\ assignments[s1,v] then assignments[s2,v] == false endif)));\n\n"

        # All seats are filled section
        model_str += '%all vehicles are filled\n'
        seats = self.calculator.get_seats_per_asset_type()
        for index, asset_type in enumerate(self.calculator.get_asset_types()):
            if full:
                model_str += f'constraint forall(s in Shifts)(if is{asset_type.code}[s] then sum(v in volunteers)(assignments[s,v]) = {seats[index]} endif);\n'
            else:
                model_str += f'constraint forall(s in Shifts)(if is{asset_type.code}[s] then sum(v in volunteers)(assignments[s,v]) <= {seats[index]} endif);\n'
        model_str += '\n'

        # Seat requirements section
        for seat_number in range(1, self.calculator.get_maximum_number_of_seats() + 1):
            model_str += f'%Seat{seat_number} Requirements\n'
            model_str += f'constraint forall(s in Shifts)(forall(v in volunteers) (if seat{seat_number}[s] == v then assignments[s,v] = true endif));\n'
            for asset_type in self.calculator.get_asset_types():
                role = self.calculator.get_seat_roles(seat_number, asset_type)
                if role is not None:
                    model_str += f'constraint forall(s in Shifts)(if is{asset_type.code}[s] then forall(v in volunteers)(if seat{seat_number}[s] == v then is{role.code}[v] = true endif) endif);\n'
                else:
                    # If the asset doesn't require this seat, set this seat equal to the first seat
                    model_str += f'constraint forall(s in Shifts)(if is{asset_type.code}[s] then seat{seat_number}[s] == seat1[s] endif);\n'
            model_str += '\n'

        model_str += "%if a volunteer is not on any seats of a shift, they are not on the shift\n"
        model_str += "constraint forall(s in Shifts)(forall(v in volunteers) (if "
        model_str += ' /\ '.join(
            [f'seat{x}[s] != v' for x in range(1, self.calculator.get_maximum_number_of_seats() + 1)])
        model_str += " then assignments[s,v] = false endif));\n\n"

        # More constant strings.
        model_str += "%maps shifts to hours worked\n"
        model_str += "constraint forall(v in volunteers)(forall(s in Shifts)(if assignments[s,v] then hoursOnAssignment[v,s] = shiftLength[s] else hoursOnAssignment[v,s] = 0 endif));\n\n"
        model_str += "%defines total hours for each volunteer\n"
        model_str += "constraint forall(v in volunteers)(totalHours[v] == sum(s in Shifts)(hoursOnAssignment[v,s]));\n\n"
        model_str += "%ensures no one is overworked\n"
        model_str += "constraint forall(v in volunteers)(totalHours[v] <= preferredHours[v]);\n\n"
        model_str += "%minimise for the sum of squares difference between preferred work and actual work\n"
        model_str += "%solve minimize sum(v in volunteers)((preferredHours[v] - totalHours[v])*(preferredHours[v] - totalHours[v]))\n"
        if full:
            model_str += "solve satisfy\n"
        else:
            model_str += "solve maximize sum(s in Shifts)(sum(v in volunteers)(assignments[s,v]))\n"

        if self.debug:
            print(model_str)
        return model_str

    def solve(self, model_str: str):
        # Instantiate the model
        gecode = minizinc.Solver.lookup("gecode")
        model = minizinc.Model()
        model.add_string(model_str)
        instance = minizinc.Instance(gecode, model)

        # Add the model parameters
        instance["V"] = self.calculator.get_number_of_volunteers()
        instance["S"] = self.calculator.get_number_of_vehicles()
        instance["preferredHours"] = self.calculator.get_preferred_hours()
        instance["shiftLength"] = self.calculator.get_shift_lengths()
        instance["compatible"] = self.calculator.calculate_compatibility()
        instance["clashing"] = self.calculator.calculate_clashes()

        # Add the asset type mappings
        asset_mapping = self.calculator.calculate_asset_types()
        for index, asset_type in enumerate(self.calculator.get_asset_types()):
            instance[f'is{asset_type.code}'] = asset_mapping[index]

        # Add the role mappings
        role_mapping = self.calculator.calculate_roles()
        for index, role in enumerate(self.calculator.get_roles()):
            instance[f'is{role.code}'] = role_mapping[index]
        result = instance.solve()
        print(f'Result: {result}')
        return result

    def save_result(self, session, result) -> None:
        """
        Save a model result to the database.
        @param session: SQL Alchemy session to use
        @param result: The model result
        """
        for index, asset_request_vehicle in enumerate(self.calculator.get_asset_request_vehicles()):
            seats = self.calculator.get_seats_for_asset_type(asset_request_vehicle.type)
            for seat_number in range(1, self.calculator.get_maximum_number_of_seats() + 1):
                if seat_number <= seats:
                    # TODO: Tech Debt:
                    #   - Make this a FK reference, not a string
                    asset_type = self.calculator.get_asset_type_by_code(asset_request_vehicle.type)
                    role = self.calculator.get_seat_roles(seat_number, asset_type)

                    # Determine which user is being referenced.
                    # TODO: Question:
                    #  Is Minizinc 0 indexed or 1 indexed?
                    user_index = result[f'seat{seat_number}'][index]
                    if user_index == len(self.calculator.get_users()):
                        add_shift(session, None, asset_request_vehicle.id, seat_number, [f'{role.code}'])
                    else:
                        user = self.calculator.get_users()[result[f'seat{seat_number}'][index]]
                        add_shift(session, user.id, asset_request_vehicle.id, seat_number, [f'{role.code}'])




    def save_empty_result(self, session):
        """
        Save empty rows when a optimisation fails so you can manually assign people.
        @param session: SQL Alchemy session to use
        @return: None
        """
        for index, asset_request_vehicle in enumerate(self.calculator.get_asset_request_vehicles()):
            seats = self.calculator.get_seats_for_asset_type(asset_request_vehicle.type)
            for seat_number in range(1, self.calculator.get_maximum_number_of_seats() + 1):
                if seat_number <= seats:
                    # TODO: Tech Debt:
                    #   - Make this a FK reference, not a string
                    asset_type = self.calculator.get_asset_type_by_code(asset_request_vehicle.type)
                    role = self.calculator.get_seat_roles(seat_number, asset_type)
                    add_shift(session, None, asset_request_vehicle.id, seat_number, [f'{role.code}'])
