class MinorException(Exception):
    """
    Exception raised for minor errors in the input.
    """
    
    def __init__(self, message : str = "Minor error occurred" , status_code : int = 400):
        """
        Constructor for MinorException class.
        Args:
            message (str): Message to be displayed.
            status_code (int): Status code to be returned.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __dict__(self):
        return {
            "message": self.message,
            "status_code": self.status_code
        }
