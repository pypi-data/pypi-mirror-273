from datetime import datetime
from typing import Any
from sqlalchemy import ForeignKey, DateTime, Integer, LargeBinary, Boolean, ForeignKey, String, func, Column
from sqlalchemy.orm import Mapped, relationship, declarative_base
from sqlalchemy.types import Enum


from elemental_tools.db.types import db_uuid
from elemental_tools.db.constraints import constraint_object_id


class AppendableTableArgs:

    __tuple__ = tuple()

    def __init__(self, *args):
        #self._static_args = {"extend_existing": True}
        self.append(constraint_object_id("ref"))
        self.append(constraint_object_id("sub"))
        self.append(*args)

    def __get__(self, *args, **kwargs):
        this = tuple()
        for value in self.__tuple__:
            if isinstance(value, tuple):
                value = value[0]
            this = (*this, value)
        return this

    def append(self, *new):
        self.__tuple__ = (*self.__tuple__, *new)


class CommonBase(object):

    __abstract__ = True

    id: Mapped[int] = Column(Integer, name="id", primary_key=True, unique=True, autoincrement=True)
    ref: Mapped[str] = Column(String(32), name="ref", nullable=False, primary_key=True, unique=True, server_default=db_uuid)
    sub: Mapped[str] = Column(String(32), name="sub", default=None)
    creation_date: Mapped[datetime] = Column(DateTime(timezone=True), name="creation_date", server_default=func.now(), nullable=False)
    last_update: Mapped[datetime] = Column(DateTime(timezone=True), name="last_update", nullable=False, server_default=func.now(), onupdate=func.now())
    status: Mapped[bool] = Column(Boolean, name="status", nullable=False, server_default="false")

    __table_args__: tuple = AppendableTableArgs()


class Index:
    def __init__(self, fields, unique=False, order='asc', sparse=True, **kwargs):
        self.fields = fields
        self.unique = unique
        self.order = order
        self.sparse = sparse
        self.kwargs = kwargs


SQLModel = declarative_base(cls=CommonBase)


