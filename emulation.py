import os

def active():
    return True if os.getenv("KBOOTH_EMULATE") else False
