from datetime import datetime

from elemental_tools.api.orm import TableUser
from elemental_tools.api.orm.currency import TableCurrency
from elemental_tools.db import SQLModel, Column, ForeignKey, String, Mapped, relationship, Float, AppendableTableArgs, DateTime, func, Boolean

from elemental_tools.db.constraints import constraint_unique


class TableTransaction(SQLModel):
    __tablename__ = "transaction"

    confirmation_date: Mapped[datetime] = Column(DateTime(timezone=True), name="confirmation_date", nullable=True)
    creation_date: Mapped[datetime] = Column(DateTime(timezone=True), name="creation_date", server_default=func.now(), nullable=False)

    status: Mapped[bool] = Column(Boolean, name="status", nullable=False, server_default="false")
    processed: Mapped[bool] = Column(Boolean, name="processed", nullable=False, server_default="false")
    exported: Mapped[bool] = Column(Boolean, name="exported", nullable=False, server_default="false")

    sub: Mapped[str] = Column(String, ForeignKey(TableUser.ref), name="sub", nullable=False)
    currency_ref: Mapped[str] = Column(String, ForeignKey(TableCurrency.ref), name="currency_ref", nullable=False)

    exchange_tax: Mapped[float] = Column(Float, name="exchange_tax", nullable=False)
    price: Mapped[float] = Column(Float, name="price", nullable=False)

    amount_from: Mapped[float] = Column(Float, name="amount_from", nullable=False)
    amount_to: Mapped[float] = Column(Float, name="amount_to", nullable=False)

    user = relationship("TableUser")
    currency = relationship("TableCurrency")

    __table_args__ = AppendableTableArgs(
        constraint_unique(
            creation_date,
            sub,
            status,
            currency_ref
        )
    )

