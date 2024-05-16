from datetime import datetime

from elemental_tools.pydantic import BaseModel, Field
from elemental_tools.api.schemas.google import SheetStyle


class InstitutionSchema(BaseModel):
    tax_number: str = Field(description='Institution tax number known as CNPJ in Brazil')
    name: str = Field(description='Institution name')
    alias: str = Field(description='The name that will be used in user sheets', default=None)
    status: bool = Field(description='Institution status', default=False)
    website: str = Field(description='Website of the current institution', default=None)

    style: SheetStyle = Field(description='Save the style of the current institution', examples=[{'background': "#000000", 'color': "#ffffff"}], default=SheetStyle())


