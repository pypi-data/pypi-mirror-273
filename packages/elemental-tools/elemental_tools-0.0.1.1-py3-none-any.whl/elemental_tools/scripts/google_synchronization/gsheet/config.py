import os

from elemental_tools.settings import SettingController
from elemental_tools.asserts import root_ref
from elemental_tools.json import json_to_temp_file
from elemental_tools.logger import Logger
from elemental_tools.path import Relative

from google.oauth2.service_account import Credentials

relative = Relative(__file__).relative

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

__logger__ = Logger(app_name="scripts", owner="google-sync").log


try:
    settings = SettingController()

    credentials_as_file = json_to_temp_file(settings.google_api_credentials_json.get(sub=root_ref(), name="google_api_credentials_json"))

    google_credentials = Credentials.from_service_account_file(
        credentials_as_file,
        scopes=scopes
    )

    os.rmdir(os.path.dirname(credentials_as_file))

    __logger__("info-error", "Google credentials has been loaded.")
except Exception as e:
    __logger__("critical-error", str(e))
