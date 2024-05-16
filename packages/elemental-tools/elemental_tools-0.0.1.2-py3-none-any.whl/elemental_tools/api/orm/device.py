

from elemental_tools.api.orm.user import TableUser

from elemental_tools.db.constraints import constraint_unique
from elemental_tools.db.orm import SQLModel, relationship, AppendableTableArgs
from elemental_tools.db import ForeignKey, Column, String, Optional, Mapped, LargeBinary, Integer, db_uuid, JSONColumn


class TableDevice(SQLModel):
    __tablename__ = "device"

    sub: Mapped[str] = Column(String, ForeignKey(TableUser.ref), name="sub", default=None)
    ip_address: Mapped[str] = Column(String, name="ip_address", nullable=False)
    fingerprint: Mapped[str] = Column(String, name="fingerprint", nullable=False)
    location: Mapped[dict] = JSONColumn(default={}, nullable=False)
    retry_times: Mapped[int] = Column(Integer, name="retry_times", server_default="3", nullable=False)
    access_token: Mapped[str] = Column(String, name="access_token", default=db_uuid)
    refresh_token: Mapped[str] = Column(String, name="refresh_token", default=db_uuid)

    user = relationship("TableUser")

    __table_args__ = AppendableTableArgs(
        constraint_unique(fingerprint, sub)
    )

