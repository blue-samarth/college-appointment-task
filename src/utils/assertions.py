from .exception import MinorException

def base_assertion(condition : bool, message : str = "Assertion failed", status_code : int = 400):
    """
    Function to assert a condition and raise an exception if it fails.
    Args:
        condition (bool): Condition to be asserted.
        message (str): Message to be displayed.
        status_code (int): Status code to be returned.
    """
    if not condition:
        raise MinorException(message, status_code)
    

def assert_not_found(condition : bool, message : str = "Resource not found"):
    """
    Function to assert a condition and raise an exception if it fails.
    Args:
        condition (bool): Condition to be asserted.
        message (str): Message to be displayed.
    """
    base_assertion(condition, message, 404)


def assert_auth(condition : bool, message : str = "Authentication failed"):
    """
    Function to assert a condition and raise an exception if it fails.
    Args:
        condition (bool): Condition to be asserted.
        message (str): Message to be displayed.
    """
    base_assertion(condition, message, 401)


def assert_bad_request(condition : bool, message : str = "Bad request"):
    """
    Function to assert a condition and raise an exception if it fails.
    Args:
        condition (bool): Condition to be asserted.
        message (str): Message to be displayed.
    """
    base_assertion(condition, message, 400)


# if the user tries to access a resource that is taken by another user
def assert_conflict(condition : bool, message : str = "Conflict"):
    """
    Function to assert a condition and raise an exception if it fails.
    Args:
        condition (bool): Condition to be asserted.
        message (str): Message to be displayed.
    """
    base_assertion(condition, message, 409)