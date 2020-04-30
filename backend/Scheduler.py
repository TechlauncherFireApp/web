import gurobipy as gp
from gurobipy import GRB

from backend.DataGenerator import *
from backend.AssetTypes import *

#Takes a list of volunteers, returns a tupleList formatted for the constraint model
def formatAvailability(Volunteers):
    availability = gp.tuplelist()
    for volunteer in Volunteers:
        for shift in shiftpopulator():
            if volunteer.Availability[shift]:
                availability.append((volunteer.name, DayHourtoNumConverter(shift)))
    return availability

#Takes a list of Volunteers and VehicleRequirements and returns a volunteer assignment and model
def Schedule(Volunteers, VehicleRequirements):
    
    # Number of volunteers required for each shift. "time": (total, advanced)
    shiftRequirements = RequesttoRequirements(EveryWeekday)
    # shiftRequirements = {
    #     0: (1, 1)
    # }

    # Amount of hours each volunteer wants to work over the entire week
    preferredHours = {}
    for volunteer in Volunteers:
        preferredHours[volunteer.name] = volunteer.prefHours
    
    # Worker availability
    availability = formatAvailability(Volunteers)
    
    # list qualified workers
    advancedQualified = []
    for volunteer in Volunteers:
        if volunteer.Explvl == FireFighter.advanced:
            advancedQualified.append(volunteer)
    
    # Model
    model = gp.Model("assignment")

    # Assignment variables: assigned[v,s] == 1 if volunteer v is assigned to shift s.
    assigned = model.addVars(availability, ub=1, lb=0, name="assigned")

    #Constraints: total hours worked <= preferred hours for each volunteer
    constraints = []
    for volunteer in Volunteers:
        constraints.append(model.addConstr(assigned.sum(volunteer.name, '*'), GRB.LESS_EQUAL, preferredHours[volunteer.name], "prefHours_" + str(volunteer.name)))

    #Constraints: total volunteers met for each shift
    for shiftKey in shiftRequirements.keys():
        numRequired = shiftRequirements[shiftKey][0]
        constraints.append(model.addConstr(assigned.sum('*', shiftKey), GRB.EQUAL, numRequired, "ShiftFilled_" + str(shiftKey)))

    #Constraints: qualifications met for each shift
    for shiftKey in shiftRequirements.keys():
        numRequiredAdvanced = shiftRequirements[shiftKey][1]
        totalAdvanced = 0
        for volunteer in advancedQualified:
            totalAdvanced = totalAdvanced + assigned.sum(volunteer.name, shiftKey)
        constraints.append(model.addConstr(totalAdvanced, GRB.GREATER_EQUAL, numRequiredAdvanced, "ShiftQualified_" + str(shiftKey)))

    
    # The objective is to minimise the hours worked by volunteers (while still filling all shifts)
    model.setObjective( gp.quicksum(assigned[v,s] for v, s in availability), GRB.MINIMIZE)

    model.optimize()

    return (model, assigned)

v=volunteerGenerate(60)
model, assignment = Schedule(v, [])