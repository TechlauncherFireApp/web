from domain import AssetRequestVehicle, Role, AssetRequestVolunteer, User, Qualification, UnavailabilityTime
from sqlalchemy import orm, func, alias
import numpy as np
import datetime


def get_input_A(session, request_id):
    asset_list_count = session.query(AssetRequestVehicle).filter(AssetRequestVehicle.request_id == request_id).count()
    return asset_list_count


def get_input_R(session):
    role_list_count = session.query(Role).count()
    return role_list_count


def get_input_P(session, request_id):
    asset_list = session.query(AssetRequestVehicle.id).filter(AssetRequestVehicle.request_id == request_id).all()
    position_count = 0
    for v_id in asset_list:
        asset_position_count = session.query(AssetRequestVolunteer).filter(
            AssetRequestVolunteer.vehicle_id == v_id[0]).count()
        position_count += asset_position_count
    return position_count


def get_input_V(session):
    volunteer_list_count = session.query(User.role).filter(User.role == "VOLUNTEER").count()
    return volunteer_list_count


def get_input_Q(session):
    qualification_list_count = session.query(Qualification).count()
    return qualification_list_count


def get_input_qualrequirements(session, request_id):
    A = get_input_A(session, request_id)
    P = get_input_P(session, request_id)
    Q = get_input_Q(session)
    qualrequirements_matrix = np.full((A, P, Q), False, dtype=bool)
    vehicle_list = get_vehicle_list(session, request_id)
    mark = 0
    for a in range(0, A):
        position_list = get_position_list(session, vehicle_list[a])
        position_in_vehicle = len(position_list)
        for p in range(0, position_in_vehicle):
            qualification_id = get_position_qualification(session, position_list[p])
            if qualification_id == None:
                continue
            else:
                for q in range(0, Q):
                    if q == qualification_id - 1:
                        qualrequirements_matrix[a][p + mark][q] = True
                        break
                    else:
                        continue
        mark += position_in_vehicle
    return qualrequirements_matrix


def get_input_rolerequirements(session, request_id):
    A = get_input_A(session, request_id)
    P = get_input_P(session, request_id)
    R = get_input_R(session)
    rolerequirements_matrix = np.full((A, P, R), False, dtype=bool)
    vehicle_list = get_vehicle_list(session, request_id)
    mark = 0
    for a in range(0, A):
        position_list = get_position_list(session, vehicle_list[a])
        position_in_vehicle = len(position_list)
        for p in range(0, position_in_vehicle):
            role_id = get_position_role(session, position_list[p])
            for r in range(0, R):
                if r == role_id - 1:
                    rolerequirements_matrix[a][p + mark][r] = True
                    break
                else:
                    continue
        mark += position_in_vehicle
    return rolerequirements_matrix


def get_input_posrequirements(session, request_id):
    A = get_input_A(session, request_id)
    P = get_input_P(session, request_id)
    vehicle_list = get_vehicle_list(session, request_id)
    posrequirements_matrix = np.full((P, A), False, dtype=bool)
    request_position = get_position_list_all(session, request_id)

    for p in range(0, len(request_position)):
        p_id = request_position[p]
        temp_matrix = np.full(A, False, dtype=bool)
        temp_asset = get_position_vehicle(session, p_id)
        for a in range(0, A):
            if vehicle_list[a] == temp_asset:
                temp_matrix[a] = True
                break
            else:
                continue
        posrequirements_matrix[p] = temp_matrix
    return posrequirements_matrix


def get_qualification_list(session):
    qualification_table = session.query(Qualification.id).all()
    qualification_type = []
    for i in qualification_table:
        qualification_type.append(i[0])
    return qualification_type


def get_input_qualability(session):
    V = get_input_V(session)
    Q = get_input_Q(session)
    qualification_type = get_qualification_list(session)
    qualability_matrix = np.full((V, Q), False, dtype=bool)
    v_qualification_list = session.query(User.qualifications).filter(User.role == "VOLUNTEER").all()

    for q in range(0, len(v_qualification_list)):
        temp_matrix = np.full(Q, False, dtype=bool)
        for q_type in range(0, Q):
            if qualification_type[q_type] in v_qualification_list[q][0]:
                temp_matrix[q_type] = True

        qualability_matrix[q] = temp_matrix

    return qualability_matrix


def get_role_list(session):
    role_table = session.query(Role.name).all()
    role_type = []
    for i in role_table:
        role_type.append(i[0])
    return role_type


def get_input_roleability(session):
    V = get_input_V(session)
    R = get_input_R(session)

    role_type = get_role_list(session)
    roleability_matrix = np.full((V, R), False, dtype=bool)
    v_role_list = session.query(User.possibleRoles).filter(User.role == "VOLUNTEER").all()

    for r in range(0, len(v_role_list)):
        temp_matrix = np.full(R, False, dtype=bool)
        for r_type in range(0, R):
            if role_type[r_type] in v_role_list[r][0]:
                temp_matrix[r_type] = True

        roleability_matrix[r] = temp_matrix

    return roleability_matrix


def get_input_availability(session, request_id):
    A = get_input_A(session, request_id)
    V = get_input_V(session)
    availability_matrix = np.full((V, A), True, dtype=bool)

    vehicle_list = get_vehicle_list(session, request_id)
    vehicle_time_list = []
    for v in vehicle_list:
        vehicle_time = get_vehicle_time(session, v)
        vehicle_time_list.append(vehicle_time)

    v_role_list = session.query(User.id).filter(User.role == "VOLUNTEER").all()

    for r in range(0, len(v_role_list)):
        temp_matrix = np.full(A, True, dtype=bool)
        user_id = v_role_list[r][0]
        unavailability_list = time_unavailability_list(session, user_id)
        for a in range(0, A):
            a_time = vehicle_time_list[a]
            for u_l in unavailability_list:
                user_unavailability = []
                user_unavailability.append(u_l[0])
                user_unavailability.append(u_l[1])
                periodicity = u_l[2]
                result = if_time_availability(user_unavailability, a_time, periodicity)
                if not result:
                    temp_matrix[a] = False
                    break
                else:
                    continue

        availability_matrix[r] = temp_matrix
    return availability_matrix


def time_unavailability_list(session, user_id):
    unavailability_list = session.query(UnavailabilityTime.start, UnavailabilityTime.end,
                                        UnavailabilityTime.periodicity).filter(
        UnavailabilityTime.userId == user_id and UnavailabilityTime.status == 1).all()
    # a list, each one is a tuple[(start,end),(start,end),peroid]
    return unavailability_list


def if_time_availability(user_unavailability, vehicle_time, periodicity):
    user_unavailability_start = user_unavailability[0]
    user_unavailability_end = user_unavailability[1]
    vehicle_time_start = vehicle_time[0]
    vehicle_time_end = vehicle_time[1]

    if vehicle_time_end < user_unavailability_start:
        return True

    if periodicity == 3:
        if user_unavailability_start <= vehicle_time_start <= user_unavailability_end:
            return False
        elif user_unavailability_start <= vehicle_time_end <= user_unavailability_end:
            return False
        elif vehicle_time_start <= user_unavailability_start and vehicle_time_end >= user_unavailability_end:
            return False
        elif vehicle_time_start >= user_unavailability_start and vehicle_time_end <= user_unavailability_end:
            return False
        else:
            return True

    elif periodicity == 2:
        while vehicle_time_start > user_unavailability_end:
            user_unavailability_start = user_unavailability_start + datetime.timedelta(weeks=1)
            user_unavailability_end = user_unavailability_end + datetime.timedelta(weeks=1)
        if user_unavailability_start <= vehicle_time_start <= user_unavailability_end:
            return False
        elif user_unavailability_start <= vehicle_time_end <= user_unavailability_end:
            return False
        elif vehicle_time_start <= user_unavailability_start and vehicle_time_end >= user_unavailability_end:
            return False
        elif vehicle_time_start >= user_unavailability_start and vehicle_time_end <= user_unavailability_end:
            return False
        else:
            return True

    elif periodicity == 1:
        while vehicle_time_start > user_unavailability_end:
            vehicle_time_start = vehicle_time_start + datetime.timedelta(days=1)
            vehicle_time_end = vehicle_time_end + datetime.timedelta(days=1)
            if user_unavailability_start <= vehicle_time_start <= user_unavailability_end:
                return False
            elif user_unavailability_start <= vehicle_time_end <= user_unavailability_end:
                return False
            elif vehicle_time_start <= user_unavailability_start and vehicle_time_end >= user_unavailability_end:
                return False
            elif vehicle_time_start >= user_unavailability_start and vehicle_time_end <= user_unavailability_end:
                return False
            else:
                return True
    else:
        return True


def get_input_clashes(session, request_id):
    A = get_input_A(session, request_id)
    clashes_matrix = np.full((A, A), False, dtype=bool)
    vehicle_list = get_vehicle_list(session, request_id)
    vehicle_time_list = []
    for v_id in vehicle_list:
        vehicle_time_list.append(get_vehicle_time(session, v_id))
    for a in range(0, A):
        for b in range(0, A):
            if a == b:
                continue
            else:
                result = if_clash(vehicle_time_list[a], vehicle_time_list[b])
                clashes_matrix[a][b] = result
    return clashes_matrix


def if_clash(first_time, second_time):
    first_time_start = first_time[0]
    first_time_end = first_time[1]
    second_name_start = second_time[0]
    second_time_end = second_time[1]

    if first_time_start <= second_name_start <= first_time_end:
        return True
    elif first_time_start <= second_time_end <= first_time_end:
        return True
    elif second_name_start <= first_time_start and second_time_end >= first_time_end:
        return True
    elif second_name_start >= first_time_start and second_time_end <= first_time_end:
        return True
    else:
        return False


def get_vehicle_time(session, vehicle_id):
    v_time = session.query(AssetRequestVehicle.from_date_time, AssetRequestVehicle.to_date_time).filter(
        AssetRequestVehicle.id == vehicle_id).first()
    start_time = v_time[0]
    end_time = v_time[1]
    vehicle_time = []
    vehicle_time.append(start_time)
    vehicle_time.append(end_time)
    return vehicle_time


def get_vehicle_list(session, request_id):
    vehicle_list = []
    asset_list = session.query(AssetRequestVehicle).filter(AssetRequestVehicle.request_id == request_id).all()
    for asset in asset_list:
        vehicle_list.append(asset.id)
    return vehicle_list


def get_position_list(session, vehicle_id):
    position_list = []
    vehicle_position_id = session.query(AssetRequestVolunteer).filter(
        AssetRequestVolunteer.vehicle_id == vehicle_id).all()
    for p in vehicle_position_id:
        position_list.append(p.id)
    return position_list


def get_position_list_all(session, request_id):
    request_position = []
    vehicle_list = get_vehicle_list(session, request_id)
    for v in vehicle_list:
        l = get_position_list(session, v)
        for n in l:
            request_position.append(n)
    request_position.sort()
    return request_position


def get_position_vehicle(session, position_id):
    vehicle = session.query(AssetRequestVolunteer.vehicle_id).filter(AssetRequestVolunteer.id == position_id).first()
    vehicle_id = vehicle[0]
    return vehicle_id


def get_position_role(session, position_id):
    role = session.query(AssetRequestVolunteer.role_id).filter(AssetRequestVolunteer.id == position_id).first()
    role_id = role[0]
    return role_id


def get_position_qualification(session, position_id):
    qualification = session.query(AssetRequestVolunteer.qualification_id).filter(AssetRequestVolunteer.id == position_id).first()
    qualification_id = qualification[0]
    return qualification_id


# This can be called by api from postman, to test easily
def test_vehicle_list(session, request_id):
    v_l = get_vehicle_list(session, request_id)
    for v in v_l:
        get_position_list(session, v)

    # print("get_postion_role", get_position_role(session,720))
    # print("get_APR_matrix", get_input_rolerequirements(session,361))
    # get_position_qualification(session,756)
    # print("get_APQ_matrix",get_input_qualrequirements(session,361))
    # print("get_position_list_all",get_position_list_all(session,360))
    # print("get_position_vehicle",get_position_vehicle(session,863))
    # print("get_posrequirements_matrix",get_input_posrequirements(session,360))
    # get_input_qualability(session)
    # print(get_qualification_list(session))
    # print(get_input_qualability(session))
    # get_role_list(session)
    # print(get_input_roleability(session))
    # print(get_vehicle_time(session,369))
    # print(get_input_availability(session,360))
    # print(time_unavailability_list(session,31))
    # print(get_input_availability(session,360))
    # print(get_input_clashes(session,323))

    return 1
