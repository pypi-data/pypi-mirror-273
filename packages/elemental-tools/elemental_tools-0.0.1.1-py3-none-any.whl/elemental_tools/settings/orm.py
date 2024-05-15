from elemental_tools.db.constraints import constraint_unique, constraint_setting_name
from elemental_tools.db.orm import SQLModel, AppendableTableArgs
from elemental_tools.db import Column, String, Mapped, LargeBinary, Boolean, ForeignKey


class TableSetting(SQLModel):
    __tablename__ = "setting"

    sub: Mapped[str] = Column(String, nullable=True, name="sub")
    name: Mapped[str] = Column(String, nullable=False, name="name")
    value: Mapped[bytes] = Column(LargeBinary, nullable=True, default=None, name="value")
    type: Mapped[str] = Column(String, nullable=False, name="type")
    visible: Mapped[bool] = Column(Boolean, server_default="true", name="visible")

    __table_args__ = AppendableTableArgs(constraint_unique(sub, name))
    __table_args__.append(constraint_setting_name)

