from ..sanitize_exception import SanitizeException

class NoCIFMatchFoundException(SanitizeException):
    """Exception raised when no valid CIF is found in the text."""
    def __init__(self, cif):
        self.message = f"No valid CIF found in text: '{cif}'"
        super().__init__(self.message)

class InvalidCIFException(SanitizeException):
    """Exception raised when a CIF is syntactically correct but fails the validation check."""
    def __init__(self, cif):
        self.message = f"Invalid CIF detected: '{cif}'"
        super().__init__(self.message)
