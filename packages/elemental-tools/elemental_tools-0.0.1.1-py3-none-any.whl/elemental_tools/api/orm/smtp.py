from typing import Union

from elemental_tools.asserts import root_ref

from elemental_tools.pydantic import EmailStr
from elemental_tools.db.constraints import constraint_email, UniqueConstraint
from elemental_tools.db.orm import SQLModel, AppendableTableArgs
from elemental_tools.db import Column, String, Mapped, Integer, LargeBinary, Citext


class TableSMTP(SQLModel):
    __tablename__ = 'smtp'

    __table_args__ = AppendableTableArgs(constraint_email())

    sub: Mapped[str] = Column(String, default=root_ref())
    server: Mapped[str] = Column(String, nullable=False)
    port: Mapped[int] = Column(Integer, nullable=False)
    email: Mapped[EmailStr] = Column(String, nullable=False)
    password: Mapped[str] = Column(String, nullable=False)

    __table_args__.append(UniqueConstraint(sub, email))


