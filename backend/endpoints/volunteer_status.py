# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
import re, json
from includes.main import contains
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close


'''
Define Data Input
{
    idVolunteer: String
    idVehicle: String
    Status: String 
}

'''

parser = reqparse.RequestParser()
parser.add_argument('idVolunteer', action='store', type=str) # unsure about this line
parser.add_argument('idVehicle', action='store', type=str)
parser.add_argument('status', action='store', type=str)


'''
Define Data Output

{
    success: boolean
}
'''

resource_fields = {
    'success': fields.Boolean,
}


class VolunteerStatus(Resource):

    @marshal_with(resource_fields)
    def patch(self):

        args = parser.parse_args()
        if (args["idVolunteer"] is None or args["idVehicle"] is None or args["status"] is None):
            return { "success": False }
        
        idVolunteer = args['idVolunteer']
        idVehicle = args['idVehicle']
        status = args['status']
        print(idVolunteer, idVehicle, status) # testing line

        # TODO
        # write the mysql to update the 'status' field in the asset-request-volunteer who has .idVolunteer = idVolunteer AND .idVehicle = idVehicle

        return { "success": False }