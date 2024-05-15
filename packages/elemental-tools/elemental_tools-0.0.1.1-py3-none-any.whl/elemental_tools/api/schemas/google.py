from datetime import datetime
from typing import Union, Dict, List

from elemental_tools.asserts import root_ref
from elemental_tools.pydantic import BaseModel, Field, PyBaseModel
from elemental_tools.system import current_timestamp


class SheetStyle(PyBaseModel):
    background: str = "#000000"
    color: str = "#ffffff"


class GooglePermission(PyBaseModel):

    sub: Union[str, None] = Field(description='Id`s of the user that will have access to this doc', default_factory=root_ref)
    email: str = Field(description='The current email assigned to the permission of this sub. For later updates.', default=None)
    date: str = Field(description='A timestamp for the changes made to the doc', default_factory=current_timestamp)


class GoogleDriveFolder(PyBaseModel):

    folder_caption: str = Field(description='A string containing the Google Drive folder caption identifier', default=None)
    external_id: Union[str, None] = Field(description='Save the id for the current sheet', default=None)
    permissions: Union[list, None] = Field(description='A list containing the ids and emails of the users that already have access to this sheet', default=[])


class GoogleSheet(PyBaseModel):

    name: Union[str, None] = Field(description='A name for the sheet to ease identification', default=None)
    external_id: Union[str, None] = Field(description='Id for the current sheet', default=None)
    date: str = Field(description='A timestamp for the changes made to the doc', default_factory=current_timestamp)
    authorized_emails: list = Field(description='A list with the emails of the persons who can see this sheet.', default=[])


class GoogleInformation(PyBaseModel):

    sheets: Dict[str, GoogleSheet] = Field(description='Store the Year and the Id for each Google Sheet Already Created.', default={})
    sheets_permissions: List = Field(description='Save email list with the permissions to the sheets', default=[])
    drive: Dict[str, GoogleDriveFolder] = Field(description='Keeps ids for the folders where the user information is stored.', default={})
