from os import environ

ENVIRONMENT = environ.get("ENVIRONMENT", "").upper()

if ENVIRONMENT not in ("PROD", "DEV"):
    raise Exception("Please set the environment variable to either DEV or PROD")
