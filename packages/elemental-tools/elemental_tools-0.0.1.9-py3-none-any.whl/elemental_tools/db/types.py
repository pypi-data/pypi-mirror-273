from typing import Union
from uuid import uuid4


from icecream import ic
from sqlalchemy import Table, Index as SQLAlchemyIndex, text, String, LargeBinary, Boolean, Column, Integer, Float, \
    DateTime, func
from sqlalchemy.dialects.postgresql import JSON, JSONB
from citext import CIText

from typing import *
from pydantic import *

from sqlalchemy.orm import Mapped
from sqlalchemy.types import Enum as SQLEnum

from elemental_tools.constants import ref_length

Citext = CIText()
db_uuid = func.substr(func.gen_random_uuid().cast(String), 1, ref_length)


def JSONColumn(*args, **kwargs) -> Column:
    return Column(JSONB, *args, **kwargs)


class Index:
    fields: list
    unique: bool = False
    order = 'asc'
    sparse: bool = True

    def __init__(self, fields: list, unique: bool = False, order: str = 'asc', sparse: bool = True, **kwargs):
        """
		Model for Index Dictations.
		:param fields: List of fields included in the index.
		:param unique: Bool indicating presence of unique or not unique constraint. (Default: False).
		:param order: (Default: asc). Available Options (asc, desc). Indicates order for the current field presentation, useful with dates and other information that must be presented first and loaded faster.
		:param sparse: (Default: True). Available Options (True, False). Indicates when null or None values must be ignored by the current index.
		"""

        self.fields = fields
        self.unique = unique
        self.order = order

        self.sparse = True

        self.kwargs = kwargs
