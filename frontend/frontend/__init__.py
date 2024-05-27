from os import environ
from sys import path

from frontend.constants import PROJECT_PATH

# Add the project path to the system path
path.append(str(PROJECT_PATH))

# Load the environment variables from the .env file
dotenv = PROJECT_PATH / ".env"
if not dotenv.exists():
    dotenv = PROJECT_PATH.parent / ".env"

if dotenv.exists():
    lines = [
        x.split("=")
        for x in dotenv.read_text().split("\n")
        if not x.startswith("#") and x
    ]

    # Update the environment variables
    environ.update({x[0]: x[-1] for x in lines if len(x) > 1})
