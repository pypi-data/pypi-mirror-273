from typing import Union

from elemental_tools.db import select, or_
from elemental_tools.db.controller import Controller
from elemental_tools.api.orm.template import TableTemplate, TableTemplateResource


class TemplateController(Controller):
	__orm__ = TableTemplate()


class TemplateResourcesController(Controller):
	__orm__ = TableTemplateResource()

	def get_from_user(self, sub: str, user_sub: Union[str, None] = None, siblings: Union[list, None] = None):
		selector = select(self.__orm__).filter(or_(
			self.__orm__.sub == sub,
			self.__orm__.sub.is_(None),
			self.__orm__.sub == user_sub,
			self.__orm__.sub.in_(siblings) & (self.__orm__.global_ == True)
		)).order_by(self.__orm__.creation_date.desc())

		result = None

		query_result = self.query_all(selector)

		if query_result:
			return query_result

# return result

