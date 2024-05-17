from datetime import datetime

from elemental_tools.db.constraints import constraint_unique
from elemental_tools.db.orm import AppendableTableArgs

from elemental_tools.db import SQLModel, func
from elemental_tools.db import Column, Mapped, String, Integer, DateTime, LargeBinary, JSON, Boolean


class TableTask(SQLModel):
    __tablename__ = f"task"
    __entrypoint__: str
    last_execution: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

    status: Mapped[bool] = Column(Boolean, server_default="false")
    sub: Mapped[str] = Column(String, nullable=False, name="sub")

    task_name: Mapped[str] = Column(String, nullable=False, name="task_name")
    description: Mapped[str] = Column(String, nullable=True, name="description")

    loops: Mapped[int] = Column(Integer, nullable=True, name="loops")
    timer: Mapped[int] = Column(Integer, nullable=True, name="timer")

    schedule_date: Mapped[datetime] = Column(DateTime(timezone=True), nullable=True, name="schedule_date")
    state: Mapped[str] = Column(String, nullable=True, name="state")

    parameters: Mapped[dict] = Column(JSON, nullable=True, name="parameters")

    __table_args__ = AppendableTableArgs(constraint_unique(sub, task_name))

    def get_entrypoint(self):
        return self.__entrypoint__

