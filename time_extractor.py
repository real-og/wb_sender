import re
import time
from datetime import datetime


def get_minutes_from_str(iso_string):
    dt = datetime.datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%SZ")
    minutes = dt.minute
    return  minutes


def current_unix_timestamp():
    return int(time.time())


def get_unix_from_str(time_str):
    dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
    return int(dt.timestamp())


def extract_time_mins(input_string):
    time_pattern = r'\b(\d{1,2})\s*[:.-]?\s*(\d{2})\b'
    matches = re.findall(time_pattern, input_string)
    if matches:
        hour, minute = matches[0]
        # return f"{hour.zfill(2)}:{minute.zfill(2)}"
        return str(minute.zfill(2))
    else:
        return None
    