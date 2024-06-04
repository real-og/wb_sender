import re
def get_time(text):
    regex = r"\b([01]?[0-9]|2[0-3]):([0-5][0-9])(?::([0-9][0-9]))?\b"

    groups = re.findall(regex, text)
    return groups

print(get_time('Время заказа 10:34,девочка, Степанида.'))