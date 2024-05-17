from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from elemental_tools.constants import path_institution_get, path_institution_post, \
    path_institution_put
from elemental_tools.api.controllers.institution import InstitutionController
from elemental_tools.api.schemas.institution import InstitutionSchema
from elemental_tools.config import config_initializer
from elemental_tools.db import insert, update, select, DuplicateKeyError
from elemental_tools.exceptions import QueryException, NotFound, AlreadyExists, SaveException
from elemental_tools.logger import Logger
from elemental_tools.tools import get_package_name

config = config_initializer()
router = APIRouter()
institution_controller = InstitutionController()

__logger__ = Logger(app_name=config.app_name, owner=get_package_name(__name__), destination=config.log_path).log

tags = ["Institution"]


@router.get(path_institution_get, tags=tags)
async def institution_get():
    try:
        result = list(institution_controller.query_all(select(institution_controller.__orm__).filter_by(status=True)))
    except Exception as e:
        raise QueryException("Institution", exception=str(e))

    if result is None:
        raise NotFound("Institution")

    return JSONResponse(content=result, status_code=200)


@router.post(path_institution_post, tags=tags)
async def institution_add(body: InstitutionSchema):
    __logger__('info', f'API received the doc: {str(body.__dict__)}')

    try:
        result = institution_controller.insert(insert(institution_controller.__orm__).values(**body.model_dump()))
    except DuplicateKeyError:
        raise AlreadyExists("Institution", "tax_number")

    if result is None:
        raise SaveException("Institution")

    return JSONResponse(content=dict(result), status_code=200)


@router.put(path_institution_put, tags=tags)
async def institution_edit(body: InstitutionSchema):
    try:
        result = institution_controller.update(update(institution_controller.__orm__).filter_by(tax_number=body.tax_number).values(**body.model_dump()))[0]
    except Exception as e:
        raise SaveException("Institution", exception=str(e))

    return JSONResponse(content={"ref": result[0]}, status_code=200)
