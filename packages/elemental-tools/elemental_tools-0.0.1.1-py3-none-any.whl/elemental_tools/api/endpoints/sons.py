from typing import List, Annotated

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from icecream import ic
from pydantic import Field
from sqlalchemy import func

from elemental_tools.constants import path_user_son_get, path_user_son_patch, \
    path_user_son_delete
from elemental_tools.api.controllers.user import UserController
from elemental_tools.api.depends import auth, pagination, Scope
from elemental_tools.api.schemas.pagination import PaginationSchema
from elemental_tools.api.schemas.user import UserSchema, UserSonSchema, ResponseUserSonPatch, ResponseUserGet
from elemental_tools.config import config_initializer
from elemental_tools.db import DuplicateKeyError, insert, update, select, delete, and_
from elemental_tools.exceptions import Unauthorized, NotFound, QueryException, AlreadyExists, Subscribe, AskYourManager
from elemental_tools.json import json_parser
from elemental_tools.logger import Logger
from elemental_tools.pydantic import UserRoles
from elemental_tools.tools import get_package_name

config = config_initializer()
router = APIRouter()
user_controller = UserController()

__logger__ = Logger(app_name=config.app_name, owner=get_package_name(__name__), destination=config.log_path).log

tags = ["Sons"]
blocked = [UserRoles.customer, UserRoles.newby]


@router.get(path_user_son_get, tags=tags, response_model=List[ResponseUserGet])
async def get_sons(_user: UserSchema = Depends(Scope(block=blocked, block_exception=Subscribe)), pagination: Annotated[PaginationSchema, None] = Depends(pagination)):

    try:
        result = []
        _status_code = 200

        _sons = user_controller.query_all(select(user_controller.__orm__).filter_by(sub=_user._ref))

        if _sons is not None:
            result = pagination.get_page(_sons, ResponseUserGet)

        return JSONResponse(content=result, headers={**pagination.headers()},
                            status_code=_status_code)
    except Exception as e:
        raise QueryException("Sons", exception=str(e))


@router.patch(path_user_son_patch, tags=tags, response_model=ResponseUserSonPatch)
async def add_sons(body: List[UserSonSchema], _user: UserSchema = Depends(Scope(expect=UserSonSchema, block=blocked, block_exception=Subscribe))):

    try:
        result = {}

        for user in body:
            _this_user = user.model_dump(exclude_none=True)
            _this_user["sub"] = _user._ref

            try:
                del _this_user["ref"]
            except KeyError:
                pass

            if user.ref is None:

                _insert_result = user_controller.insert(insert(user_controller.__orm__).values(**_this_user))
                for insert_res in _insert_result:
                    result[_this_user["email"]] = str(insert_res[0])

            else:
                result[_this_user["email"]] = str(user_controller.update(
                    update(user_controller.__orm__).filter_by(ref=user.ref, sub=_this_user["sub"]).values(
                        **_this_user))[0][0])

    except DuplicateKeyError as error:
        __logger__("error", f"Failed to store user because of exception: {str(error)}")
        raise AlreadyExists("Son")

    return JSONResponse(content=result, status_code=200)


@router.delete(path_user_son_delete, tags=tags, response_model=List)
async def user_remove_sons(body: List[str], _: None = Depends(Scope(block=blocked, block_exception=AskYourManager)), _user: Annotated[UserSchema, None] = Depends(Scope(block=[UserRoles.employee], block_exception=AskYourManager))):

    _result = None
    _id_list = []

    for _id in body:
        _id_list.append(_id)

    _result = user_controller.delete(delete(user_controller.__orm__).filter(and_(user_controller.__orm__.ref.in_(_id_list),  user_controller.__orm__.sub == _user._ref)))

    if not _result:
        raise NotFound("User")

    return JSONResponse(content={'result': str(_result)}, status_code=200)

