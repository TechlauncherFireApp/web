# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json
# Mysql
#from querys.volunteer import volunteer
from includes.main import contains
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close
from querys.volunteer import availabilitiesToDateTime



'''
Define Data Input
 {
     volunteerID: String
 }

'''

parser = reqparse.RequestParser()
parser.add_argument('volunteerID', action='store', type=str)


'''
Define Data Output

get every: asset-request_volunteer.idVolunteer == volunteerID
need data from four different tables in database
{
    "results" : [{
        "requestTitle":     String      (asset-request.title)
        "vehicleID":        String      (asset-request_vehicle.id)
        "vehicleType":      String      (vehicle.type)
        "vehicleFrom":      DateTimeString iso8601      (asset-request_vehicle.from)
        "vehicleTo":        DateTimeString iso8601      (asset-request_vehicle.to)
        "volunteerRoles":   [String]    (asset-request_volunteer.roles)
        "volunteerStatus":  String      (asset-request_volunteer.status)
    }]
}
'''

result_list_field = {
    'requestTitle': fields.String,
    'vehicleID': fields.String,
    'vehicleType': fields.String,
    'vehicleFrom': fields.DateTime(dt_format='iso8601'),
    'vehicleTo': fields.DateTime(dt_format='iso8601'),
    'volunteerRoles': fields.List(fields.String),
    'volunteerStatus': fields.String,
}

resource_fields = {
    'results': fields.List(fields.Nested(result_list_field)),
}


# Handle the volunteer/shifts endpoint
class VolunteerShifts(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        if args["volunteerID"] is None:
            return { "success": False }
        volunteerID = args["volunteerID"]

        conn = connection()
        if is_connected(conn):
            cur = conn.cursor(prepared=True)
            try:
                q = re.sub("\s\s+", " ", """
                    SELECT DISTINCT
                        ar.`title` AS `requestTitle`,
                        arv.`id` AS `vehicleID`, arv.`type` AS `vehicleType`,
                        arv.`from` AS `vehicleFrom`, arv.`to` AS `vehicleTo`,
                        arp.`roles` AS `volunteerRoles`, arp.`status` AS `volunteerStatus`
                    FROM
                        `asset-request_volunteer` AS arp
                        INNER JOIN `asset-request_vehicle` AS arv ON arp.`idVehicle` = arv.`id`
                        INNER JOIN `asset-request` AS ar ON arv.`idRequest` = ar.`id`
                    WHERE
                        `idVolunteer` = %s;
                """)

                cur.execute(q, [volunteerID])
                res = [dict(zip(cur.column_names, r)) for r in cur.fetchall()]
                o = []
                for r in res:
                    r["volunteerRoles"] = json.loads(r["volunteerRoles"])
                    o.append(r)
                print(o)
                if contains(o):
                    cur_conn_close(cur, conn)
                    return { "success": True, "results": o }
                cur_conn_close(cur, conn)
            except Exception as e:
                cur_conn_close(cur, conn)
                print (str(e))

        return {"success": False}


















# # Flask
# from flask import Flask
# from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
# # Helpers
# from endpoints.helpers.input_validation import *

# '''
# Define Data Input - from query parameters

# Comparitors
# gt:greater than
# lt:less than
# gte:greater than or equal to
# lte:less than or equal to
# eq:equal to

# # Most important
# ?endTime
# ?startTime
# # Less important
# ?assetClass

# ?sort_by=String (key probably firstName)
# ?order_by=String [desc | asc]
# ?results_num=Integer (number of results that can fit on a page)
# ?page_num=Integer Default=1
# '''

# # Generate the parameters for each filter comparator
# def generate_filter_argument(parameter, comparators, parser, type_function):
#     for comparator in comparators:
#         parser.add_argument(parameter + '[' + comparator + ']', action='store', type=type_function, store_missing=True)
#     return parser

# # Split args and their filter comparison
# # Returns pairs of [parameter, comparator string]
# def split_filter_comparison(args):
#     filter_args = []
#     for arg in args:
#         # Separate the parameter and comparator
#         arg_split = arg.split('[')
#         # Ignore parameters without a comparator
#         if len(arg_split) is 2:
#             # Remove the last ']'
#             arg_split[1] = arg_split[1][:-1]
#             # Store the filter parameter
#             filter_args.append(arg_split)
#     return filter_args

# parser = reqparse.RequestParser()
# # Define search criteria parameters
# parser = generate_filter_argument('startTime', ['gt','lt'], parser, inputs.datetime_from_iso8601)
# parser = generate_filter_argument('endTime', ['gt','lt'], parser, inputs.datetime_from_iso8601)

# parser.add_argument('volunteerID', action='store', type=str)
# # Define ordering, sorting, retrieval parameters
# parser.add_argument('sort_by', action='store', type=str, choices=('startTime', 'endTime'), default='startTime')
# parser.add_argument('order_by', action='store', type=str, choices=('desc','asc'), default='desc')
# parser.add_argument('results_num', action='store', type=int)
# parser.add_argument('page_num', action='store', type=int, default=1)

# '''
# Define Data Output

# {
#     "results" : [{
#         "shiftID": Integer,
#         "assetClass": String, [lightUnit | mediumTanker | heavyTanker]
#         "startTime": DateTimeString,
#         "endTime": DateTimeString,
#         "volunteers": [{
#             "ID": String,
#             "positionID": Integer,
#             "role": [String], [basic | advanced | crewLeader | driver]
#         }]
#     }]

# }
# '''

# volunteer_field = {
#     'ID': fields.String,
#     'positionID': fields.Integer,
#     'role': fields.List(fields.String)
# }

# shift_list_field = {
#     'shiftID': fields.String,
#     'assetClass': fields.String,
#     'startTime': fields.DateTime(dt_format='iso8601'),
#     'endTime': fields.DateTime(dt_format='iso8601'),
#     'volunteers': fields.List(fields.Nested(volunteer_field))
# }

# resource_fields = {
#     'results': fields.List(fields.Nested(shift_list_field)),
# }

# # Handle the Recommendation endpoint
# class VolunteerShifts(Resource):
#     @marshal_with(resource_fields)
#     def get(self):
#         args = parser.parse_args()
#         if args['volunteerID'] is None:
#             raise ValueError('VolunteerID was not provided')
#         filter_args = split_filter_comparison(args)
#         print(args)


#         # Get the ordering, sorting, retrieval parameters
#         sort_by = args['sort_by']
#         order_by = args['order_by']
#         page_num = args['page_num']
#         results_num = args['results_num']
#         if results_num is None:
#             limit_results = False
#         else:
#             limit_results = True

#         # TODO based on parameters get shifts for a volunteer

#         # Return the results
#         output = []
#         return { 'results': output }
