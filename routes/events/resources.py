from flask import jsonify, make_response
from flask_restful import Resource, abort
from database_system.core import get_connection
from routes.events.helpers import check_event_request_alerts, check_user_exists
from routes.events.serialisers import get_event_request_parser


class EventsResource(Resource):
    def post(self):
        event_request_parser = get_event_request_parser()
        event_request_data = event_request_parser.parse_args()
        user_id = event_request_data["user_id"]

        conn = get_connection()
        # Check if the current user exists
        if not check_user_exists(conn, user_id):
            conn.close()
            no_user_message = "The user with the specified ID does not exist in the system."
            abort(404, message=no_user_message)

        alert_flag, alert_codes = check_event_request_alerts(conn, event_request_data)

        conn.close()
        # Built out response object
        response_dict_object = {
            "alert": alert_flag,
            "alert_codes": alert_codes,
            "user_id": user_id
        }
        response_json_object = jsonify(response_dict_object)
        return make_response(response_json_object, 200)
