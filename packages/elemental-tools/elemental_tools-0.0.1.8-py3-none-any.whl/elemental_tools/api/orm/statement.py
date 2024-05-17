from datetime import datetime
from typing import Union

from elemental_tools.asserts import DefaultTax
from elemental_tools.db import SQLModel, ForeignKey, Column, Mapped, LargeBinary, String, Boolean, Float, ForeignKey, relationship, DateTime
from elemental_tools.api.orm.institution import TableInstitution


class TableStatement(SQLModel):
    __tablename__ = "statement"

    sub: Mapped[str] = Column(String, name="sub", nullable=False)
    type: Mapped[str] = Column(String, nullable=False)
    tax: Mapped[float] = Column(Float, default=DefaultTax(sub=sub))
    value: Mapped[float] = Column(Float)
    date: Mapped[datetime] = Column(DateTime, nullable=False)
    institution_ref: Mapped[str] = Column(String, ForeignKey(TableInstitution.ref), nullable=False)
    institution: Mapped[str] = relationship("TableInstitution", foreign_keys=[institution_ref])


