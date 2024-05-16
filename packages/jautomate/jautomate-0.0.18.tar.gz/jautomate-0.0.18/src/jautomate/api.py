"""
Handles creating instances of the Classic and Pro APIs for
Jamf using dotenv to store the credentials.
"""
import os

from dotenv import load_dotenv
from jps_api_wrapper.classic import Classic
from jps_api_wrapper.pro import Pro

load_dotenv()

jamf_p = Pro(
    os.getenv('JPS_URL'),
    os.getenv('JPS_USERNAME'),
    os.getenv('JPS_PASSWORD')
)

jamf_c = Classic(
    os.getenv('JPS_URL'),
    os.getenv('JPS_USERNAME'),
    os.getenv('JPS_PASSWORD')
)
