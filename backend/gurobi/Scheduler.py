from datetime import *
from minizinc import *

def rangeOverlaps(range1, range2):
    start1 = range1[0]
    start2 = range2[0]
    end1 = range1[1]
    end2 = range2[1]
    if (end1 < start2) or (end2 < start1):
        return False
    else:
        return True


def rangeSurrounds(range1, range2):
    start1 = range1[0]
    start2 = range2[0]
    end1 = range1[1]
    end2 = range2[1]
    if start1 <= start2 and end1 >= end2:
        return True
    else:
        return False

def getDuration(start, end):
    diff = end - start
    hours = int(diff.total_seconds()/3600)
    return hours

def addLightUnitToOutput(seats, currentRequest):
    output = []
    for i in range(2):
        voldict = {}
        role = []
        voldict["ID"] = seats[i][currentRequest]
        voldict["positionID"] = i
        if i == 0:
            role.append("driver")
            role.append("crewLeader")
        if i == 1:
            role.append("advanced")
        voldict["role"] = role
        output.append(voldict)
    return output


def addMediumTankerToOutput(seats, currentRequest):
    output = []
    for i in range(3):
        voldict = {}
        role = []
        voldict["ID"] = seats[i][currentRequest]
        voldict["positionID"] = i
        if i == 0:
            role.append("driver")
        if i == 1:
            role.append("crewLeader")
        if i == 2:
            role.append("basic")
        voldict["role"] = role
        output.append(voldict)
    return output


def addHeavyTankerToOutput(seats, currentRequest):
    output = []
    for i in range(5):
        voldict = {}
        role = []
        voldict["ID"] = seats[i][currentRequest]
        voldict["positionID"] = i
        if i == 0:
            role.append("driver")
        if i == 1:
            role.append("crewLeader")
        if i > 1 and i < 4:
            role.append("advanced")
        if i == 4:
            role.append("basic")
        voldict["role"] = role
        output.append(voldict)
    return output



'''
this code is for testing purposes:

Volunteers = []
for i in range(12):
    volunteer = {}
    volunteer["ID"] = i
    volunteer["prefHours"] = 69945585 + 1
    volunteer["possibleRoles"] = ["basic", "advanced", "crewLeader", "driver"]
    start = datetime.min
    end = datetime.max
    volunteer["availabilities"] = [(start,end)]
    Volunteers.append(volunteer)
    
AssetRequests = []
for i in range(2):
    assetrequest = {}
    assetrequest["shiftID"] = i
    assetrequest["assetClass"] = "lightUnit"
    start = datetime.now()
    end = datetime.max
    assetrequest["timeframe"] = (start,end)
    AssetRequests.append(assetrequest)

for i in range(1):
    assetrequest = {}
    assetrequest["shiftID"] = i
    assetrequest["assetClass"] = "heavyTanker"
    start = datetime.now()
    end = datetime.max
    assetrequest["timeframe"] = (start,end)
    AssetRequests.append(assetrequest)
'''


#Takes a list of Volunteers and Requests and returns a volunteer assignment and model
def Schedule(Volunteers, VehicleRequest):

    #create an array of preferredHours
    preferredHours = []
    for volunteer in Volunteers:
        preferredHours.append(volunteer["prefHours"])

    shiftLengths = []
    for request in VehicleRequest:
        start = request["timeframe"][0]
        end = request["timeframe"][1]
        shiftLengths.append(getDuration(start,end))

    compatible = []
    for request in VehicleRequest:
        requestRow = []
        requestTime = request["timeframe"]
        for volunteer in Volunteers:
            temp = False
            for availability in volunteer["availabilities"]:
                if(rangeSurrounds(availability, requestTime)):
                    temp = True
            requestRow.append(temp)
        compatible.append(requestRow)

    clashing = []
    for request1 in VehicleRequest:
        currentRequestClashes = []
        for request2 in VehicleRequest:
            currentRequestClashes.append(rangeOverlaps(request1["timeframe"], request2["timeframe"]))
        clashing.append(currentRequestClashes)
    for i in range(len(VehicleRequest)):
        clashing[i][i] = False

    isHeavy = []
    isMedium = []
    isLight = []
    for request in VehicleRequest:
        if request["assetClass"] == "heavyTanker":
            isHeavy.append(True)
            isMedium.append(False)
            isLight.append(False)
        if request["assetClass"] == "mediumTanker":
            isHeavy.append(False)
            isMedium.append(True)
            isLight.append(False)
        if request["assetClass"] == "lightUnit":
            isHeavy.append(False)
            isMedium.append(False)
            isLight.append(True)

    isDriver = []
    isCrewLeader = []
    isAdvanced = []
    isBasic = []
    for volunteer in Volunteers:
        basic = False
        advanced = False
        crewLeader = False
        driver = False
        for qualification in volunteer["possibleRoles"]:
            if qualification == "basic":
                basic = True
            if qualification == "advanced":
                advanced = True
            if qualification == "crewLeader":
                crewLeader = True
            if qualification == "driver":
                driver = True
        isBasic.append(basic)
        isAdvanced.append(advanced)
        isCrewLeader.append(crewLeader)
        isDriver.append(driver)

    gecode = Solver.lookup("gecode")
    model = Model()
    model.add_string(
        """
        int: V;
        int: S;
        set of int: Volunteers = 1..V;
        set of int: Shifts = 1..S;
        
        array[Shifts,Volunteers] of bool: compatible;
        array[Shifts,Shifts] of bool: clashing;
        array[Shifts,Volunteers] of var bool: assignments;
        array[Volunteers] of int: preferredHours;
        array[Shifts] of int: shiftLength;
        
        array[Shifts] of bool: isHeavy;
        array[Shifts] of bool: isMedium;
        array[Shifts] of bool: isLight;
        
        array[Volunteers] of bool: isBasic;
        array[Volunteers] of bool: isAdvanced;
        array[Volunteers] of bool: isCrewLeader;
        array[Volunteers] of bool: isDriver;
        
        array[Shifts] of var Volunteers: seat1;
        array[Shifts] of var Volunteers: seat2;
        array[Shifts] of var Volunteers: seat3;
        array[Shifts] of var Volunteers: seat4;
        array[Shifts] of var Volunteers: seat5;
        
        array[Volunteers,Shifts] of var int: hoursOnAssignment;
        array[Volunteers] of var int: totalHours;
        
        %volunteer availability check
        constraint forall(s in Shifts)(forall(v in Volunteers)(if compatible[s,v] == false then assignments[s,v] == false endif));
        
        %volunteers cannot be assigned to 2 shifts at once
        constraint forall(s1 in Shifts)(forall(s2 in Shifts)(forall(v in Volunteers)(if clashing[s1,s2] /\ assignments[s1,v] then assignments[s2,v] == false endif)));
        
        %all vehicles are filled
        constraint forall(s in Shifts)(if isHeavy[s] then sum(v in Volunteers)(assignments[s,v]) = 5 endif);
        constraint forall(s in Shifts)(if isMedium[s] then sum(v in Volunteers)(assignments[s,v]) = 3 endif);
        constraint forall(s in Shifts)(if isLight[s] then sum(v in Volunteers)(assignments[s,v]) = 2 endif);
        
        %Seat1 Requirements
        constraint forall(s in Shifts)(forall(v in Volunteers) (if seat1[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(forall(v in Volunteers)(if seat1[s] == v then isDriver[v] = true endif));
        constraint forall(s in Shifts)(if isLight[s] then forall(v in Volunteers)(if seat1[s] == v then isCrewLeader[v] = true endif) endif);
        
        %seat2 Requirements
        constraint forall(s in Shifts)(forall(v in Volunteers) (if seat2[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if isLight[s] then forall(v in Volunteers)(if seat2[s] == v then isAdvanced[v] = true endif) endif);
        constraint forall(s in Shifts)(if isMedium[s] then forall(v in Volunteers)(if seat2[s] == v then isCrewLeader[v] = true endif) endif);
        constraint forall(s in Shifts)(if isHeavy[s] then forall(v in Volunteers)(if seat2[s] == v then isCrewLeader[v] = true endif) endif);
        
        %seat3 Requirements
        constraint forall(s in Shifts)(forall(v in Volunteers) (if seat3[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if isLight[s] then seat3[s] == seat2[s] endif);
        constraint forall(s in Shifts)(if isMedium[s] then forall(v in Volunteers)(if seat3[s] == v then isBasic[v] = true endif) endif);
        constraint forall(s in Shifts)(if isHeavy[s] then forall(v in Volunteers)(if seat3[s] == v then isAdvanced[v] = true endif) endif);
        
        %seat4 Requirements
        constraint forall(s in Shifts)(forall(v in Volunteers) (if seat4[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if isLight[s] then seat4[s] == seat2[s] endif);
        constraint forall(s in Shifts)(if isMedium[s] then seat4[s] == seat3[s] endif);
        constraint forall(s in Shifts)(if isHeavy[s] then forall(v in Volunteers)(if seat4[s] == v then isAdvanced[v] = true endif) endif);
        
        %seat5 Requirements
        constraint forall(s in Shifts)(forall(v in Volunteers) (if seat5[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if isLight[s] then seat5[s] == seat2[s] endif);
        constraint forall(s in Shifts)(if isMedium[s] then seat5[s] == seat3[s] endif);
        constraint forall(s in Shifts)(if isHeavy[s] then forall(v in Volunteers)(if seat5[s] == v then isBasic[v] = true endif) endif);
        
        %if a volunteer is not on any seats of a shift, they are not on the shift
        constraint forall(s in Shifts)(forall(v in Volunteers) (if seat5[s] != v /\ seat4[s] != v /\ seat3[s] != v /\ seat2[s] != v /\ seat1[s] != v then assignments[s,v] = false endif));
        
        
        %maps shifts to hours worked
        constraint forall(v in Volunteers)(forall(s in Shifts)(if assignments[s,v] then hoursOnAssignment[v,s] = shiftLength[s] else hoursOnAssignment[v,s] = 0 endif));
        
        %defines total hours for each volunteer
        constraint forall(v in Volunteers)(totalHours[v] == sum(s in Shifts)(hoursOnAssignment[v,s]));
        
        %ensures no one is overworked
        constraint forall(v in Volunteers)(totalHours[v] <= preferredHours[v]);
        
        %minimise for the sum of squares difference between preferred work and actual work
        %solve minimize sum(v in Volunteers)((preferredHours[v] - totalHours[v])*(preferredHours[v] - totalHours[v]))
        solve satisfy
        """
    )

    instance = Instance(gecode, model)
    instance["V"] = len(Volunteers)
    instance["S"] = len(VehicleRequest)
    instance["preferredHours"] = preferredHours
    instance["shiftLength"] = shiftLengths
    instance["compatible"] = compatible
    instance["clashing"] = clashing
    instance["isHeavy"] = isHeavy
    instance["isMedium"] = isMedium
    instance["isLight"] = isLight
    instance["isBasic"] = isBasic
    instance["isAdvanced"] = isAdvanced
    instance["isCrewLeader"] = isCrewLeader
    instance["isDriver"] = isDriver
    result = instance.solve()

    if result.solution:
        output = []
        for i in range(len(VehicleRequest)):
            vehicledict = {}
            vehicledict["shiftID"] = VehicleRequest[i]["shiftID"]
            vehicledict["assetClass"] = VehicleRequest[i]["assetClass"]
            seats = []
            seats.append(result["seat1"])
            seats.append(result["seat2"])
            seats.append(result["seat3"])
            seats.append(result["seat4"])
            seats.append(result["seat5"])
            if vehicledict["assetClass"] == "lightUnit":
                volunteers = addLightUnitToOutput(seats, i)
            if vehicledict["assetClass"] == "mediumTanker":
                volunteers = addMediumTankerToOutput(seats, i)
            if vehicledict["assetClass"] == "heavyTanker":
                volunteers = addHeavyTankerToOutput(seats, i)
            vehicledict["volunteers"] = volunteers
            output.append(vehicledict)
    else:
        print("failed to solve, invalid model")
        output = []
    return output

