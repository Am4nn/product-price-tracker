"""
Utility to check for required environment variables and configuration.
"""
from dotenv import load_dotenv
load_dotenv()  # loads .env variables
import os
import sys
import logging

def check_required_envs(required_vars):
    """
    Checks if all required environment variables are set.
    If any are missing, logs error and exits.
    """
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logging.error(f"Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)
    else:
        logging.info("All required environment variables are set.")

def get_env_var(name, default=""):
    return os.getenv(name, default)
