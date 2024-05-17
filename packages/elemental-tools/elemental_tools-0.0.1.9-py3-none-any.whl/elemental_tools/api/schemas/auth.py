import uuid
from typing import Union

import requests
from fastapi import Request
from icecream import ic
from pydantic_core.core_schema import ValidationInfo
from fastapi import BackgroundTasks
from elemental_tools.config import config_initializer

from elemental_tools.constants import password_min_length, ref_length, login_retry_times
from elemental_tools.system import generate_reference
from elemental_tools.exceptions import NotFound, UnauthorizedDevice, Invalid, Forbidden, Unauthorized
from elemental_tools.pydantic import BaseModel, field_validator, Field, PrivateAttr, PyBaseModel

from elemental_tools.api.controllers.device import DeviceController
from elemental_tools.api.controllers.user import UserController
from elemental_tools.api.schemas.user import UserSchema

from elemental_tools.db import select, update, insert
from elemental_tools.system import current_timestamp, Cache
from elemental_tools.tools import get_ip_address_location

user_controller = UserController()
device_controller = DeviceController()

config = config_initializer()
cache = Cache()


class DeviceSchema(BaseModel):
    sub: str = Field(description="User ID")
    ip_address: str = Field(description="Device IP Address")
    fingerprint: str = Field(description="User Device Fingerprint")
    location: Union[dict, None] = Field(description="Device Location", default=None)
    status: bool = Field(description="User Device Allowance Status", default=False)

    retry_times: int = Field(default=login_retry_times, alias="_retry_times")
    access_token: str = Field(default_factory=generate_reference, alias="_access_token")
    refresh_token: str = Field(default_factory=generate_reference, alias="_refresh_token")

    @classmethod
    @field_validator('sub')
    def validate_sub(cls, sub):

        try:
            _this_user = user_controller.query(select(user_controller.__orm__).filter_by(ref=sub))
            if _this_user is not None:
                return sub
        except:
            raise NotFound("Device Owner")


class LoginSchema(BaseModel, extra="allow"):
    device_ref: Union[str, None] = Field(None)
    access_token: Union[str, None] = Field(None)

    fingerprint: str = Field(default_factory=generate_reference, min_length=ref_length)

    email: str = Field()
    password: str = Field()

    _this_user: UserSchema = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        user = user_controller.query(select(user_controller.__orm__).filter_by(email=self.email, password=self.password))

        if user is not None:
            self._this_user = UserSchema(**user)
            self._this_user._ref = user["ref"]
            self._this_user._sub = user["sub"]

        else:
            raise Unauthorized("User", "Invalid e-mail, please register.")

    @classmethod
    @field_validator("email")
    def validate_email(cls, email, values: ValidationInfo):

        _this_user = values.data["_this_user"]
        if _this_user is not None:
            return email
        else:
            raise NotFound("User", "Invalid e-mail, please register.")

    @classmethod
    @field_validator("password")
    def validate_password(cls, password, values: ValidationInfo):
        _this_user = values.data["_this_user"]
        if len(password) >= password_min_length and _this_user is not None:
            if values.data["_this_user"].password == password:
                return password

        raise Forbidden("password", message=f"Invalid password, please make sure you are entering at least {password_min_length} chars.")

    def validate_password_and_device(self, ip_address):

        if self._this_user is not None:
            _this_user_device = device_controller.query(select(device_controller.__orm__).filter_by(fingerprint=self.fingerprint, sub=self._this_user._ref))

            if _this_user_device is not None:
                #_device = DeviceSchema(**_this_user_device)

                if _this_user_device["status"]:

                    device_controller.update(update(device_controller.__orm__).filter_by(ref=_this_user_device["ref"]).values(last_update=current_timestamp(), retry_times=login_retry_times),)

                    self.device_ref = _this_user_device["ref"]
                    self.access_token = _this_user_device["access_token"]

                    return self.device_ref, self.access_token

                else:
                    raise UnauthorizedDevice()

            new_device = DeviceSchema(**{"fingerprint": self.fingerprint, "sub": self._this_user._ref}, ip_address=ip_address)
            _device = new_device.model_dump()

            _device["ref"] = new_device._ref
            _device["sub"] = self._this_user._ref
            location = cache.get(f"""{ip_address.replace(".", "")}_location""")

            if location is None:

                location = get_ip_address_location(ip_address)
                cache.__setattr__(f"""{ip_address.replace(".", "")}_location""", location)
                cache.save()

            _device["location"] = location

            device_controller.insert(insert(device_controller.__orm__).values(**_device), upsert=True, index_elements=["fingerprint", "sub"])

            raise UnauthorizedDevice()

        else:
            try:
                _this_user = user_controller.query(select(user_controller.__orm__).filter_by(email=self.email))
            except Exception as e:
                raise NotFound("Email", message=f"Invalid email, please check.")

            if _this_user is not None:
                self._this_user = UserSchema(**_this_user)
                _this_user_device = device_controller.query(select(device_controller.__orm__).filter_by(fingerprint=self.fingerprint, sub=self._this_user._ref))

                if _this_user_device is not None:
                    _device = DeviceSchema(**_this_user_device)

                    _device._ref = _this_user_device["ref"]
                    _device._sub = _this_user_device["sub"]
                    _device._creation_date = _this_user_device["creation_date"]
                    _device._last_update = _this_user_device["last_update"]

                    if _device.status:
                        if _device.retry_times < 1:
                            device_controller.update(update(device_controller.__orm__).filter_by(ref=_device._ref).values(status=False))
                            raise Unauthorized("password", retry_times=0, message="Device has been blocked. Please check your email to allow this device again.")

                        device_controller.update(update(device_controller.__orm__).filter_by(ref=_device._ref).values(retry_times=_device.retry_times - 1))
                        raise Unauthorized("password", retry_times=_device.retry_times)


class ResponseLoginSuccess(PyBaseModel):

    access_token: str = Field(description="Access Token to Use To Generate a Refresh Token", alias="access-token")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ResponseRefreshSuccess(PyBaseModel):

    access_token: str = Field(description="Access Token to Use With Authorized Endpoints", alias="access-token")
    refresh_token: str = Field(description="Refresh Token to Use With Authorized Endpoints", alias="refresh-token")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ResponseAllowDeviceSuccess(PyBaseModel):

    location: Union[dict, None] = Field(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

