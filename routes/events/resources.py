from flask import jsonify, make_response
from flask_restful import Resource, abort
from routes.events.serialisers import get_event_request_parser


class EventsResource(Resource):
    def post(self):
        event_request_parser = get_event_request_parser()
        event_request_data = event_request_parser.parse_args()
        print(event_request_data)
        return make_response(jsonify({"message": "Endpoint is active"}), 200)
