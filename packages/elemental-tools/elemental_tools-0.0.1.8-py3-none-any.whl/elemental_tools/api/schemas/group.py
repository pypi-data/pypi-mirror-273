from typing import Union, List

from elemental_tools.pydantic import UserRoles
from elemental_tools.pydantic import Field, BaseModel, PyBaseModel


class MembershipSchema(PyBaseModel):
    role: UserRoles = Field(description="Indicate User Role/Scope")
    user_ref: str = Field(description="User Reference")


class GroupSchema(BaseModel):
    sub: str = Field(description="Owner ID")
    tax_number: str = Field(description="Tax Number or CNPJ in Brazil")
    title: str = Field(description="Group Title")
    members: Union[List[MembershipSchema], list] = Field(description="Membership Information", default=[])
