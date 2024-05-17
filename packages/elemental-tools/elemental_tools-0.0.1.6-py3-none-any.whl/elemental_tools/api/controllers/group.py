from elemental_tools.logger import Logger
from elemental_tools.db.controller import Controller
from elemental_tools.api.orm.group import TableGroup


class GroupController(Controller):
	__orm__ = TableGroup


