from typing import List, Annotated

import pandas as pd
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from elemental_tools.constants import path_notification_get, path_notification_post, \
    path_notification_put
from elemental_tools.api.controllers.notification import NotificationController
from elemental_tools.api.controllers.template import TemplateController, TemplateResourcesController
from elemental_tools.api.controllers.user import UserController
from elemental_tools.api.depends import auth
from elemental_tools.api.schemas.notification import NotificationSchema
from elemental_tools.api.schemas.templates import TemplateResourceSchema
from elemental_tools.api.schemas.user import UserSchema
from elemental_tools.config import config_initializer
from elemental_tools.db import insert, update, select, DuplicateKeyError, or_
from elemental_tools.exceptions import NotFound, QueryException, SaveException, Invalid, AlreadyExists
from elemental_tools.logger import Logger
from elemental_tools.templates import Templates
from elemental_tools.tools import get_package_name

config = config_initializer()
router = APIRouter()
notification_controller = NotificationController()
user_controller = UserController()
template_controller = TemplateController()
template_resources_controller = TemplateResourcesController()


__logger__ = Logger(app_name='api-endpoint', owner=get_package_name(__name__), destination=config.log_path).log


tags = ["Notifications"]


@router.get(path_notification_get, tags=tags)
async def notification_get(_user: Annotated[UserSchema, None] = Depends(auth)):
    try:
        result = None
        users_id = [_user._ref]

        siblings = user_controller.query_all(select(user_controller.__orm__).filter_by(sub=_user.sub))
        if siblings is not None:
            users_id += [sib["ref"] for sib in siblings]

        notifications = notification_controller.query_all(
            select(notification_controller.__orm__).filter(notification_controller.__orm__.sub.in_(users_id)))

        if notifications is not None:

            result = []
            all_user_resources = template_resources_controller.query_all(select(template_controller.__orm__).filter(or_(notification_controller.__orm__.sub == _user._ref, notification_controller.__orm__.sub.in_(users_id))))

            if all_user_resources is not None:
                resources_dataframe = pd.DataFrame(all_user_resources)

            else:
                resources_dataframe = pd.DataFrame({**TemplateResourceSchema().model_dump()})

            # iterate on every notification found to retrieve add data:
            for notification in notifications:

                current_notification = NotificationSchema(**notification)

                # query template:
                current_template = template_controller.query(
                    select(template_controller.__orm__).filter_by(ref=current_notification.template_ref))

                if current_template is not None:
                    current_notification.template_title = current_template["title"]
                    current_notification.template_subject = current_template["subject"]

                    # query destination:
                    current_destination = user_controller.query(
                        select(user_controller.__orm__).filter_by(ref=current_notification.customer_ref))
                    if current_destination is not None:

                        current_notification.destination_name = current_destination["name"]
                        current_notification.destination_email = current_destination["email"]
                        current_notification.destination_cellphone = current_destination["cellphone"]
                        current_notification.modifier_labels = []
                        for notification_modifier in current_notification.modifiers:

                            try:
                                current_resources = resources_dataframe[
                                    resources_dataframe["ref"].isin(current_template["resources"])]
                                _this_resource_modifiers = current_resources["modifiers"].iloc[0]

                                for mod in _this_resource_modifiers:
                                    current_notification.modifier_labels.append(mod["title"])

                            except KeyError:
                                pass

                    # convert to jsonable data:
                    _result = current_notification.model_dump()
                    result.append(_result)

        if result is None:
            # "model": NotificationSchema().__dict__
            return NotFound("Notification")

    except Exception as e:
        raise QueryException("Notification")

    return JSONResponse(content=result, status_code=200)


@router.post(path_notification_post, tags=tags)
async def notification_add(body: List[NotificationSchema], _user: Annotated[UserSchema, None] = Depends(auth)):

    try:
        result = []
        for notification in body:
            notification.sub = _user._ref
            if notification.template_ref is not None:
                try:
                    templates = Templates(notification.sub, notification.template_ref)
                    if templates.user_templates is None:
                        raise NotFound("Template")

                    if templates.this_template is not None:
                        notification.last_response_execution = None

                except Exception as exc:
                    raise SaveException("Notification", exception="template exception")

            try:
                notification.modifiers = [str(mod) for mod in notification.modifiers if mod is not None]
            except TypeError:
                raise Invalid("Notification Modifier")

            try:
                notification.customer_ref = notification.customer_ref
            except TypeError:
                raise Invalid("Notification Customer Reference")

            try:
                notification.template_ref = notification.template_ref
            except TypeError:
                raise Invalid("Notification Template")

            _result = notification_controller.insert(insert(notification_controller.__orm__).values(notification.model_dump()))
            result.append(_result[0])

        return JSONResponse(content=result, status_code=200)

    except DuplicateKeyError as d:
        __logger__('error', f'Failed to store notification because of exception: {str(d)}')
        raise AlreadyExists("Notification", "customer")


@router.put(path_notification_put, tags=tags)
async def notification_edit(sub: str, body: NotificationSchema):

    try:
        result = notification_controller.update(update(notification_controller.__orm__).filter_by(ref=sub).values(**body.model_dump()))

    except:
        raise SaveException("Notification")

    return JSONResponse(content=result, status_code=200)

