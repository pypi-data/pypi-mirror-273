from ..sanitize_exception import SanitizeException

class InvalidDateException(SanitizeException):
    def __init__(self, found_date):
        self.message = (f'Specified date does not match the format DD/MM/YYYY - Date Found: {found_date}')
        super().__init__(self.message)

class EmptyDateException(SanitizeException):
    def __init__(self, found_date):
        self.message = ("No date provided or input is empty")
        super().__init__(self.message)

