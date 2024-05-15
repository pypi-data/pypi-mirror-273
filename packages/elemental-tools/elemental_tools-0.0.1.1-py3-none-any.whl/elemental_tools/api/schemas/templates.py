from typing import Optional, Union, List

from fastapi import UploadFile

from elemental_tools.api.schemas.user import UserSchema
from elemental_tools.exceptions import Invalid
from elemental_tools.pydantic import BaseModel, Field, field_validator


class TemplateResourceModifiers(BaseModel):
    title: str = Field(description='Modifier Title')
    content: str = Field(description='Modifier Text or HTML Content')

    @classmethod
    @field_validator("title")
    def validate_title(cls, title):
        if len(str(title)) >= 1:
            return title
        else:
            raise Invalid("title", message="Invalid Resource Title")

    @classmethod
    @field_validator("content")
    def validate_content(cls, content):
        if content is None:
            return None
        elif len(str(content)) >= 1:
            return content
        else:
            raise Invalid("content", message="Resource Content Too Short")


class TemplateResourceSchema(BaseModel):
    sub: Union[str, None] = Field(description='Resource Owner Id', default=None)
    status: Union[bool, None] = Field(description='Resource Status', default=True)
    title: str = Field(description='Resource Title')
    personal: Optional[bool] = Field(description="Indicates whenever the resource is shared with the siblings users", default=True)
    content: Union[str, None] = Field(description='Resource Text or HTML Content', default=None)
    icon: Union[UploadFile, None] = Field(description="Icon file or url to upload and store as resource icon", default=None)
    editable: Optional[bool] = Field(description="Indicates whenever the resource is editable by users", default=True)
    modifiers: Union[List[TemplateResourceModifiers], None] = Field(description="Store the modifiers for the current resource", default_factory=list, examples=[[{"title": "This Modifier", "content": ""}]])

    @classmethod
    @field_validator('modifiers')
    def valid_modifiers(cls, mods: list):
        result = []

        for mod in mods:

            if not isinstance(mod, TemplateResourceModifiers):
                mod = TemplateResourceModifiers(**mod)

            if mod.ref not in [md.ref for md in result]:
                result.append(mod)

        return result


class TemplateSchema(BaseModel,  arbitrary_types_allowed=True):
    sub: Union[str, None] = Field(description='Template User Owner', default=None)
    status: Union[bool, None] = Field(description='Template Status', default=False)
    content: Union[str, None] = Field(description='Template Text or HTML Content', default=None)
    subject: Union[str, None] = Field(description='Template Subject', default=None)
    title: Union[str, None] = Field(description='Template Title', default=None)
    type: str = Field(description='Template Type', default='personal')
    variables: Union[dict, None] = Field(description='Template available variables.', default={key: None for key in UserSchema.model_fields.keys()})
    resources: list = Field(description='Template resources.', default=[])

