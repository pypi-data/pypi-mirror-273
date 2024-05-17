from typing import List, Annotated

from fastapi import Depends, Header, Query
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from icecream import ic

from elemental_tools.api.controllers.group import GroupController
from elemental_tools.constants import path_user_get_me, path_user_post, path_user_put, \
    path_user_institution_patch, path_institution_get, path_user_get_scope
from elemental_tools.api.controllers.institution import InstitutionController
from elemental_tools.api.controllers.user import UserController
from elemental_tools.api.depends import auth, pagination, Scope, FixedScope
from elemental_tools.api.schemas.pagination import PaginationSchema
from elemental_tools.api.schemas.user import UserSchema, UserInstitutionSetting, UserPutSchema, ResponseUserScope, \
    ResponseUserPut, ResponseUserGet
from elemental_tools.asserts import root_ref
from elemental_tools.config import config_initializer
from elemental_tools.db import insert, update, select, DuplicateKeyError
from elemental_tools.system import generate_reference
from elemental_tools.exceptions import QueryException, NotFound, AlreadyExists, SaveException
from elemental_tools.json import compare_and_get_different_values
from elemental_tools.logger import Logger
from elemental_tools.pydantic import UserRoles
from elemental_tools.tools import get_package_name

config = config_initializer()
router = APIRouter()

user_controller = UserController()
institution_controller = InstitutionController()
group_controller = GroupController()

__logger__ = Logger(app_name=config.app_name, owner=get_package_name(__name__), destination=config.log_path).log


tags = ["User"]


@router.get(path_user_get_me, tags=tags, response_model=ResponseUserGet)
async def user_get(_user: Annotated[UserSchema, None] = Depends(auth), pagination: Annotated[PaginationSchema, None] = Depends(pagination)):

    try:

        me = user_controller.query(select(user_controller.__orm__).filter_by(ref=_user._ref))
        if me is not None:
            _result = ResponseUserGet(**me).model_dump()
            return JSONResponse(content=_result, headers={**pagination.headers()},
                                status_code=200)
        else:
            NotFound("User")

    except Exception as e:
        raise QueryException("User", str(e))


@router.get(path_user_get_scope, tags=tags, response_model=ResponseUserScope)
async def user_get_scope(_user: Annotated[UserSchema, None] = Depends(auth), pagination: Annotated[PaginationSchema, None] = Depends(pagination)):

    try:
        stmt = select(group_controller.__orm__).filter(group_controller.__orm__.members["user_ref"] == _user._ref)
        _result = ResponseUserScope(me=_user._role, groups=group_controller.query_all(stmt))

        return JSONResponse(content=_result, headers={**pagination.headers()})

    except Exception as e:
        raise QueryException("User Scope", str(e))


@router.post(path_user_post, tags=tags, response_model=ResponseUserGet)
async def user_post(body: UserSchema, _=Depends(FixedScope(expect=UserSchema, fixed_role=[UserRoles.newby]))):

    try:
        for inst in body.institutions:
            _this_inst = institution_controller.query(select(institution_controller.__orm__).filter_by(ref=inst.institution_ref))

            if _this_inst is None:
                raise NotFound("Institution")

        user = body.model_dump()

        user["ref"] = generate_reference()
        user["sub"] = body._sub
        user["role"] = body._role
        user["creation_date"] = body._creation_date
        user["last_update"] = body._last_update

        result = user_controller.insert(insert(user_controller.__orm__).values(**user))

        _inserted_id = result[0]
    except DuplicateKeyError as d:
        __logger__("error", f"Failed to store user because of exception: {str(d)}")
        raise AlreadyExists("User", "Email")

    return JSONResponse(content=dict(ref=str(_inserted_id)), status_code=200)


@router.put(path_user_put, tags=tags, response_model=ResponseUserPut)
async def user_put(body: UserPutSchema, _user: UserSchema = Depends(Scope(expect=UserPutSchema))):

    if body.institutions is not None and isinstance(body.institutions, list):
        for inst in body.institutions:
            _this_inst = institution_controller.query(select(institution_controller.__orm__).filter_by(ref=inst["ref"]))
            if _this_inst is None:
                raise NotFound("Institution")
    try:
        result = user_controller.update(update(user_controller.__orm__).filter_by(ref=_user._ref).values(**body.model_dump(exclude_none=True), last_update=body._last_update))[0][0]
        return JSONResponse(content=ResponseUserPut(ref=result).model_dump(), status_code=200)
    except DuplicateKeyError or KeyError:
        pass

    raise SaveException("User")


# ATTENTION!!!
@router.patch(path_user_institution_patch, tags=tags, description="To add institutions to a user")
async def user_patch_institutions(body: List[UserInstitutionSetting], _user: Annotated[UserSchema, Depends(auth)]):

    try:
        for inst_to_add in body:
            _this_inst = institution_controller.query(select(institution_controller.__orm__).filter_by(ref=inst_to_add.institution_ref))

            if _this_inst is None:
                raise NotFound("Institution")

        _new_user_institutions = [e.model_dump() for e in body]
        _new_user_institutions_ids = [inst["institution_ref"] for inst in _new_user_institutions]

        _current_user_institutions = user_controller.query({"ref": _user._ref}).get("institutions", [])

        _merge_user_institutions = [c_i for c_i in _current_user_institutions if c_i["institution_ref"] not in _new_user_institutions_ids] + _new_user_institutions
        result = user_controller.update(update(user_controller.__orm__).filter_by(ref=_user._ref).values(institutions=_merge_user_institutions))

    except Exception as e:
        raise SaveException("User", exception=str(e))

    return JSONResponse(content={"count": len(result)}, status_code=200)

