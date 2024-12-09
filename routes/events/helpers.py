from database_system.core import basic_lookup, basic_write_dict


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


def check_large_withdrawal(alert_flag, alert_codes, event_request_data):
    large_withdrawal_boundary = 100
    large_withdrawal_alert_code = 1100
    if event_request_data["amount"] > large_withdrawal_boundary:
        alert_flag = True
        alert_codes.append(large_withdrawal_alert_code)
    return alert_flag, alert_codes


def check_withdrawal_streak(conn, alert_flag, alert_codes, event_request_data):
    schema_name = "public"
    table_name = "user_actions"
    foreign_key_column = "user_id"
    timestamp_column = "timestamp"
    type_column = "type"
    user_id = event_request_data["user_id"]
    withdrawal_key = "withdraw"
    withdrawal_streak_count_max = 3
    withdrawal_streak_alert_code = 30
    # Get the last 3 user actions
    query = (f"SELECT {schema_name}.{table_name}.{type_column} "
             f"FROM {schema_name}.{table_name} "
             f"WHERE "
             f"{schema_name}.{table_name}.{foreign_key_column} = %s "
             f"ORDER BY {schema_name}.{table_name}.{timestamp_column} DESC "
             f"LIMIT {withdrawal_streak_count_max}")
    values = [user_id,]
    user_actions = basic_lookup(conn, query, values=values)
    # Leaves if there are less than 3 user actions
    if len(user_actions) < withdrawal_streak_count_max:
        return alert_flag, alert_codes
    # Uses list comprehension to quickly check if the last 3 actions are withdrawals
    if all(current_action["type"] == withdrawal_key for current_action in user_actions):
        alert_flag = True
        alert_codes.append(withdrawal_streak_alert_code)

    return alert_flag, alert_codes


def check_deposit_growth(conn, alert_flag, alert_codes, event_request_data):
    schema_name = "public"
    table_name = "user_actions"
    foreign_key_column = "user_id"
    type_column = "type"
    amount_column = "amount"
    timestamp_column = "timestamp"
    deposit_key = "deposit"
    growth_count = 3
    growth_alert_code = 300
    # Query to fetch the last 3 deposits for the user
    query = (f"SELECT {schema_name}.{table_name}.{amount_column} "
             f"FROM {schema_name}.{table_name} "
             f"WHERE "
             f"{schema_name}.{table_name}.{foreign_key_column} = %s AND "
             f"{schema_name}.{table_name}.{type_column} = %s "
             f"ORDER BY {schema_name}.{table_name}.{timestamp_column} DESC "
             f"LIMIT {growth_count}")
    values = [event_request_data["user_id"], deposit_key]
    user_actions = basic_lookup(conn, query, values=values)
    # Return early if fewer than 3 deposits exist
    if len(user_actions) < growth_count:
        return alert_flag, alert_codes
    # Check if each deposit is larger than the previous one
    if all(user_actions[count]["amount"] > user_actions[count + 1]["amount"] for count in range(len(user_actions) - 1)):
        alert_flag = True
        alert_codes.append(growth_alert_code)
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
        alert_flag, alert_codes = check_large_withdrawal(alert_flag, alert_codes, event_request_data)
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


def write_user_action(conn, user_id, action_type, amount, timestamp):
    schema_name = "public"
    table_name = "user_actions"
    primary_key_column = "action_id"
    data_dict = {
        "user_id": user_id,
        "type": action_type,
        "amount": amount,
        "timestamp": timestamp,
    }
    new_entry_id = basic_write_dict(
        conn,
        schema_name,
        table_name,
        data_dict,
        primary_key_column=primary_key_column,
        return_id=True
    )
    return new_entry_id
