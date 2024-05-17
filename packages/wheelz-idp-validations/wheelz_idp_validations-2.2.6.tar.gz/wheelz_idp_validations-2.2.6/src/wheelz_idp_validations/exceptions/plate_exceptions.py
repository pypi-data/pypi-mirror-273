from ..sanitize_exception import SanitizeException

class InvalidPlateException(SanitizeException):
    def __init__(self, text):
        self.message = f"No valid plate found in text: '{text}'"
        super().__init__(self.message)

class EmptyInputException(SanitizeException):
    def __init__(self, text):
        self.message = f"Empty input received for plate processing: '{text}'"
        super().__init__(self.message)
