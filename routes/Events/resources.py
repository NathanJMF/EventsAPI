from flask import jsonify, make_response
from flask_restful import Resource, abort


class EventsResource(Resource):
    def post(self):
        return make_response(jsonify({"message": "Endpoint is active"}), 200)
