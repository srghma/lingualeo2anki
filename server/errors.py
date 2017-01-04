class Error(Exception):
    """Base class for exceptions in this package."""
    pass


class InvalidInterceptionError(Error):
    """docstring for InvalidInterceptionError"""

    def __init__(self, message, rawbody):
        self.message = message
        self.rawbody = rawbody
