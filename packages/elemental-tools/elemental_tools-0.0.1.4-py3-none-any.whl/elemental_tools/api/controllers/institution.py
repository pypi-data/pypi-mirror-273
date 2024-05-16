from elemental_tools.logger import Logger
from elemental_tools.db.controller import Controller
from elemental_tools.api.orm.institution import TableInstitution


class InstitutionController(Controller):
	__orm__ = TableInstitution


