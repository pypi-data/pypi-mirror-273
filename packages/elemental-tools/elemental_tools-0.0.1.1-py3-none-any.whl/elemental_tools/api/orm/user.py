from elemental_tools.asserts import DefaultTax
from elemental_tools.pydantic import UserRoles

from elemental_tools.db.constraints import constraint_password_length, constraint_unique, constraint_cnpj, constraint_cpf
from elemental_tools.db.orm import SQLModel, AppendableTableArgs
from elemental_tools.db import JSONColumn, String, Mapped, Column, Boolean, Float, LargeBinary, SQLEnum


class TableUser(SQLModel):
    __tablename__ = "user"

    sub: Mapped[str] = Column(String, name="sub")

    tax_number: Mapped[str] = Column(String(19), name="tax_number")
    doc_number: Mapped[str] = Column(String(14), name="doc_number")
    doc_id_number: Mapped[str] = Column(String, name="doc_id_number")

    admin: Mapped[bool] = Column(Boolean, name="admin", nullable=False, default=False)
    google_sync: Mapped[bool] = Column(Boolean, name="google_sync", nullable=False, default=False)
    is_human_attendance: Mapped[bool] = Column(Boolean, name="is_human_attendance", nullable=False, default=False)

    tax: Mapped[float] = Column(Float, name="tax", nullable=False, default=DefaultTax(sub=sub))
    role: Mapped[str] = Column(SQLEnum(UserRoles), default=UserRoles.customer)
    name: Mapped[str] = Column(String, name="name", nullable=False)
    email: Mapped[str] = Column(String, name="email", nullable=False, unique=True)
    password: Mapped[str] = Column(String, name="password", nullable=True)
    phone: Mapped[str] = Column(String, name="phone", default=None, nullable=True)
    cellphone: Mapped[str] = Column(String, name="cellphone", default=None, nullable=True)
    wpp_user_id: Mapped[str] = Column(String, name="wpp_user_id", default=None, nullable=True)
    parent_assigned_status: Mapped[str] = Column(String, name="parent_assigned_status", default=None, nullable=True)
    obs: Mapped[str] = Column(String, name="obs", default=None, nullable=True)
    language: Mapped[str] = Column(String, name="language", default='pt')
    last_subject: Mapped[str] = Column(String, name="last_subject", default="")

    companies: Mapped[list] = JSONColumn(default=[])
    institutions: Mapped[list] = JSONColumn(default=[])
    google: Mapped[list] = JSONColumn(default=[])

    __table_args__ = AppendableTableArgs(constraint_password_length)
    __table_args__.append(constraint_unique(cellphone, sub, email), constraint_cnpj, constraint_cpf)

