import gurobipy as gp
from gurobipy import GRB

from backend.DataGenerator import *

Volunteers = volunteerGenerate(5)

# Number of volunteers required for each shift. "time": (basic, advanced)
shiftRequirements = {
    "Mon1":  (1,1)
    }

# Amount of hours each volunteer wants to work over the entire week
preferredHours = {}
for volunteer in Volunteers:
    preferredHours[volunteer.name] = volunteer.prefHours
    
# Worker availability
availability = gp.tuplelist()
for volunteer in Volunteers:
    for shift in shiftpopulator():
        if volunteer.Availability[shift]:
            availability.append((volunteer.name, shift))

# Model
model = gp.Model("assignment")

# Assignment variables: assigned[v,s] == 1 if volunteer v is assigned to shift s.
assigned = model.addVars(availability, ub=1, lb=0, name="assigned")

# The objective is to minimise the hours worked by volunteers (while still filling all shifts)
model.setObjective( gp.quicksum(assigned[v,s] for v, s in availability), GRB.MINIMIZE)


