from typing import Union

from elemental_tools.asserts import root_ref
from elemental_tools.pydantic import BaseModel, Field, EmailStr


class SMTPSchema(BaseModel):
    sub: str = Field(description="User Who Own the SMTP Configuration", default=root_ref())
    status: bool = Field(description="Status of the SMTP Configuration. True when it's working otherwise False.", default=False)
    server: str = Field(description='SMTP Server')
    port: int = Field(description='SMTP Server Port')
    email: EmailStr = Field(description='User email for google drive sharing and other stuff')
    password: str = Field(description='Password')

