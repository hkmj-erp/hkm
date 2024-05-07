from datetime import datetime


def get_month_number(month_string):
    try:
        # Parse the month string to a datetime object using strptime
        # This will throw a ValueError if the input is not a valid month name
        month_dt = datetime.strptime(month_string, "%B")
        # Extract the month number from the datetime object
        return month_dt.month
    except ValueError:
        # If the input is not a valid month name, return None
        return None
