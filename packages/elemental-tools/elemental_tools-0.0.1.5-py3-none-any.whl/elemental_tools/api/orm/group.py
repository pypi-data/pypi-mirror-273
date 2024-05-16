from typing import Union, List

from elemental_tools.api.schemas.group import MembershipSchema



from elemental_tools.db.constraints import constraint_unique
from elemental_tools.db import SQLModel, Column, AppendableTableArgs
from elemental_tools.db import String, JSONColumn, LargeBinary, Mapped


class TableGroup(SQLModel):
    __tablename__ = "group"

    sub: Mapped[str] = Column(String, nullable=False, name="sub")

    title: Mapped[str] = Column(String, nullable=False, name="title")
    members: Mapped[Union[List[MembershipSchema], list]] = JSONColumn(nullable=False, name="members", default=[])

    __table_args__ = AppendableTableArgs(constraint_unique(sub, title))

