from typing import Union

from pydantic import Field

from elemental_tools.asserts import DefaultTax
from elemental_tools.pydantic import BaseModel



class StatementSchema(BaseModel,  arbitrary_types_allowed=True):
    sub: Union[str, None] = Field(description='User ref for the current statement registration', default=None)
    status: bool = Field(description='Indicates whenever this statement register must be exported or not. True value will bypass the Statement Google Sync for this register.', default=False)
    tax: float = Field(description='Set tax for user transactions', default_factory=DefaultTax(sub=sub))

