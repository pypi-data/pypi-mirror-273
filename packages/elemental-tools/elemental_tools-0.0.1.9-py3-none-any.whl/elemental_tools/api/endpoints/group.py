from typing import List, Annotated, Union

from fastapi import Depends, Header
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from elemental_tools.constants import path_group_get, path_group_post, path_group_put
from elemental_tools.api.controllers.group import GroupController
from elemental_tools.api.depends import auth, pagination
from elemental_tools.api.schemas.group import GroupSchema, MembershipSchema
from elemental_tools.api.schemas.pagination import PaginationSchema
from elemental_tools.api.schemas.user import UserSchema
from elemental_tools.pydantic import UserRoles
from elemental_tools.config import config_initializer
from elemental_tools.db import insert, select, update, and_
from elemental_tools.exceptions import get_duplicated_key, Invalid, SaveException, NotFound
from elemental_tools.logger import Logger
from elemental_tools.tools import get_package_name

config = config_initializer()
router = APIRouter()
group_controller = GroupController()


__logger__ = Logger(app_name=config.app_name, owner=get_package_name(__name__), destination=config.log_path).log


tags = ["Group"]


@router.get(path_group_get, tags=tags, response_model=List[GroupSchema])
async def get_group(_user: Annotated[UserSchema, None] = Depends(auth), pagination: Annotated[PaginationSchema, None] = Depends(pagination), role: Union[str, None] = Header(default=None, examples=[e for e in UserRoles.__dict__ if not e.startswith("_")])):
    result = []

    if role is None:
        stmt = select(group_controller.__orm__).where(group_controller.__orm__.members["user_ref"] == _user._ref)
        groups = list(group_controller.query_all(stmt))

    else:
        available_scopes = [e for e in UserRoles.__dict__ if not e.startswith("_")]
        selected_scopes = role.split(",")
        for scope in selected_scopes:
            if scope not in available_scopes:
                raise Invalid("Scope")

        stmt = select(group_controller.__orm__).where(and_(group_controller.__orm__.members["user_ref"] == _user._ref, group_controller.__orm__.members["role"] == role))
        groups = list(group_controller.query_all(stmt))

    if groups is not None:
        result = pagination.get_page(groups)

    return JSONResponse(content={"result": result}, status_code=200)


@router.post(path_group_post, tags=tags)
async def add_groups(body: GroupSchema, _user: Annotated[UserSchema, None] = Depends(auth)):

    try:
        _this_group = body
        _this_group.members = [MembershipSchema(user_ref=_user._ref, role=UserRoles.owner).model_dump()]
        _this_group = body.model_dump()

        _insert_result = group_controller.insert(insert(group_controller.__orm__).values(**_this_group))

        return JSONResponse(content={'ref': _insert_result}, status_code=200)

    except Exception as error:
        __logger__('error', f'Failed to store {str(tags[0])} because of exception: {str(error)}')
        raise SaveException("Group")


@router.put(path_group_put, tags=tags)
async def edit_groups(body: GroupSchema, _user: Annotated[UserSchema, None] = Depends(auth)):

    user_allowed = False

    try:

        user_group = group_controller.query(select(group_controller.__orm__).where(
            and_(group_controller.__orm__.members["user_ref"] == _user._ref,
                 group_controller.__orm__.ref == body.ref,
            )))

        if user_group is not None:

            for member in user_group["members"]:
                if member["user_ref"] == _user._ref and member["role"] in [UserRoles.admin, UserRoles.owner, UserRoles.manager, UserRoles.editor]:
                    user_allowed = True
                    break

            if user_allowed:
                _update_result = group_controller.update(update(group_controller.__orm__).filter_by(ref=body.ref).values(**body.model_dump()))[0]
                return JSONResponse(content={'ref': _update_result}, status_code=200)

        if not user_allowed:
            raise NotFound("Group")

    except Exception as error:
        __logger__('error', f'Failed to edit {str(tags[0])} because of exception: {str(error)}')
        raise SaveException("Group", exception=get_duplicated_key(error))

