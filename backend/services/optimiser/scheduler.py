import minizinc


# range1 and range2 are tuples (or 2 item lists) with a start and end time
# the function returns true if the two ranges overlap
def range_overlaps(range1, range2):
    start1 = range1[0]
    start2 = range2[0]
    end1 = range1[1]
    end2 = range2[1]
    if (end1 < start2) or (end2 < start1):
        return False
    else:
        return True


# range1 and range2 are tuples (or 2 item lists) with a start and end time
# the function returns true if the first range completely encompasses the second
def range_surrounds(range1, range2):
    start1 = range1[0]
    start2 = range2[0]
    end1 = range1[1]
    end2 = range2[1]
    print(range1, range2)
    if start1 <= start2 and end1 >= end2:
        return True
    else:
        return False


# this function takes two datetimes and returns the difference/duration between them
def get_duration(start, end):
    diff = end - start
    hours = int(diff.total_seconds() / 3600)
    return hours


# this is a helper function, it formats the output of light units for the scheduler
def add_light_unit_to_output(seats, currentRequest, volunteers):
    output = []
    already_added = []
    for i in range(2):
        volunteer_dict = {}
        role = []
        index = seats[i][currentRequest] - 1
        if index < 0 or (index in already_added):
            volunteer_dict["ID"] = -1
        else:
            volunteer_dict["ID"] = volunteers[index]["ID"]
        volunteer_dict["positionID"] = i
        if i == 0:
            role.append("driver")
            role.append("crewLeader")
        if i == 1:
            role.append("advanced")
        volunteer_dict["role"] = role
        already_added.append(index)
        output.append(volunteer_dict)

    return output


# this is a helper function, it formats the output of medium tankers for the scheduler
def add_medium_tanker_to_output(seats, current_request, volunteers):
    output = []
    already_added = []
    for i in range(3):
        volunteer_dict = {}
        role = []
        index = seats[i][current_request] - 1
        if index < 0 or (index in already_added):
            volunteer_dict["ID"] = -1
        else:
            volunteer_dict["ID"] = volunteers[index]["ID"]
        volunteer_dict["positionID"] = i
        if i == 0:
            role.append("driver")
        if i == 1:
            role.append("crewLeader")
        if i == 2:
            role.append("basic")
        volunteer_dict["role"] = role
        already_added.append(index)
        output.append(volunteer_dict)
    return output


# this is a helper function, it formats the output of heavy tankers for the scheduler
def add_heavy_tanker_to_output(seats, currentRequest, volunteers):
    output = []
    already_added = []
    for i in range(5):
        volunteer_dict = {}
        role = []
        index = seats[i][currentRequest] - 1
        if index < 0 or (index in already_added):
            volunteer_dict["ID"] = -1
        else:
            volunteer_dict["ID"] = volunteers[index]["ID"]
        volunteer_dict["positionID"] = i
        if i == 0:
            role.append("driver")
        if i == 1:
            role.append("crewLeader")
        if i > 1 and i < 4:
            role.append("advanced")
        if i == 4:
            role.append("basic")
        volunteer_dict["role"] = role
        already_added.append(index)
        output.append(volunteer_dict)
    return output


# this is a helper function which generates a list of shift lengths given a list of vehicle requests
def generate_shift_lengths(vehicle_request):
    shift_lengths = []
    for request in vehicle_request:
        start = request["timeframe"][0]
        end = request["timeframe"][1]
        shift_lengths.append(get_duration(start, end))
    return shift_lengths


# this is a helper function which determines the compatibility for volunteer availability and shift times for the 
# scheduler Takes scheduler inputs and returns a 2d array of booleans where each element is the compatibility of 1 
# volunteer and 1 shift 
def generate_compatibility(volunteers, vehicle_request):
    compatible = []
    for request in vehicle_request:
        request_row = []
        request_time = request["timeframe"]
        for volunteer in volunteers:
            temp = True
            # TODO: This comparison is broken
            # for availability in volunteer["availabilities"]:
            #    if range_surrounds(availability, request_time):
            #        temp = True
            request_row.append(temp)
        compatible.append(request_row)
    return compatible


# this is a helper function which determines any clashes within a list of vehicle requests Takes scheduler inputs and
# returns a 2d array of booleans where each element is the compatability of 1 shift with another shift
def generate_clashes(vehicle_request):
    clashing = []
    for request1 in vehicle_request:
        current_request_clashes = []
        for request2 in vehicle_request:
            current_request_clashes.append(range_overlaps(request1["timeframe"], request2["timeframe"]))
        clashing.append(current_request_clashes)
    for i in range(len(vehicle_request)):
        clashing[i][i] = False
    return clashing


# Takes a list of volunteers and Requests and returns a volunteer assignment and model
def schedule(volunteers, vehicle_request):
    temp = full_schedule(volunteers, vehicle_request)
    # if a full solve was possible, return it
    if temp != []:
        return temp
    # otherwise, return a partial solve
    else:
        print("Generating partial fill")
        return partial_schedule(volunteers, vehicle_request)


# this function should only be called from Schedule
# This attempts a complete assignment, returning an empty list if a full assignment is impossible
def full_schedule(volunteers, vehicle_request):
    # create an array of preferredHours
    preferred_hours = []
    for volunteer in volunteers:
        preferred_hours.append(volunteer["prefHours"])

    # generates a list of shift lengths corresponding to each vehicle request
    shift_lengths = generate_shift_lengths(vehicle_request)

    # generates a 2d array of booleans for the model
    # each entry denotes the compatibility of 1 volunteer to 1 request
    compatible = generate_compatibility(volunteers, vehicle_request)

    # generates a 2d array of booleans for the model
    # each entry denotes whether there is a clash (true) between vehicle requests
    clashing = generate_clashes(vehicle_request)

    # the following codeblock generates 3 lists of booleans
    # if is_heavy(index) = true then vehicle_request(index) is a heavy tanker
    # if is_medium(index) = true then vehicle_request(index) is a medium tanker
    # if is_light(index) = true then vehicle_request(index) is a light unit
    is_heavy = []
    is_medium = []
    is_light = []
    for request in vehicle_request:
        if request["assetClass"] == "heavyTanker":
            is_heavy.append(True)
            is_medium.append(False)
            is_light.append(False)
        if request["assetClass"] == "mediumTanker":
            is_heavy.append(False)
            is_medium.append(True)
            is_light.append(False)
        if request["assetClass"] == "lightUnit":
            is_heavy.append(False)
            is_medium.append(False)
            is_light.append(True)

    # the following codeblock generates 4 lists of booleans
    # if is_driver(index) = true then volunteer(index) is a driver
    # if is_crew_leader(index) = true then volunteer(index) is a crewleader
    # if is_advanced(index) = true then volunteer(index) is advanced
    # if is_basic(index) = true then volunteer(index) is basic
    is_driver = []
    is_crew_leader = []
    is_advanced = []
    is_basic = []
    for volunteer in volunteers:
        basic = False
        advanced = False
        crew_leader = False
        driver = False
        for qualification in volunteer["possibleRoles"]:
            if qualification == "basic":
                basic = True
            if qualification == "advanced":
                advanced = True
            if qualification == "crew_leader":
                crew_leader = True
            if qualification == "driver":
                driver = True
        is_basic.append(basic)
        is_advanced.append(advanced)
        is_crew_leader.append(crew_leader)
        is_driver.append(driver)

    # we are using the gecode optimiser
    gecode = minizinc.Solver.lookup("gecode")
    # create the model
    model = minizinc.Model()
    # the following string generates the minizinc model for a full solve
    model.add_string(
        """
        int: V;
        int: S;
        set of int: volunteers = 1..V;
        set of int: Shifts = 1..S;

        array[Shifts,volunteers] of bool: compatible;
        array[Shifts,Shifts] of bool: clashing;
        array[Shifts,volunteers] of var bool: assignments;
        array[volunteers] of int: preferredHours;
        array[Shifts] of int: shiftLength;

        array[Shifts] of bool: isHeavy;
        array[Shifts] of bool: is_medium;
        array[Shifts] of bool: is_light;

        array[volunteers] of bool: is_basic;
        array[volunteers] of bool: is_advanced;
        array[volunteers] of bool: is_crew_leader;
        array[volunteers] of bool: is_driver;

        array[Shifts] of var volunteers: seat1;
        array[Shifts] of var volunteers: seat2;
        array[Shifts] of var volunteers: seat3;
        array[Shifts] of var volunteers: seat4;
        array[Shifts] of var volunteers: seat5;

        array[volunteers,Shifts] of var int: hoursOnAssignment;
        array[volunteers] of var int: totalHours;

        %volunteer availability check
        constraint forall(s in Shifts)(forall(v in volunteers)(if compatible[s,v] == false then assignments[s,v] == false endif));

        %volunteers cannot be assigned to 2 shifts at once
        constraint forall(s1 in Shifts)(forall(s2 in Shifts)(forall(v in volunteers)(if clashing[s1,s2] /\ assignments[s1,v] then assignments[s2,v] == false endif)));

        %all vehicles are filled
        constraint forall(s in Shifts)(if isHeavy[s] then sum(v in volunteers)(assignments[s,v]) = 5 endif);
        constraint forall(s in Shifts)(if is_medium[s] then sum(v in volunteers)(assignments[s,v]) = 3 endif);
        constraint forall(s in Shifts)(if is_light[s] then sum(v in volunteers)(assignments[s,v]) = 2 endif);

        %Seat1 Requirements
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat1[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(forall(v in volunteers)(if seat1[s] == v then is_driver[v] = true endif));
        constraint forall(s in Shifts)(if is_light[s] then forall(v in volunteers)(if seat1[s] == v then is_crew_leader[v] = true endif) endif);

        %seat2 Requirements
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat2[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if is_light[s] then forall(v in volunteers)(if seat2[s] == v then is_advanced[v] = true endif) endif);
        constraint forall(s in Shifts)(if is_medium[s] then forall(v in volunteers)(if seat2[s] == v then is_crew_leader[v] = true endif) endif);
        constraint forall(s in Shifts)(if isHeavy[s] then forall(v in volunteers)(if seat2[s] == v then is_crew_leader[v] = true endif) endif);

        %seat3 Requirements
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat3[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if is_light[s] then seat3[s] == seat2[s] endif);
        constraint forall(s in Shifts)(if is_medium[s] then forall(v in volunteers)(if seat3[s] == v then is_basic[v] = true endif) endif);
        constraint forall(s in Shifts)(if isHeavy[s] then forall(v in volunteers)(if seat3[s] == v then is_advanced[v] = true endif) endif);

        %seat4 Requirements
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat4[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if is_light[s] then seat4[s] == seat2[s] endif);
        constraint forall(s in Shifts)(if is_medium[s] then seat4[s] == seat3[s] endif);
        constraint forall(s in Shifts)(if isHeavy[s] then forall(v in volunteers)(if seat4[s] == v then is_advanced[v] = true endif) endif);

        %seat5 Requirements
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat5[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if is_light[s] then seat5[s] == seat2[s] endif);
        constraint forall(s in Shifts)(if is_medium[s] then seat5[s] == seat3[s] endif);
        constraint forall(s in Shifts)(if isHeavy[s] then forall(v in volunteers)(if seat5[s] == v then is_basic[v] = true endif) endif);

        %if a volunteer is not on any seats of a shift, they are not on the shift
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat5[s] != v /\ seat4[s] != v /\ seat3[s] != v /\ seat2[s] != v /\ seat1[s] != v then assignments[s,v] = false endif));


        %maps shifts to hours worked
        constraint forall(v in volunteers)(forall(s in Shifts)(if assignments[s,v] then hoursOnAssignment[v,s] = shiftLength[s] else hoursOnAssignment[v,s] = 0 endif));

        %defines total hours for each volunteer
        constraint forall(v in volunteers)(totalHours[v] == sum(s in Shifts)(hoursOnAssignment[v,s]));

        %ensures no one is overworked
        constraint forall(v in volunteers)(totalHours[v] <= preferredHours[v]);

        %minimise for the sum of squares difference between preferred work and actual work
        %solve minimize sum(v in volunteers)((preferredHours[v] - totalHours[v])*(preferredHours[v] - totalHours[v]))
        solve satisfy
        """
    )

    # initialise all the variables in the minizinc model from the variables we previously created
    instance = minizinc.Instance(gecode, model)
    instance["V"] = len(volunteers)
    instance["S"] = len(vehicle_request)
    instance["preferredHours"] = preferred_hours
    instance["shiftLength"] = shift_lengths
    instance["compatible"] = compatible
    instance["clashing"] = clashing
    instance["isHeavy"] = is_heavy
    instance["is_medium"] = is_medium
    instance["is_light"] = is_light
    instance["is_basic"] = is_basic
    instance["is_advanced"] = is_advanced
    instance["is_crew_leader"] = is_crew_leader
    instance["is_driver"] = is_driver
    # solve the model
    result = instance.solve()
    # if there is a valid solution, format it and output
    if result.solution:
        output = []
        for i in range(len(vehicle_request)):
            vehicledict = {}
            vehicledict["shiftID"] = vehicle_request[i]["shiftID"]
            vehicledict["assetClass"] = vehicle_request[i]["assetClass"]
            vehicledict["timeframe"] = vehicle_request[i]["timeframe"]
            seats = []
            seats.append(result["seat1"])
            seats.append(result["seat2"])
            seats.append(result["seat3"])
            seats.append(result["seat4"])
            seats.append(result["seat5"])
            if vehicledict["assetClass"] == "lightUnit":
                volunteers = add_light_unit_to_output(seats, i, volunteers)
            if vehicledict["assetClass"] == "mediumTanker":
                volunteers = add_medium_tanker_to_output(seats, i, volunteers)
            if vehicledict["assetClass"] == "heavyTanker":
                volunteers = add_heavy_tanker_to_output(seats, i, volunteers)
            vehicledict["volunteers"] = volunteers
            output.append(vehicledict)
    # if there is no valid model, output an empty list
    else:
        print("failed to solve, invalid model")
        output = []
    return output


# this function should only be called from Schedule
# This attempts a complete assignment, returning an empty list if a full assignment is impossible
def partial_schedule(volunteers, vehicle_request):
    # create an array of preferredHours
    preferred_hours = []
    for volunteer in volunteers:
        preferred_hours.append(volunteer["prefHours"])

    # generates a list of shift lengths corresponding to each vehicle request
    shift_lengths = generate_shift_lengths(vehicle_request)

    # generates a 2d array of booleans for the model
    # each entry denotes the compatability of 1 volunteer to 1 request
    compatible = generate_compatibility(volunteers, vehicle_request)

    # generates a 2d array of booleans for the model
    # each entry denotes whether there is a clash (true) between the corresponding vehicle requests
    clashing = generate_clashes(vehicle_request)

    # the following codeblock generates 3 lists of booleans
    # if is_heavy(index) = true then vehicle_request(index) is a heavy tanker
    # if is_medium(index) = true then vehicle_request(index) is a medium tanker
    # if is_light(index) = true then vehicle_request(index) is a light unit
    is_heavy = []
    is_medium = []
    is_light = []
    for request in vehicle_request:
        if request["assetClass"] == "heavyTanker":
            is_heavy.append(True)
            is_medium.append(False)
            is_light.append(False)
        if request["assetClass"] == "mediumTanker":
            is_heavy.append(False)
            is_medium.append(True)
            is_light.append(False)
        if request["assetClass"] == "lightUnit":
            is_heavy.append(False)
            is_medium.append(False)
            is_light.append(True)

    # the following codeblock generates 4 lists of booleans
    # if is_driver(index) = true then volunteer(index) is a driver
    # if is_crew_leader(index) = true then volunteer(index) is a crewleader
    # if is_advanced(index) = true then volunteer(index) is advanced
    # if is_basic(index) = true then volunteer(index) is basic
    is_driver = []
    is_crew_leader = []
    is_advanced = []
    is_basic = []
    for volunteer in volunteers:
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
        is_basic.append(basic)
        is_advanced.append(advanced)
        is_crew_leader.append(crewLeader)
        is_driver.append(driver)

    # we are using the gecode optimiser
    gecode = minizinc.Solver.lookup("gecode")
    # create the model
    model = minizinc.Model()
    # the following string generates the minizinc model for a full solve
    model.add_string(
        """
        int: V;
        int: S;
        set of int: volunteers = 1..V;
        set of int: Shifts = 1..S;

        array[Shifts,volunteers] of bool: compatible;
        array[Shifts,Shifts] of bool: clashing;
        array[Shifts,volunteers] of var bool: assignments;
        array[volunteers] of int: preferredHours;
        array[Shifts] of int: shiftLength;

        array[Shifts] of bool: is_heavy;
        array[Shifts] of bool: is_medium;
        array[Shifts] of bool: is_light;

        array[volunteers] of bool: is_basic;
        array[volunteers] of bool: is_advanced;
        array[volunteers] of bool: is_crew_leader;
        array[volunteers] of bool: is_driver;

        array[Shifts] of var 0..V: seat1;
        array[Shifts] of var 0..V: seat2;
        array[Shifts] of var 0..V: seat3;
        array[Shifts] of var 0..V: seat4;
        array[Shifts] of var 0..V: seat5;

        array[volunteers,Shifts] of var int: hoursOnAssignment;
        array[volunteers] of var int: totalHours;

        %volunteer availability check
        constraint forall(s in Shifts)(forall(v in volunteers)(if compatible[s,v] == false then assignments[s,v] == false endif));

        %volunteers cannot be assigned to 2 shifts at once
        constraint forall(s1 in Shifts)(forall(s2 in Shifts)(forall(v in volunteers)(if clashing[s1,s2] /\ assignments[s1,v] then assignments[s2,v] == false endif)));

        %all vehicles are (at most) filled. This allows for partial fills
        constraint forall(s in Shifts)(if is_heavy[s] then sum(v in volunteers)(assignments[s,v]) <= 5 endif);
        constraint forall(s in Shifts)(if is_medium[s] then sum(v in volunteers)(assignments[s,v]) <= 3 endif);
        constraint forall(s in Shifts)(if is_light[s] then sum(v in volunteers)(assignments[s,v]) <= 2 endif);

        %Seat1 Requirements
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat1[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(forall(v in volunteers)(if seat1[s] == v then is_driver[v] = true endif));
        constraint forall(s in Shifts)(if is_light[s] then forall(v in volunteers)(if seat1[s] == v then is_crew_leader[v] = true endif) endif);

        %seat2 Requirements
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat2[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if is_light[s] then forall(v in volunteers)(if seat2[s] == v then is_advanced[v] = true endif) endif);
        constraint forall(s in Shifts)(if is_medium[s] then forall(v in volunteers)(if seat2[s] == v then is_crew_leader[v] = true endif) endif);
        constraint forall(s in Shifts)(if is_heavy[s] then forall(v in volunteers)(if seat2[s] == v then is_crew_leader[v] = true endif) endif);

        %seat3 Requirements
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat3[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if is_light[s] then seat3[s] == seat2[s] endif);
        constraint forall(s in Shifts)(if is_medium[s] then forall(v in volunteers)(if seat3[s] == v then is_basic[v] = true endif) endif);
        constraint forall(s in Shifts)(if is_heavy[s] then forall(v in volunteers)(if seat3[s] == v then is_advanced[v] = true endif) endif);

        %seat4 Requirements
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat4[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if is_light[s] then seat4[s] == seat2[s] endif);
        constraint forall(s in Shifts)(if is_medium[s] then seat4[s] == seat3[s] endif);
        constraint forall(s in Shifts)(if is_heavy[s] then forall(v in volunteers)(if seat4[s] == v then is_advanced[v] = true endif) endif);

        %seat5 Requirements
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat5[s] == v then assignments[s,v] = true endif));
        constraint forall(s in Shifts)(if is_light[s] then seat5[s] == seat2[s] endif);
        constraint forall(s in Shifts)(if is_medium[s] then seat5[s] == seat3[s] endif);
        constraint forall(s in Shifts)(if is_heavy[s] then forall(v in volunteers)(if seat5[s] == v then is_basic[v] = true endif) endif);

        %if a volunteer is not on any seats of a shift, they are not on the shift
        constraint forall(s in Shifts)(forall(v in volunteers) (if seat5[s] != v /\ seat4[s] != v /\ seat3[s] != v /\ seat2[s] != v /\ seat1[s] != v then assignments[s,v] = false endif));


        %maps shifts to hours worked
        constraint forall(v in volunteers)(forall(s in Shifts)(if assignments[s,v] then hoursOnAssignment[v,s] = shiftLength[s] else hoursOnAssignment[v,s] = 0 endif));

        %defines total hours for each volunteer
        constraint forall(v in volunteers)(totalHours[v] == sum(s in Shifts)(hoursOnAssignment[v,s]));

        %ensures no one is overworked
        constraint forall(v in volunteers)(totalHours[v] <= preferredHours[v]);

        %maximise for number of volunteers assigned
        solve maximize sum(s in Shifts)(sum(v in volunteers)(assignments[s,v]))
        """
    )
    # initialise all the variables in the minizinc model from the variables we previously created
    instance = minizinc.Instance(gecode, model)
    instance["V"] = len(volunteers)
    instance["S"] = len(vehicle_request)
    instance["preferredHours"] = preferred_hours
    instance["shiftLength"] = shift_lengths
    instance["compatible"] = compatible
    instance["clashing"] = clashing
    instance["is_heavy"] = is_heavy
    instance["is_medium"] = is_medium
    instance["is_light"] = is_light
    instance["is_basic"] = is_basic
    instance["is_advanced"] = is_advanced
    instance["is_crew_leader"] = is_crew_leader
    instance["is_driver"] = is_driver
    # solve the model
    result = instance.solve()
    # if there is a valid solution, format it and output
    if result.solution:
        output = []
        for i in range(len(vehicle_request)):
            vehicle_dict = {}
            vehicle_dict["shiftID"] = vehicle_request[i]["shiftID"]
            vehicle_dict["assetClass"] = vehicle_request[i]["assetClass"]
            vehicle_dict["timeframe"] = vehicle_request[i]["timeframe"]
            seats = []
            seats.append(result["seat1"])
            seats.append(result["seat2"])
            seats.append(result["seat3"])
            seats.append(result["seat4"])
            seats.append(result["seat5"])
            if vehicle_dict["assetClass"] == "lightUnit":
                volunteers = add_light_unit_to_output(seats, i, volunteers)
            if vehicle_dict["assetClass"] == "mediumTanker":
                volunteers = add_medium_tanker_to_output(seats, i, volunteers)
            if vehicle_dict["assetClass"] == "heavyTanker":
                volunteers = add_heavy_tanker_to_output(seats, i, volunteers)
            vehicle_dict["volunteers"] = volunteers
            output.append(vehicle_dict)
    # if there is no valid model, output an empty list
    else:
        print("No partial fill possible")
        output = []
    return output

# Test Code
# print(Schedule(volunteers,AssetRequests))
