# Flask
from flask import Flask
from flask_restful import reqparse, abort, Resource, fields, marshal_with, inputs
# Helpers
from endpoints.helpers.input_validation import *

'''
Define Data Input - from query parameters

Comparitors
gt:greater than
lt:less than
gte:greater than or equal to
lte:less than or equal to
eq:equal to

# Most important
?endTime
?startTime
# Less important
?assetClass

?sort_by=String (key probably firstName)
?order_by=String [desc | asc]
?results_num=Integer (number of results that can fit on a page)
?page_num=Integer Default=1
'''

# Generate the parameters for each filter comparator
def generate_filter_argument(parameter, comparators, parser, type_function):
    for comparator in comparators:
        parser.add_argument(parameter + '[' + comparator + ']', action='store', type=type_function, store_missing=True)
    return parser

# Split args and their filter comparison
# Returns pairs of [parameter, comparator string]
def split_filter_comparison(args):
    filter_args = []
    for arg in args:
        # Separate the parameter and comparator
        arg_split = arg.split('[')
        # Ignore parameters without a comparator
        if len(arg_split) is 2:
            # Remove the last ']'
            arg_split[1] = arg_split[1][:-1]
            # Store the filter parameter
            filter_args.append(arg_split)
    return filter_args

parser = reqparse.RequestParser()
# Define search criteria parameters
parser = generate_filter_argument('startTime', ['gt','lt'], parser, inputs.datetime_from_iso8601)
parser = generate_filter_argument('endTime', ['gt','lt'], parser, inputs.datetime_from_iso8601)

parser.add_argument('volunteerID', action='store', type=str)
# Define ordering, sorting, retrieval parameters
parser.add_argument('sort_by', action='store', type=str, choices=('startTime', 'endTime'), default='startTime')
parser.add_argument('order_by', action='store', type=str, choices=('desc','asc'), default='desc')
parser.add_argument('results_num', action='store', type=int)
parser.add_argument('page_num', action='store', type=int, default=1)

'''
Define Data Output

{
    "results" : [{
        "shiftID": Integer,
        "assetClass": String, [lightUnit | mediumTanker | heavyTanker]
        "startTime": DateTimeString,
        "endTime": DateTimeString,
        "volunteers": [{
            "ID": String,
            "positionID": Integer,
            "role": [String], [basic | advanced | crewLeader | driver]
        }]
    }]

}
'''

volunteer_field = {
    'ID': fields.String,
    'positionID': fields.Integer,
    'role': fields.List(fields.String)
}

shift_list_field = {
    'shiftID': fields.String,
    'assetClass': fields.String,
    'startTime': fields.DateTime(dt_format='iso8601'),
    'endTime': fields.DateTime(dt_format='iso8601'),
    'volunteers': fields.List(fields.Nested(volunteer_field))
}

resource_fields = {
    'results': fields.List(fields.Nested(shift_list_field)),
}

# Handle the Recommendation endpoint
class VolunteerShifts(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        if args['volunteerID'] is None:
            raise ValueError('VolunteerID was not provided')
        filter_args = split_filter_comparison(args)
        print(args)


        # Get the ordering, sorting, retrieval parameters
        sort_by = args['sort_by']
        order_by = args['order_by']
        page_num = args['page_num']
        results_num = args['results_num']
        if results_num is None:
            limit_results = False
        else:
            limit_results = True

        # TODO based on parameters get shifts for a volunteer

        # Return the results
        output = []
        return { 'results': output }
