from typing import List

from pydantic import field_validator

from elemental_tools.api.orm.user import TableUser
from elemental_tools.api.schemas.templates import TemplateResourceModifiers, TemplateResourceSchema
from elemental_tools.api.schemas.user import UserSchema
from elemental_tools.db import ForeignKey, Mapped, Column, JSONColumn, String, Boolean
from elemental_tools.db.constraints import constraint_unique
from elemental_tools.db.orm import SQLModel, relationship, AppendableTableArgs


class TableTemplateResource(SQLModel):
    __tablename__ = 'template_resource'

    sub: Mapped[str] = Column(String, ForeignKey(TableUser.ref), default=None)

    title: Mapped[str] = Column(String, nullable=False)
    personal: Mapped[bool] = Column(Boolean, server_default='true')
    content: Mapped[str] = Column(String, default=None)
    icon: Mapped[bytes] = Column(String, default=None)
    editable: Mapped[bool] = Column(Boolean, default=True)

    modifiers: List[TemplateResourceModifiers] = JSONColumn(default=[])

    user = relationship("TableUser")

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


class TableTemplate(SQLModel):
    __tablename__ = "template"

    sub: Mapped[str] = Column(String, ForeignKey(TableUser.ref), )

    content: Mapped[str] = Column(String, default=None)
    subject: Mapped[str] = Column(String, default=None)
    title: Mapped[str] = Column(String, default=None)
    type: Mapped[str] = Column(String, server_default='personal')
    variables: Mapped[dict] = JSONColumn(default={key: None for key in UserSchema.model_fields.keys()})
    resources: List[TemplateResourceSchema] = JSONColumn(default=[])
    deletable: Mapped[bool] = Column(Boolean, default=True)

    __table_args__ = AppendableTableArgs(constraint_unique(title, sub))
    user = relationship("TableUser")


