# from elemental_tools.api.schemas.google import GoogleInformation, SheetStyle
# from elemental_tools.api.schemas.smtp import SMTPSchema
# from elemental_tools.api.schemas.user import UserSchema, UserCompany, UserInstitutionSetting, UserSonSchema
from elemental_tools.pydantic import BaseModel, PyBaseModel, Field


class ResponseMessage(PyBaseModel):

    message: str = Field()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

