import uuid

def generate_uuid():
    """
    Generate a unique UUID4 string.
    Returns a 32-char hex string without dashes.
    """
    return uuid.uuid4().hex
