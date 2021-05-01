import minizinc
from sqlalchemy import orm

from domain import session_scope
from repository.asset_request_volunteer_repository import add_shift
from services.optimiser3.calculator import Calculator


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
        int: C;
        set of int: CLASH = 1..C;
        
        int: A;
        set of int: ASSETSHIFT = 1..A;
        
        int: S;
        set of int: ROLE = 1..S;      
        
        int: R;
        set of int: VOLUNTEER = 1..R;
        
        array[ASSETSHIFT,ASSETSHIFT] of bool: clashing; % NxM array storing pairs of clashing shifts
        array[ASSETSHIFT, ROLE] of int: sreq; % NxM array storing asset shifts (rows) and roles(columns), [n,m] is how many of those roles are required. 
        array[ASSETSHIFT,VOLUNTEER] of bool: compatible; % NxM array storing if the volunteer is available for that asset shift. 
        array[VOLUNTEER, ROLE] of bool: mastery; %NxM array storing the volunteer can perform that action 
        
        %~~~~~~~~~~~~~~~~~~~
        % Decision variables
        array[ASSETSHIFT,VOLUNTEER,ROLE] of var bool: contrib; % ROLE contribution assignment
        %contrib = 1 iff volunteer r contributes with ROLE s to assetshift a.
        
        %~~~~~~~~~~~~~~~~~~~
        % Constraints
        % ROLE constraint: ROLE requirements are satisfied
        constraint forall(a in ASSETSHIFT, s in ROLE where sreq[a,s]>0)(
          sum(r in VOLUNTEER)(contrib[a,r,s]) <= sreq[a,s]
        );
        
        % Non-Multi-Tasking constraint: Maximum of one contribution to each activity
        constraint forall(a in ASSETSHIFT, r in VOLUNTEER)(
          sum(s in ROLE where mastery[r,s]==true /\ sreq[a,s]>0)
             (contrib[a,r,s]) <= 1
        );
        
        % ROLE constraint: VOLUNTEERs only use ROLEs they have mastered
        constraint forall(a in ASSETSHIFT, r in VOLUNTEER, s in ROLE)(
          contrib[a,r,s] <= bool2int(mastery[r,s])
        );
        
        % Compatibility constraint: VOLUNTEERs are only assigned shifts they are compatible with
        constraint forall(a in ASSETSHIFT, r in VOLUNTEER)(
          sum(s in ROLE)(contrib[a,r,s]) <= bool2int(compatible[a,r])
        );
        
        % Clashing constraint: VOLUNTEERs cannot be assigned to 2 shifts that clash
        constraint forall(c in CLASH)(
          let {int: a1 = clashing[c,1],
               int: a2 = clashing[c,2]} in 
          forall(r in VOLUNTEER)(
            sum(s in ROLE)(contrib[a1,r,s] + contrib[a2,r,s]) <= 1
          )
        );
        
        %~~~~~~~~~~~~~~~~~~~
        % Objective
        solve satisfy;
        """
        return model_str

    def solve(self):
        # Instantiate the model
        gecode = minizinc.Solver.lookup("gecode")
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

        # Add the model parameters
        instance["A"] = self.calculator.get_number_of_vehicles()
        instance["C"] = self.calculator.get_number_of_vehicles()
        instance["R"] = self.calculator.get_number_of_volunteers()
        instance["S"] = self.calculator.get_number_of_roles()
        instance["clashing"] = self.calculator.calculate_clashes()
        instance["sreq"] = self.calculator.calculate_skill_requirement()
        instance['compatible'] = self.calculator.calculate_compatibility()
        instance['mastery'] = self.calculator.calculate_mastery()

        result = instance.solve()
        print(f'Result: {result}')
        return result

    def save_result(self, session, result) -> None:
        """
        Save a model result to the database.
        @param session: SQL Alchemy session to use
        @param result: The model result
        """


with session_scope() as session:
    o = Optimiser(session, 135, True)
    o.solve()
