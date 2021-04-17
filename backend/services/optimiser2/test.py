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


