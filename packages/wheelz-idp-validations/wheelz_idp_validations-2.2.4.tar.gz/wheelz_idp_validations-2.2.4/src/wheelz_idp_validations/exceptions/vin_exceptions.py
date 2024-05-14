from ..sanitize_exception import SanitizeException

class InvalidVinException(SanitizeException):
    def __init__(self, vin):
        self.message = (f'No valid VIN found in text: {vin}')
        super().__init__(self.message)
