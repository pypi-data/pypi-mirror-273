import random
import uuid, hashlib
from typing import Union, List, Dict, Any

from fastapi import Header, Request, HTTPException, Cookie
from icecream import ic
from pydantic import EmailStr

from elemental_tools.api.controllers.device import DeviceController
from elemental_tools.api.controllers.user import UserController
from elemental_tools.api.schemas.auth import DeviceSchema, LoginSchema
from elemental_tools.api.schemas.pagination import PaginationSchema
from elemental_tools.api.schemas.user import UserSchema
from elemental_tools.config import config_initializer
from elemental_tools.constants import password_min_length, password_max_length
from elemental_tools.db import select, update
from elemental_tools.exceptions import Unauthorized, Invalid
from elemental_tools.logger import Logger
from elemental_tools.pydantic import BaseModel, UserRoles, PyBaseModel
from elemental_tools.system import multireplace
from elemental_tools.tools import get_package_name

config = config_initializer()

device_controller = DeviceController()
user_controller = UserController()

__logger__ = Logger(app_name=config.app_name, owner=get_package_name(__name__), destination=config.log_path).log


def device_authorization(email: str = Header(json_schema_extra={"default": "{{email}}"}), password: str = Header(json_schema_extra={"default": "{{password}}"}), device: str = Header(json_schema_extra={"default": "{{device_ref}}"}, min_length=24)):
    __logger__("info", f'Device: {device}', origin="device-authorization")

    try:
        device = device_controller.query(select(device_controller.__orm__).filter_by(ref=device))
        user = user_controller.query(select(user_controller.__orm__).filter_by(email=email, password=password))
        __logger__("info", f'User: {user}', origin="device-authorization", debug=config.debug)
        if device is not None and user is not None:
            _device = DeviceSchema(**device)
            _device._ref = device["ref"]

            # renew the token for the next authentication
            device_controller.update(update(device_controller.__orm__).filter_by(ref=device["ref"], status=False).values(status=True))
            __logger__("success", f"Authorized!", origin="device-authorization")
            return _device
        __logger__("alert", f"Unauthorized!", origin="device-authorization")

    except Exception as e:
        __logger__("error", f"Unauthorized!\n\tInternal Exception: {str(e)}", origin="device-authorization")

    raise Unauthorized


def auth(request: Request, access_token: str = Header(json_schema_extra={"default": "{{access_token}}"}), refresh_token: str = Header(json_schema_extra={"default": "{{refresh_token}}"}), user_agent=Header(alias="user-agent"), device_info=Cookie(alias="device-info")) -> UserSchema:
    fingerprint = generate_device_fingerprint(user_agent, request.client.host, device_info)
    return _auth(fingerprint, access_token, refresh_token)


def _auth(fingerprint: str, access_token: str, refresh_token: str) -> UserSchema:

    __logger__('info', f'User Signing With:\n\tFingerprint: {fingerprint}\n\tRefresh Token: {refresh_token}\n\tAccess Token: {access_token}', origin='authentication', debug=config.debug)

    try:
        device_auth = device_controller.query(select(device_controller.__orm__).filter_by(fingerprint=fingerprint, refresh_token=refresh_token, access_token=access_token, status=True))

        if device_auth is not None:
            _user = user_controller.query(select(user_controller.__orm__).filter_by(ref=device_auth['sub']))

            if _user is not None:
                _this_user = UserSchema(**_user)

                _this_user._role = _user["role"]
                _this_user._ref = _user["ref"]
                _this_user._sub = _user["sub"]
                _this_user._creation_date = _user["creation_date"]

                # renew the token for the next authentication
                # device_controller.update(update(device_controller.__orm__).filter_by(ref=_auth['ref']).values(refresh_token=None))
                __logger__('success', f"Authorized!", origin="authentication")
                return _this_user

        __logger__("alert", f"Unauthorized!", origin="authentication")

    except Exception as e:
        __logger__("error", f"Unauthorized!\n\tInternal Exception: {str(e)}", origin="authentication")

    raise Unauthorized


def pagination(page_num: int = Header(default=1), page_size: int = Header(default=50)) -> PaginationSchema:
    """
    Paginates data based on the specified page number and page size.

    Parameters:
        page_num (int): The page number to retrieve. Defaults to 1.
        page_size (int): The number of items per page. Defaults to 50.

    Returns:
        PaginationSchema

    Raises:
        ValueError: If `page_num` or `page_size` is less than 1.
    """

    __logger__("info", f"Querying for Page\n\tNum: {page_num}\n\tPage Size: {page_size}", origin="pagination")
    result = PaginationSchema(page_size=page_size, page_num=page_num)
    __logger__("success", f"Result was found!", origin="pagination")

    return result


def clean_headers(headers: str) -> str:
    junk_chars = [":", " ", "/", "(", ")", ".", ",", "@", "&", "$", "@", "-", "%", "*"]
    return multireplace(headers, from_=junk_chars, to="")


def generate_device_fingerprint(user_agent, request_client_host, device_info) -> str:
    device_info = clean_headers(request_client_host + user_agent + device_info)
    fingerprint = uuid.UUID(bytes=hash(device_info).to_bytes(16, byteorder='big', signed=True)).hex
    return fingerprint


async def user_login(
        request: Request,
        email: EmailStr = Header(json_schema_extra={"default": "{{email}}"}),
        password: str = Header(json_schema_extra={"default": "{{password}}"}, min_length=password_min_length, max_length=password_max_length),
        user_agent=Header(alias="user-agent"),
        device_info=Cookie(alias="device-info")
) -> Union[LoginSchema, None]:
    _user = user_controller.query(select(user_controller.__orm__).filter_by(email=email, password=password))
    fingerprint = generate_device_fingerprint(user_agent, request.client.host, device_info)
    __logger__("info", f'User: {_user}; Device Fingerprint: {fingerprint}', origin="device-authorization", debug=config.debug)

    if _user is not None:

        _result = LoginSchema(email=email, password=password, fingerprint=fingerprint)
        _result.validate_password_and_device(request.client.host)

        __logger__("success", f"Token Generated: {_result.access_token}", origin="device-authorization")

        return _result

    raise Unauthorized("Device")


class Scope:
    __name__ = "Scope"
    expected_role: Union[List[UserRoles], None] = None
    schema: Union[BaseModel, PyBaseModel, Any, None] = None
    user: Union[UserSchema, None] = None
    role: Union[List[UserRoles], None] = None
    _role: Union[List[UserRoles], None] = None
    body = None
    block: Union[List[UserRoles], None] = None
    block_exception: Union[HTTPException, None] = None
    exception: HTTPException = lambda: Unauthorized(detail=f"Unauthorized. Changes are not allowed.", message=f"Changes are not allowed.")

    def __init__(self, expect: Union[BaseModel, PyBaseModel, List[UserRoles], Any] = None, fixed_role: Union[List[UserRoles], None] = None, user: UserSchema = None, block: Union[List[UserRoles], None] = None, block_exception: Any = None):
        """
        Scope Dependency with builtin authentication;

        Args:
            expect: Receives a BaseModel (with Field(json_schema_extra={"role": desiredRole})) or List of UserRoles;
            fixed_role: Fixed role for the validation;
            user: UserSchema to retrieve the auth user role;
        """

        if isinstance(expect, list):
            self.expected_role = expect
        else:
            self.schema = expect

        self.role = fixed_role
        self.user = user

        if user is not None:
            self._role = [user._role]

        if fixed_role is not None:
            self._role = fixed_role

        self.block = block
        self.block_exception = block_exception

    async def validate_role(self, body: Union[dict, list] = None) -> bool:
        """
        Validate the role against the given body.

        Args:
            body: Body of the request to be validated.

        Returns:
            bool: True if validation succeeds.

        Raises:
            Invalid: If the body is invalid.
            Unauthorized: If the role is unauthorized.
        """
        if self.schema is not None:
            if isinstance(body, list) or isinstance(body, List):

                for item in body:
                    await self.validate_role(item)

            if isinstance(body, dict) or isinstance(body, Dict):
                for f_name, f_value in body.items():
                    pydantic_field = self.schema.model_fields.get(f_name, None)
                    if pydantic_field is None:
                        raise Invalid(f_name)
                    if pydantic_field.json_schema_extra is not None:
                        role_spec: Union[None, List[UserRoles]] = pydantic_field.json_schema_extra.get("role", None)
                        if role_spec is not None:
                            if not any([role for role in self._role if role in role_spec]) and UserRoles.all not in role_spec:
                                __logger__("alert", f"Blocked!!!", owner=Scope.__name__)
                                raise Unauthorized(detail=f"Unauthorized. Changes on {f_name} are not allowed.",
                                                   message=f"Changes on {f_name} are not allowed.")

            if not body:
                __logger__("critical", f"Empty Body on Validation!!!", owner=Scope.__name__)
                raise Invalid("body")

        if self.expected_role is not None:
            __logger__("initializing", f"Validating Expected Role: {str(self.expected_role)}")
            if not any([role for role in self.expected_role if role in self._role]) and UserRoles.all not in self.expected_role:
                __logger__("alert", f"Blocked!!!")
                raise self.exception

        return True

    async def __call__(self, request: Request, access_token: str = Header(json_schema_extra={"default": "{{access_token}}"}), refresh_token: str = Header(json_schema_extra={"default": "{{refresh_token}}"}), device_info=Cookie(alias="device-info")) -> Union[UserSchema, None]:
        """
        Callable middleware to handle scope authentication and authorization.

        Args:
            request (Request): HTTP request object.
            access_token (str, optional): Access token. Require Header(json_schema_extra={"default": "{{access_token}}"}).
            refresh_token (str, optional): Refresh token. Require Header(json_schema_extra={"default": "{{refresh_token}}"}).

        Returns:
            Union[UserSchema, None]: User schema if authenticated and authorized, None otherwise.

        """
        __logger__('initializing', f"Role Validation...", owner=Scope.__name__)
        if self.role is None:
            __logger__('initializing', f"Authorizing User...", owner=Scope.__name__)
            fingerprint = generate_device_fingerprint(request.headers['user-agent'], request.client.host, device_info)
            self.user = _auth(fingerprint, access_token, refresh_token)

            self._role = [self.user._role]

            if self.block is not None:
                __logger__('initializing', f"Blocked Role's Validation...",
                           owner=Scope.__name__)
                if any([role for role in self._role if role in self.block]):
                    __logger__('alert', f"Blocking: {str(self.block)} on {str(self._role)}",
                               owner=Scope.__name__)
                    if self.block_exception:
                        raise self.block_exception
                    else:
                        raise self.exception
                __logger__('success', f"Unblocked!", owner=Scope.__name__)

            if request.method != "GET":

                __logger__('initializing', f"Awaiting Body...", owner=Scope.__name__)
                body = await request.json()
                __logger__('success', f"Body Received", owner=Scope.__name__)

                __logger__('initializing', f"Body Validation:\n\t{str(body)}", owner=Scope.__name__)
                await self.validate_role(body)
                __logger__("success", "Body Validation Finished", owner=Scope.__name__)

        if self.user is not None:
            __logger__('success', f"Returning User", owner=Scope.__name__)
            return self.user


class FixedScope(Scope):

    """
    Scope Dependency without authentication;
    """

    async def __call__(self, request: Request) -> None:
        """
        Callable middleware to handle scope without needing user access and refresh token.

        Args:
            request (Request): HTTP request object.

        Returns:
            Union[UserSchema, None]: User schema if authenticated and authorized, None otherwise.

        """
        __logger__('initializing', f"Awaiting Body...",
                   owner=Scope.__name__)
        body = await request.json()
        __logger__('success', f"Body Received", owner=Scope.__name__)

        __logger__('initializing', f"Body Validation:\n\t{str(body)}", owner=Scope.__name__)
        await self.validate_role(body)

