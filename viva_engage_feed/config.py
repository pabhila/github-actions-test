"""Configuration loader for the Viva Engage Feed Extractor.

Reads settings from environment variables, optionally loading a .env file
via python-dotenv.
"""

import os

from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN: str = os.environ.get("ENGAGE_BEARER_TOKEN", "")
GROUP_ID: str = os.environ.get("ENGAGE_GROUP_ID", "")
OUTPUT_FILE: str = os.environ.get("OUTPUT_FILE", "feed_report.html")
