from typing import Annotated, Union

import pandas as pd
from fastapi import Depends, Header
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from elemental_tools.constants import path_template_get, path_template_resource_get, \
    path_template_resource_modifier_get, path_template_patch, path_template_resource_patch
from elemental_tools.api.controllers.template import TemplateController, TemplateResourcesController
from elemental_tools.api.controllers.user import UserController
from elemental_tools.api.depends import auth
from elemental_tools.api.schemas.templates import TemplateSchema, TemplateResourceSchema
from elemental_tools.api.schemas.user import UserSchema
from elemental_tools.config import config_initializer
from elemental_tools.db import select, insert, update, and_, or_, DuplicateKeyError
from elemental_tools.system import generate_reference
from elemental_tools.exceptions import QueryException, AlreadyExists, SaveException
from elemental_tools.logger import Logger
from elemental_tools.tools import get_package_name

config = config_initializer()
router = APIRouter()
template_controller = TemplateController()
user_controller = UserController()
template_resources_controller = TemplateResourcesController()


__logger__ = Logger(app_name=config.app_name, owner=get_package_name(__name__), destination=config.log_path).log


tag_template = ["Notification/Template"]
tag_template_resource = ["Notification/Template Resource"]


@router.get(path_template_get, tags=tag_template)
async def template_get(_user: Annotated[UserSchema, None] = Depends(auth), template_ref=Header(default=None)):
    try:

        # When user not provide an id, return all templates available:
        if template_ref is None:
            result = []
            _result = template_controller.query_all(select(template_controller.__orm__).filter_by(sub=_user._ref))

            for e in _result:
                result.append(e)

        # Otherwise, query for the requested id:
        else:
            result = template_controller.query(select(template_controller.__orm__).filter(
                and_(template_controller.__orm__.sub == _user._ref, template_controller.__orm__.ref == template_ref)))

            if result is not None:
                result['ref'] = str(result["ref"])
                if result['resources'] is not None:
                    result['temp'] = []
                    for res in result['resources']:
                        _this_resource = template_resources_controller.query(
                            select(template_resources_controller.__orm__).filter(
                                and_(template_resources_controller.__orm__.sub == _user._ref,
                                     template_resources_controller.__orm__.ref == res)))
                        if _this_resource is not None:
                            result['temp'].append(_this_resource)

        if result is None:
            return JSONResponse(
                content={'message': 'Cannot find templates', 'model': TemplateSchema().__dict__},
                status_code=404)

    except Exception as e:
        raise QueryException("Template", exception=str(e))

    return JSONResponse(content=result, status_code=200)


@router.get(path_template_resource_get, tags=tag_template_resource, description="Returns the template resources")
async def template_resource(resource_id: Union[str, None] = Header(default=None),
                            _user: Annotated[UserSchema, None] = Depends(auth)):
    _result = []
    try:

        if resource_id is None:
            # select(user_controller.__orm__).filter_by()
            _siblings = []
            # user_controller.query_all()
            if _siblings is not None:
                _siblings = list(_siblings)
            else:
                _siblings = []

            _user_resources = template_resources_controller.get_from_user(sub=_user._ref, user_sub=_user.sub,
                                                                          siblings=_siblings)
            if _user_resources is not None:
                _result = list(_user_resources)

        else:
            _user_resources = template_resources_controller.query_all(
                select(template_resources_controller.__orm__).filter_by(sub=_user._ref, ref=resource_id))

        result = []
        for resource in _user_resources:
            resource["ref"] = str(resource["ref"])
            del resource["sub"]
            result.append(resource)

    except Exception as e:
        raise QueryException("Template Resource", exception=str(e))

    return JSONResponse(content=result, status_code=200)


@router.get(path_template_resource_modifier_get, tags=tag_template_resource, description="Returns the template resources modifiers")
async def template_resource_modifiers(
        template_ref: str = Header(description="When not set, return all templates for the current user."),
        _user: Annotated[UserSchema, None] = Depends(auth)
):
    _result = []
    try:

        _siblings = user_controller.query_all({'sub': _user.sub})
        if _siblings is not None:
            _siblings = list(_siblings)
        else:
            _siblings = []

        current_template = template_controller.query(dict(_id=template_ref))

        if current_template is not None:
            current_template = TemplateSchema(**current_template)
            old_selector = select(template_resources_controller.__orm__).filter(
                or_(template_resources_controller.__orm__.sub == _user._ref,
                    template_resources_controller.__orm__.sub.in_(_siblings)))

            _user_resources = list(template_resources_controller.query_all(old_selector))
            _user_resources_df = pd.DataFrame(_user_resources)
            for resource in current_template.resources:
                # Filter the DataFrame based on _id
                current_resource = _user_resources_df[_user_resources_df['ref'] == resource]
                # Convert the filtered DataFrame to dictionary with 'records' orientation
                for modifiers in current_resource.modifiers:
                    for mod in modifiers:
                        _result.append(mod)

    except Exception as e:
        raise QueryException("Template Resource", exception=str(e))

    return JSONResponse(content=list(_result), status_code=200)


@router.patch(path_template_patch, tags=tag_template, description="Save Notification Template")
async def template_save(body: TemplateSchema, _user: Annotated[UserSchema, None] = Depends(auth), template_ref=Header(default=None)):

    try:
        body.set_ref(template_ref)

        body.sub = _user._ref

        body.resources = [res for res in body.resources]

        if body.ref is not None:
            try:
                _result = template_controller.update(update(template_controller.__orm__).filter_by(ref=body.ref).values(**body.model_dump()))

                if _result:
                    _result = {"ref": body.ref}
                else:
                    _result = {"ref": None}

            except DuplicateKeyError as e:
                raise AlreadyExists("Template", "Title")

        else:
            _result = template_controller.insert(insert(template_controller.__orm__).values(**body.model_dump()))

    except Exception as e:
        raise SaveException("Template", exception=str(e))

    return JSONResponse(content=_result, status_code=200)


@router.patch(path_template_resource_patch, tags=tag_template_resource, description="Create a new template resource")
async def template_resource_save(body: TemplateResourceSchema, _user: Annotated[UserSchema, None] = Depends(auth), resource_id=Header(default=None)):

    try:
        body.set_ref(resource_id)
        body.sub = _user._ref
        if body.icon is not None:
            body.icon = await body.icon.read()

        if body.ref is not None:
            try:
                body.modifiers = [mod for mod in body.modifiers if mod is not None]

                for mod in body.modifiers:
                    if mod.ref is None:
                        mod.ref = generate_reference()

                _result = template_resources_controller.update(update(template_resources_controller.__orm__).filter_by(ref=body.ref).values(**body.model_dump()))
                if _result is not None:
                    _result = {"result": _result}

            except DuplicateKeyError as e:
                raise AlreadyExists("Resource", "Name")

        else:
            _result = template_resources_controller.insert(insert(template_resources_controller.__orm__).values(**body.model_dump()))[0]

    except Exception as e:
        raise SaveException("Template", exception=str(e))

    return JSONResponse(content=_result, status_code=200)


