from domain import AssetRequestVehicle, Role, AssetRequestVolunteer, User, Qualification
from sqlalchemy import orm, func, alias
import numpy as np


def get_input_A(session, request_id):
    asset_list_count = session.query(AssetRequestVehicle).filter(AssetRequestVehicle.request_id == request_id).count()
    return asset_list_count

def get_input_R(session):
    role_list_count = session.query(Role).count()
    return role_list_count

def get_input_P(session,request_id):
    asset_list = session.query(AssetRequestVehicle.id).filter(AssetRequestVehicle.request_id == request_id).all()
    print(asset_list)
    position_count = 0
    for v_id in asset_list:
        asset_position_count = session.query(AssetRequestVolunteer).filter(AssetRequestVolunteer.vehicle_id == v_id[0]).count()
        print(asset_position_count)
        position_count += asset_position_count
    return position_count

def get_input_V(session):
    volunteer_list_count = session.query(User.role).filter(User.role == "VOLUNTEER").count()
    return volunteer_list_count

def get_input_Q(session):
    qualification_list_count = session.query(Qualification).count()
    return qualification_list_count

def get_input_qualrequirements(session,request_id):
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


def get_input_rolerequirements(session,request_id):
    A = get_input_A(session,request_id)
    P = get_input_P(session,request_id)
    R = get_input_R(session)
    rolerequirements_matrix = np.full((A,P,R),False,dtype=bool)
    vehicle_list = get_vehicle_list(session,request_id)
    mark = 0
    for a in range(0,A):
        position_list = get_position_list(session,vehicle_list[a])
        position_in_vehicle = len(position_list)
        for p in range(0,position_in_vehicle):
            role_id = get_position_role(session,position_list[p])
            for r in range(0,R):
                if r == role_id-1:
                    rolerequirements_matrix[a][p+mark][r] = True
                    break
                else:
                    continue
        mark += position_in_vehicle
    return rolerequirements_matrix

def get_input_posrequirements(session,request_id):
    A = get_input_A(session,request_id)
    P = get_input_P(session,request_id)
    vehicle_list = get_vehicle_list(session,request_id)
    posrequirements_matrix = np.full((P,A),False,dtype=bool)
    request_position = get_position_list_all(session,request_id)

    for p in range(0,len(request_position)):
        p_id = request_position[p]
        temp_matrix = np.full(A,False,dtype=bool)
        temp_asset = get_position_vehicle(session,p_id)
        for a in range (0,A):
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
    qualability_matrix = np.full((V,Q),False,dtype=bool)
    v_qualification_list = session.query(User.qualifications).filter(User.role == "VOLUNTEER").all()

    for q in range(0,len(v_qualification_list)):
        temp_matrix = np.full(Q, False, dtype=bool)
        for q_type in range(0,Q):
            if qualification_type[q_type] in v_qualification_list[q][0]:
                temp_matrix[q_type] = True

        qualability_matrix[q] = temp_matrix

    return qualability_matrix

def get_role_list(session):
    role_table = session.query(Role.name).all()
    role_type = []
    for i in role_table:
        role_type.append(i[0])
    print(role_type)
    return role_type


def get_input_roleability(session):
    V = get_input_V(session)
    R = get_input_R(session)

    role_type = get_role_list(session)
    roleability_matrix = np.full((V,R),False,dtype=bool)
    v_role_list = session.query(User.possibleRoles).filter(User.role == "VOLUNTEER").all()

    for r in range(0,len(v_role_list)):
        temp_matrix = np.full(R, False, dtype=bool)
        for r_type in range(0,R):
            if role_type[r_type] in v_role_list[r][0]:
                temp_matrix[r_type] = True

        roleability_matrix[r] = temp_matrix

    return roleability_matrix













def get_vehicle_list(session, request_id):
    vehicle_list=[]
    asset_list = session.query(AssetRequestVehicle).filter(AssetRequestVehicle.request_id == request_id).all()
    for asset in asset_list:
        vehicle_list.append(asset.id)
    return vehicle_list

def get_position_list(session,vehicle_id):
    position_list = []
    vehicle_position_id = session.query(AssetRequestVolunteer).filter(AssetRequestVolunteer.vehicle_id == vehicle_id).all()
    for p in vehicle_position_id:
        position_list.append(p.id)
    return position_list

def get_position_list_all(session,request_id):
    request_position = []
    vehicle_list = get_vehicle_list(session,request_id)
    for v in vehicle_list:
        l = get_position_list(session,v)
        for n in l:
            request_position.append(n)
            print(request_position)
    request_position.sort()
    return request_position

def get_position_vehicle(session,position_id):
    vehicle = session.query(AssetRequestVolunteer.vehicle_id).filter(AssetRequestVolunteer.id == position_id).first()
    vehicle_id = vehicle[0]
    return vehicle_id


def get_position_role(session,position_id):
    role = session.query(AssetRequestVolunteer.role_id).filter(AssetRequestVolunteer.id == position_id).first()
    role_id = role[0]
    return role_id

def get_position_qualification(session,position_id):
    role = session.query(AssetRequestVolunteer.qualification_id).filter(AssetRequestVolunteer.id == position_id).first()
    role_id = role[0]
    return role_id





def test_vehicle_list(session, request_id):
    v_l = get_vehicle_list(session,request_id)
    for v in v_l:
        get_position_list(session,v)

    #print("get_postion_role", get_position_role(session,720))
    #print("get_APR_matrix", get_input_rolerequirements(session,361))
    #get_position_qualification(session,756)
    #print("get_APQ_matrix",get_input_qualrequirements(session,361))
    #print("get_position_list_all",get_position_list_all(session,360))
    #print("get_position_vehicle",get_position_vehicle(session,863))
    #print("get_posrequirements_matrix",get_input_posrequirements(session,360))
    #get_input_qualability(session)
    #print(get_qualification_list(session))
    #print(get_input_qualability(session))
    #get_role_list(session)
    print(get_input_roleability(session))
    return 1














