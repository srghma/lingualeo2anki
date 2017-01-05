class Error(Exception):
    """Base class for exceptions in this package."""
    pass


class InvalidInterceptionError(Error):
    """docstring for InvalidInterceptionError"""

    def __init__(self, message):
        self.message = message


class DigError(Error):
    """for dig method in utils"""

    def __init__(self, dictionary, key):
        self.dictionary = dictionary
        self.key = key
