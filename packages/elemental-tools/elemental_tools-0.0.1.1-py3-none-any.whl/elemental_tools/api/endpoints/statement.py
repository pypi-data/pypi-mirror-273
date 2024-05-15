from typing import Annotated

from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from elemental_tools.constants import path_get
from elemental_tools.api.controllers.statement import StatementController
from elemental_tools.api.schemas.user import UserSchema
from elemental_tools.config import config_initializer
from elemental_tools.exceptions import QueryException, NotFound
from elemental_tools.json import json_parser
from elemental_tools.logger import Logger
from elemental_tools.tools import get_package_name

config = config_initializer()
router = APIRouter()

__logger__ = Logger(app_name=config.app_name, owner=get_package_name(__name__), destination=config.log_path).log

path_root = "/user/statement"


@router.get(f"{path_root}{path_get}", tags=['Statement'])
async def statement_get(_user: Annotated[UserSchema, None], date: str, institution=None):

	try:
		statement_db = StatementController(sub=_user._ref, institution_ref=institution)

		result = statement_db.retrieve_statement()

		if result is None:
			return NotFound("Statement")
	except:
		raise QueryException("Statement")

	return JSONResponse(content=json_parser(result), status_code=200)

