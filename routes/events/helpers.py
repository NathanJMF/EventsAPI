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
