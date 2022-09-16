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
    print(qualrequirements_matrix)
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
    print(rolerequirements_matrix)
    return rolerequirements_matrix


def get_vehicle_list(session, request_id):
    vehicle_list=[]
    asset_list = session.query(AssetRequestVehicle).filter(AssetRequestVehicle.request_id == request_id).all()
    for asset in asset_list:
        vehicle_list.append(asset.id)
    print(vehicle_list)
    return vehicle_list

def get_position_list(session,vehicle_id):
    position_list = []
    vehicle_position_id = session.query(AssetRequestVolunteer).filter(AssetRequestVolunteer.vehicle_id == vehicle_id).all()
    for p in vehicle_position_id:
        position_list.append(p.id)
    print(position_list)
    return position_list

def get_position_role(session,position_id):
    role = session.query(AssetRequestVolunteer.role_id).filter(AssetRequestVolunteer.id == position_id).first()
    role_id = role[0]
    return role_id

def get_position_qualification(session,position_id):
    role = session.query(AssetRequestVolunteer.qualification_id).filter(AssetRequestVolunteer.id == position_id).first()
    role_id = role[0]
    print(role_id)
    return role_id





def test_vehicle_list(session, request_id):
    v_l = get_vehicle_list(session,request_id)
    for v in v_l:
        get_position_list(session,v)

    #print("get_postion_role", get_position_role(session,720))
    #print("get_APR_matrix", get_input_rolerequirements(session,361))
    #get_position_qualification(session,756)
    #print("get_APQ_matrix",get_input_qualrequirements(session,361))
    return 1














