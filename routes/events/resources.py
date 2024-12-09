from flask import jsonify, make_response
from flask_restful import Resource
from routes.events.helpers import check_event_request_alerts
from routes.events.serialisers import get_event_request_parser


class EventsResource(Resource):
    def post(self):
        event_request_parser = get_event_request_parser()
        event_request_data = event_request_parser.parse_args()
        user_id = event_request_data["user_id"]
        alert_flag, alert_codes = check_event_request_alerts(event_request_data)
        # Built out response object
        response_dict_object = {
            "alert": alert_flag,
            "alert_codes": alert_codes,
            "user_id": user_id
        }
        response_json_object = jsonify(response_dict_object)
        return make_response(response_json_object, 200)
