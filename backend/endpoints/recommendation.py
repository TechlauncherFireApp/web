from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with


# Dictionary Object returned from Back-End
# {
#     volunteer_list : [{
#           asset_id: Integer,
#           asset_class: Enum,
#           start_time: TimeBlock,
#           end_time: TimeBlock,
#           position: [{
#               position_id: Integer,
#               role: driver | advanced | basic,
#               qualifications: String
#           }],
#           volunteers: [{
#               volunteer_id: Integer,
#               position_id: Integer,
#               volunteer_name: String,
#               role: driver | advanced | basic,
#               qualifications: String,
#               contact Info: [{
#                   type: email | phone,
#                   detail: email_add | phone_no
#               }]
#           }]
#     }]
# }

TimeBlock = fields.Integer

position_field = {
    'position_id': fields.Integer,
    'role': fields.String,
    'qualifications': fields.String,
}

volunteer_field = {
    'volunteer_id': fields.Integer,
    'position_id': fields.Integer,
    'volunteer_name': fields.String,
    'role': fields.String,
    'qualifications': fields.String,
    'contact_info': fields.List(fields.Nested({
        'type': fields.String,
        'detail': fields.String,
    }))
}

volunteer_list_field = {
    'asset_id': fields.Integer,
    'asset_class': fields.String,
    'start_time': TimeBlock,
    'end_time': TimeBlock,
    'position': fields.List(fields.Nested(position_field)),
    'volunteers': fields.List(fields.Nested(volunteer_field)),
}

resource_fields = {
    'volunteer_list': fields.List(fields.Nested(volunteer_list_field)),
}

class Recommendation(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return_data = {
            'asset_id': 1,
            'asset_class': "Heavy",
            'start_time': 24,
            'end_time': 36,
            'position': [{
                'position_id': 1,
                'role': "driver",
                'qualifications': ""
            },{
                'position_id': 2,
                'role': "advanced",
                'qualifications': ""
            },{
                'position_id': 3,
                'role': "advanced",
                'qualifications': ""
            },{
                'position_id': 4,
                'role': "basic",
                'qualifications': ""
            }],
            'volunteers': [{
                'volunteer_id': 12,
                'position_id': 1,
                'volunteer_name': "Random Name",
                'role': "driver",
                'qualifications': "",
                'contact_info': [{
                    'type': "phone",
                    'detail': "0411 111 111"
                }]
                },{
                'volunteer_id': 13,
                'position_id': 2,
                'volunteer_name': "Random Name",
                'role': "advanced",
                'qualifications': "",
                'contact_info': [{
                    'type': "phone",
                    'detail': "0411 111 111"
                }]
                },{
                'volunteer_id': 92,
                'position_id': 3,
                'volunteer_name': "Random Name",
                'role': "advanced",
                'qualifications': "",
                'contact_info': [{
                    'type': "phone",
                    'detail': "0411 111 111"
                }]
                },{
                'volunteer_id': 8,
                'position_id': 4,
                'volunteer_name': "Random Name",
                'role': "basic",
                'qualifications': "",
                'contact_info': [{
                    'type': "phone",
                    'detail': "0411 111 111"
                }]
            }]
        }
        return {"volunteer_list" : [return_data]}