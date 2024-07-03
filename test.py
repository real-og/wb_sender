import re
def extract_time_mins(input_string):
    time_pattern = r'\b(\d{1,2})\s*[:.-]?\s*(\d{2})\b'
    matches = re.findall(time_pattern, input_string)
    if matches:
        hour, minute = matches[0]
        # return f"{hour.zfill(2)}:{minute.zfill(2)}"
        return str(minute.zfill(2))
    else:
        return None
    

print(extract_time_mins('Вася и коля 12.11'))