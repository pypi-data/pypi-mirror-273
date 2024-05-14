import re
from ..exceptions.gender_exceptions import *

def sanitize_gender(received_gender):
    # Use regex to find an 'M' or 'F' anywhere in the string
    match = re.search(r'\b[MF]\b', received_gender)

    if not match:
        # If no standalone 'M' or 'F' is found, try finding 'M' or 'F' surrounded by other characters
        match = re.search(r'[MF]', received_gender)
        if not match:
            # If still not found, raise an exception
            raise InvalidGenderException(received_gender)

    return match.group()
