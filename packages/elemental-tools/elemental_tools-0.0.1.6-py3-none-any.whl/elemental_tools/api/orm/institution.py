from elemental_tools.api.schemas.google import SheetStyle
from elemental_tools.db.constraints import constraint_unique, constraint_cnpj
from elemental_tools.db.orm import SQLModel, AppendableTableArgs
from elemental_tools.db import JSONColumn, Column, Mapped, String


class TableInstitution(SQLModel):
    __tablename__ = "institution"

    tax_number: Mapped[str] = Column(String(18), nullable=False, name="tax_number")
    name: Mapped[str] = Column(String, nullable=False, name="name")
    alias: Mapped[str] = Column(String, name="alias")
    website: Mapped[str] = Column(String, nullable=True, default=None, name="website")

    style: Mapped[SheetStyle] = JSONColumn(default={'background': "#000000", 'color': "#ffffff"})

    __table_args__ = AppendableTableArgs(constraint_unique(tax_number, name), constraint_cnpj)


