from typing import Annotated

import psutil
from fastapi import Header, Depends, Request, Cookie
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from icecream import ic

from pydantic import Field

from elemental_tools.code.speed_test import Timer
from elemental_tools.constants import path_auth_login, path_auth_logout, path_auth_refresh, path_health_check, \
    path_auth_device, ref_length, path_read_me
from elemental_tools.api.controllers.device import DeviceController
from elemental_tools.api.depends import device_authorization, user_login, generate_device_fingerprint
from elemental_tools.api.schemas import ResponseMessage
from elemental_tools.api.schemas.auth import LoginSchema, DeviceSchema, ResponseLoginSuccess, \
    ResponseAllowDeviceSuccess, ResponseRefreshSuccess
from elemental_tools.config import config_initializer
from elemental_tools.db import update, select, and_
from elemental_tools.json import json_parser
from elemental_tools.system import generate_reference
from elemental_tools.exceptions import Unauthorized, NotFoundDevice, Invalid, SaveException
from elemental_tools.logger import Logger
from elemental_tools.pydantic import PyBaseModel
from elemental_tools.safety import InternalClock
from elemental_tools.system import Cache
from elemental_tools.tools import get_package_name, get_ip_address_location

config = config_initializer()
router = APIRouter()
device_controller = DeviceController()
cache = Cache()


__logger__ = Logger(app_name=config.app_name, owner=get_package_name(__name__), destination=config.log_path).log
_clock = InternalClock(logger=__logger__)


tags_auth = ["Auth"]
tags_health_check = ["Health Check"]


class HealthResponse(PyBaseModel, extra="allow"):

    class System(PyBaseModel):
        cpu_load: float = Field(default_factory=lambda: psutil.virtual_memory().percent)
        ram_usage: float = Field(default_factory=psutil.cpu_percent)
        requests_per_second: float = Field(default=0.0)

    class API(PyBaseModel):
        allowed_device_amount: int = Field(default_factory=lambda: int(device_controller.count_rows(device_controller.__orm__.status)))

    class You(PyBaseModel, extra="allow"):
        ip_address: str = Field(None)
        location: dict = Field({})
        request: dict = Field({})

    system: System = Field(default_factory=System)
    api: API = Field(default_factory=API)
    you: You = Field(default_factory=You)


@router.get(path_health_check, tags=tags_health_check, response_model=HealthResponse)
async def root(request: Request, user_agent=Header(alias="user-agent"), device_info=Cookie(alias="device-info", default="")):
    timer = Timer()
    response = {}

    status_code = 500

    try:
        response = HealthResponse()
        response.you.ip_address = request.client.host
        response.you.headers = dict(request.headers)
        response.you.fingerprint = generate_device_fingerprint(user_agent, request.client.host, device_info)
        location_tag = f"""{response.you.ip_address.replace(".", "")}_location"""
        location = cache.get(location_tag)

        if location is None:
            location = get_ip_address_location(response.you.ip_address)
            cache.__setattr__(location_tag, location)
            cache.save()

        response.you.location = location

        response = response.model_dump()
        status_code = 200

    except Exception as e:
        if isinstance(response, HealthResponse):
            response = response.model_dump()

        response["detail"] = str(e)
        response["instructions"] = f"In order to reinstall the database follow the read me instructions:{path_read_me}"

    if isinstance(response["system"], dict):
        response["system"]["requests_per_second"] = timer.per_sec()

    return JSONResponse(response, status_code=status_code)


@router.post(path_auth_login, tags=tags_auth, response_model=ResponseLoginSuccess)
async def login(_user: Annotated[LoginSchema, None] = Depends(user_login)):

    __logger__("info", f"Login On Device:\n\tFingerprint: {_user.fingerprint}\n\tEmail: {str(_user.email)}", origin=path_auth_login)
    response = {"access-token": _user.access_token}
    __logger__("success", f"Logged Device: {str(_user.device_ref)}", origin=path_auth_login)

    return JSONResponse(content=response, headers=response, status_code=200)


@router.post(path_auth_logout, tags=tags_auth, response_model=ResponseMessage)
async def logout(request: Request, access_token: str = Header(json_schema_extra={"default": "{{access_token}}"}), refresh_token: str = Header(json_schema_extra={"default": "{{refresh_token}}"}), user_agent=Header(alias="user-agent"),
        device_info=Cookie(alias="device-info")):
    fingerprint = generate_device_fingerprint(user_agent, request.client.host, device_info)

    try:
        _device_in_database = device_controller.query(
            select(device_controller.__orm__).filter(
                and_(
                    device_controller.__orm__.fingerprint == fingerprint,
                    device_controller.__orm__.access_token == access_token,
                    device_controller.__orm__.refresh_token == refresh_token)
            )
        )

        if _device_in_database is not None:
            _device = DeviceSchema(**_device_in_database)
            _device._sub, _device._ref = _device_in_database["sub"], _device_in_database["ref"]
            _device.status = False
            _device.refresh_token = None

            device_controller.update(update(device_controller.__orm__).filter_by(ref=_device._ref, sub=_device._sub).values(**_device.model_dump()))

            return JSONResponse(content=dict(message="Device logged out successfully"), headers={"access-token": ""}, status_code=200)

        raise NotFoundDevice

    except Exception as e:
        raise SaveException("Auth", status_code=403)


@router.post(path_auth_refresh, tags=tags_auth, response_model=ResponseRefreshSuccess)
async def post_refresh_token(request: Request, access_token: str = Header(json_schema_extra={"default": "{{access_token}}"}), user_agent=Header(alias="user-agent"),
        device_info=Cookie(alias="device-info")):
    fingerprint = generate_device_fingerprint(user_agent, request.client.host, device_info)

    __logger__("info", f"Checking Device:\n\tFingerprint: {str(fingerprint)}\n\tAccess-Token: {str(access_token)}", origin=path_auth_refresh, debug=config.debug)
    _device_in_database = device_controller.query(select(device_controller.__orm__).filter(
        and_(
            device_controller.__orm__.fingerprint == fingerprint,
            device_controller.__orm__.access_token == access_token,
            device_controller.__orm__.status
        )))

    if _device_in_database is not None:
        __logger__("info", f"Device Located: {str(_device_in_database)}", origin=path_auth_refresh, debug=config.debug)

        _device_in_database["refresh_token"] = generate_reference()

        _update_res = device_controller.update(update(device_controller.__orm__).filter_by(ref=_device_in_database["ref"]).values(refresh_token=_device_in_database["refresh_token"]))

        if _update_res is not None:
            _result = {
                "access-token": _device_in_database["access_token"], "refresh-token": _device_in_database["refresh_token"]
            }

            __logger__("success", f"Device Authorized: {str(_update_res)}", origin=path_auth_refresh)
            return JSONResponse(content=_result, headers=_result, status_code=200)

    __logger__("alert", f"Device Unauthorized: {str(_device_in_database)}", origin=path_auth_refresh)
    raise Unauthorized("Device")


@router.put(path_auth_device, tags=tags_auth, response_model=ResponseAllowDeviceSuccess)
async def allow_device(device: Annotated[DeviceSchema, None] = Depends(device_authorization)):

    try:
        status_code, data = 200, ResponseAllowDeviceSuccess(location=device.location).model_dump()
        __logger__("success", f"Device Allowed: {str(device._ref)}", origin=path_auth_device)
        return JSONResponse(data, status_code=status_code)
    except Exception as e:
        raise Unauthorized(message=str(e))

