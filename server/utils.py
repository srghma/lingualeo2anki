from .config import config

def debug(str, *args):
    if config.debug:
        print("DEBUG: ", str % args)
