import gurobipy as gp
from gurobipy import GRB

from backend.DataGenerator import *
from backend.AssetTypes import *

#Takes a list of volunteers, returns a tupleList formatted for the constraint model
from backend.VolunteerGraph import Assignment, VolunteerPlot


def formatAvailability(Volunteers):
    availability = gp.tuplelist()
    for volunteer in Volunteers:
        for shift in shiftpopulator():
            if volunteer.Availability[shift]:
                availability.append((volunteer.id, DayHourtoNumConverter(shift)))
    return availability

#Takes a list of Volunteers and VehicleRequirements and returns a volunteer assignment and model
def Schedule(Volunteers, VehicleRequest):
    
    # Number of volunteers required for each shift. "time": (total, advanced)
    shiftRequirements = RequesttoRequirements(VehicleRequest)

    # Amount of hours each volunteer wants to work over the entire week
    preferredHours = {}
    for volunteer in Volunteers:
        preferredHours[volunteer.id] = volunteer.prefHours
    
    # Volunteer availability
    availability = formatAvailability(Volunteers)
    formattedRequests = gp.tuplelist()
    for volunteer in Volunteers:
        for request in VehicleRequest:
            formattedRequests.append((volunteer.id, request.AssetType.LicenceNo, request.StartTime))
    
    # list qualified Volunteers
    advancedQualified = []
    for volunteer in Volunteers:
        if volunteer.Explvl == FireFighter.advanced:
            advancedQualified.append(volunteer)
    
    # Model
    model = gp.Model("assignment")

    # Assignment variables: assigned[v,s] == 1 if volunteer v is assigned to shift s.
    assigned = model.addVars(availability, ub=1, lb=0, name="assigned")
    assignedToVehicle = model.addVars(formattedRequests, ub=1, lb=0, name="assignedToVehicle")

    constraints = []

    # Constraints: volunteer must be assigned to a vehicle for an entire shift
    for volunteer in Volunteers:
        for request in VehicleRequest:
            shiftSum = 0
            for i in range(request.Duration):
                time = request.StartTime + i
                shiftSum = shiftSum + assigned.sum(volunteer.id, time)
            constraints.append(model.addGenConstrIndicator(assignedToVehicle[volunteer.id, request.AssetType.LicenceNo, request.StartTime], True, shiftSum, GRB.EQUAL, request.Duration))
            constraints.append(model.addGenConstrIndicator(assignedToVehicle[volunteer.id, request.AssetType.LicenceNo, request.StartTime], False, shiftSum, GRB.EQUAL, 0))


    #Constraints: total hours worked <= preferred hours for each volunteer
    for volunteer in Volunteers:
        constraints.append(model.addConstr(assigned.sum(volunteer.id, '*'), GRB.LESS_EQUAL, preferredHours[volunteer.id], "prefHours_" + str(volunteer.id)))

    #Constraints: total volunteers met for each shift
    for shiftKey in shiftRequirements.keys():
        numRequired = shiftRequirements[shiftKey][0]
        constraints.append(model.addConstr(assigned.sum('*', shiftKey), GRB.EQUAL, numRequired, "ShiftFilled_" + str(shiftKey)))

    #Constraints: qualifications met for each shift
    for shiftKey in shiftRequirements.keys():
        numRequiredAdvanced = shiftRequirements[shiftKey][1]
        totalAdvanced = 0
        for volunteer in advancedQualified:
            totalAdvanced = totalAdvanced + assigned.sum(volunteer.id, shiftKey)
        constraints.append(model.addConstr(totalAdvanced, GRB.GREATER_EQUAL, numRequiredAdvanced, "ShiftQualified_" + str(shiftKey)))

    
    # The objective is to minimise the hours worked by volunteers (while still filling all shifts)
    model.setObjective( gp.quicksum(assigned[v,s] for v, s in availability), GRB.MINIMIZE)

    model.optimize()

    assignments = []
    plotList=[]
    for volunteer in Volunteers:
        for request in VehicleRequest:
            value = assignedToVehicle[(volunteer.id, request.AssetType.LicenceNo, request.StartTime)].X
            if value > 0:
                assignments.append("volunteer " + str(volunteer.id) + ", " + str(volunteer.name) + " assigned to " + str(request.AssetType.type) + ", ID " + str(request.AssetType.LicenceNo) + " for the shift starting " + str(request.StartTime))
                plotList.append(Assignment(volunteer.id,request.StartTime,request.Duration))

    print(" ")
    for assignment in assignments:
        print(assignment)
    VolunteerPlot(plotList)
    return (model, assignedToVehicle)

v=volunteerGenerate(200)

model, assignment = Schedule(v, EveryWeekday)
