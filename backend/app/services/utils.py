import re

def valid_phone_number(phone_string: str):
    regex = r"^[0-9]{9,15}$"
    if not re.search(regex, phone_string, re.I):
        return False
    return True