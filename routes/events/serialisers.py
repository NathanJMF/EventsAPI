from flask_restful import reqparse
from routes.events.helpers import validate_amount


def get_event_request_parser():
    event_request_parser = reqparse.RequestParser()

    event_request_parser.add_argument(
        "type",
        type=str,
        required=True,
        choices=("deposit", "withdraw"),
        help="The type of user action is required and must be either 'deposit' or 'withdraw'."
    )

    event_request_parser.add_argument(
        "amount",
        type=validate_amount,
        required=True,
        help="The amount for the user action is required. It must be a positive number in string format e.g., '42.00'."
    )

    event_request_parser.add_argument(
        "user_id",
        type=int,
        required=True,
        help="The user ID is required and must be an integer identifying the user."
    )

    event_request_parser.add_argument(
        "time",
        type=int,
        required=True,
        help="The timestamp is required and must be an integer representing the time of the action."
    )

    return event_request_parser
