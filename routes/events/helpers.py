from database_system.core import basic_lookup


def validate_amount(current_amount):
    try:
        # Convert to float first to ensure it's a valid number
        float_amount = float(current_amount)

        # Check for exactly two decimal places
        if len(current_amount.split('.')[-1]) > 2:
            raise ValueError

        # Ensure non-negative and non-zero values
        if float_amount <= 0:
            raise ValueError

        return float_amount
    except (ValueError, AttributeError):
        raise ValueError("The amount must be a positive number with exactly two decimal places (e.g., '42.00').")


def check_large_withdrawal(conn, alert_flag, alert_codes, event_request_data):
    return alert_flag, alert_codes


def check_withdrawal_streak(conn, alert_flag, alert_codes, event_request_data):
    return alert_flag, alert_codes


def check_deposit_growth(conn, alert_flag, alert_codes, event_request_data):
    return alert_flag, alert_codes


def check_deposit_limit(conn, alert_flag, alert_codes, event_request_data):
    return alert_flag, alert_codes


def check_event_request_alerts(conn, event_request_data):
    withdraw_event_key = "withdraw"
    alert_flag = False
    alert_codes = []
    # Assumes that type will be "deposit" if it is not "withdraw" as request parser ensures correctness.
    # Function is less reusable because of this decision
    if event_request_data["type"] == withdraw_event_key:
        alert_flag, alert_codes = check_large_withdrawal(conn, alert_flag, alert_codes, event_request_data)
        alert_flag, alert_codes = check_withdrawal_streak(conn, alert_flag, alert_codes, event_request_data)
    else:
        alert_flag, alert_codes = check_deposit_growth(conn, alert_flag, alert_codes, event_request_data)
        alert_flag, alert_codes = check_deposit_limit(conn, alert_flag, alert_codes, event_request_data)
    return alert_flag, alert_codes


def check_user_exists(conn, user_id):
    current_user_result = get_user_by_id(conn, user_id)
    if current_user_result:
        return True
    return False


def get_user_by_id(conn, user_id):
    current_schema = "public"
    current_table = "users"
    primary_key_column = "user_id"
    query = (f"SELECT * "
             f"FROM {current_schema}.{current_table} "
             f"WHERE "
             f"{current_schema}.{current_table}.{primary_key_column} = %s")
    values = [user_id,]
    result = basic_lookup(conn, query, values=values)
    return result
