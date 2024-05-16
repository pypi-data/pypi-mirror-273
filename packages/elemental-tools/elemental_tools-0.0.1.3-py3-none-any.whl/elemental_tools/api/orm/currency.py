from elemental_tools.api.orm import TableUser
from elemental_tools.db import SQLModel, Column, ForeignKey, String, Mapped, relationship, Float


class TableCurrency(SQLModel):
    __tablename__ = "currency"

    sub: Mapped[str] = Column(String, ForeignKey(TableUser.ref), name="sub", nullable=False)
    currency_from: Mapped[str] = Column(String, name="currency_from", nullable=False)
    currency_to: Mapped[str] = Column(String, name="currency_to", nullable=False)
    exchange_tax: Mapped[float] = Column(Float, name="exchange_tax", nullable=False)

    user = relationship("TableUser")

