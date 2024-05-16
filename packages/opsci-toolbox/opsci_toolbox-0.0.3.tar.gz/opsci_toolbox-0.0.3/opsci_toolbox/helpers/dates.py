from datetime import datetime, timezone
import pandas as pd

def get_now():
    return datetime.now(timezone.utc)

def str_to_datetime(date_string, format = "%a %b %d %H:%M:%S %z %Y"):
    # Facebook Format : "2024-02-13T15:20:23+0000" = "%Y-%m-%dT%H:%M:%S%z"
    # Youtube : '1970-01-01T00:00:00Z' = "%Y-%m-%dT%H:%M:%SZ" 
    # Twitter RapidAPI : '%a %b %d %H:%M:%S %z %Y'
    try:
        formated_date = datetime.strptime(date_string, format)
        return formated_date
    except Exception as e:
        pass
        print(e)
        return date_string


def datetime_to_str(date, date_format = '%Y-%m-%dT%H:%M:%SZ'):
    return date.strftime(date_format)

def number_of_days(start_date, end_date):
    # Calculate the difference
    time_difference = start_date - end_date
    # Extract the number of days from the timedelta object
    days_difference = time_difference.days
    return days_difference

def df_col_to_datetime(df, col):
    df[col] = pd.to_datetime(df[col])
    return df

