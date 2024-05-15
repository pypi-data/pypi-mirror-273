import uuid
from enum import Enum
from typing import Union, Optional, List, ClassVar

from elemental_tools.constants import password_min_length, password_max_length
from elemental_tools.api.schemas.google import GoogleInformation
from elemental_tools.asserts import root_ref
from elemental_tools.exceptions import Invalid
from elemental_tools.pydantic import BaseModel, Field, field_validator, EmailStr, PyBaseModel, PrivateAttr, \
    partial_model, UserRoles
from elemental_tools.system import current_timestamp, generate_reference, multireplace

junk_doc_chars = [".", "-", "/"]
            

class UserInstitutionSetting(PyBaseModel):
    institution_ref: str = Field(description="Obtained using the institution endpoint")
    status: Union[bool, None] = Field(examples=[True, False], description="A boolean indicating whether the institution integration will be enabled", default=True, json_schema_extra={"role": [UserRoles.admin]})
    email: str = Field(description="Email for the user account on the current institution website")
    password: str = Field(description="Password for the user account on the current institution website")
    last_sync: str = Field(description="Timestamp for the last synchronization to this institution",
                           default_factory=current_timestamp)

    @field_validator("institution_ref")
    def validate_institution_ref(cls, institution_ref):
        try:
            return str(institution_ref)
        except:
            raise Invalid("institution_ref")


class UserSchema(BaseModel):
    _role: UserRoles = PrivateAttr(default="customer")
    _sub: Union[str, None] = PrivateAttr(default_factory=root_ref)
    _wpp_user_id: Union[str, None] = PrivateAttr(default=None)
    _is_human_attendance: Optional[bool] = PrivateAttr(default=False)
    _last_subject: Optional[str] = PrivateAttr(default="")

    doc_number: Union[str, None] = Field(description="CPF", default=None, json_schema_extra={"role": [UserRoles.admin, UserRoles.manager, UserRoles.newby]})
    tax_number: Union[str, None] = Field(description="CNPJ", default=None, json_schema_extra={"role": [UserRoles.admin, UserRoles.manager, UserRoles.newby]})
    doc_id_number: Union[str, None] = Field(description="ID/RG", default=None, json_schema_extra={"role": [UserRoles.admin, UserRoles.manager, UserRoles.newby]})

    name: str = Field(description="User Name", json_schema_extra={"role": [UserRoles.admin, UserRoles.manager, UserRoles.newby]})
    email: EmailStr = Field(description="User Email", json_schema_extra={"role": [UserRoles.admin, UserRoles.manager, UserRoles.newby]})
    password: str = Field(description="Password", min_length=password_min_length, max_length=password_max_length, json_schema_extra={"role": [UserRoles.admin, UserRoles.manager, UserRoles.newby, UserRoles.customer]})

    phone: Union[str, None] = Field(description="User Phone", default=None, json_schema_extra={"role": [UserRoles.admin, UserRoles.manager, UserRoles.newby]})
    cellphone: Union[str, None] = Field(description="User Cellphone (Whatsapp and SMS)", default=None, json_schema_extra={"role": [UserRoles.admin, UserRoles.manager, UserRoles.newby]})

    language: str = Field(description="Language for message translation", default="pt", json_schema_extra={"role": [UserRoles.admin, UserRoles.manager, UserRoles.newby, UserRoles.customer]})

    google_sync: bool = Field(description="Activate the google statement synchronization for the current user", default=False, json_schema_extra={"role": [UserRoles.admin, UserRoles.manager, UserRoles.newby, UserRoles.customer]})
    institutions: Union[List[UserInstitutionSetting], list, None] = Field(examples=[[UserInstitutionSetting(**{"status":True, "institution_ref": str("65dbfb92b01fc2f7ebe66620"), "email": "a@b.com", "password": "123456"})]], description="Store the user information for the institutions to be integrated", default=[])
    google: Optional[GoogleInformation] = Field(default=GoogleInformation())

    @classmethod
    @field_validator("cellphone")
    def validate_cellphone(cls, cellphone):
        if cellphone is not None:
            return cellphone
        else:
            raise Invalid("cellphone")

    @classmethod
    @field_validator("password")
    def validate_password(cls, password):
        if password is not None:
            if len(password) >= password_min_length:
                return password
            else:
                raise Invalid("password")

    @classmethod
    @field_validator("institutions")
    def valid_institutions(cls, institutions: list):
        result = []

        for institution in institutions:
            if not isinstance(institution, UserInstitutionSetting):
                result.append(UserInstitutionSetting(**institution))
            else:
                result.append(institution)

        return result

    @field_validator("doc_number")
    def valid_doc_number(cls, value: Union[str, None]):

        if value is not None:
            clean_doc = multireplace(value, from_=junk_doc_chars, to="")
            threshold = len(clean_doc) * 0.9
            if clean_doc.count("0") >= threshold:
                raise Invalid("doc_number")

        return value

    @field_validator("doc_id_number")
    def valid_doc_id_number(cls, value: Union[str, None]):

        if value is not None:
            clean_doc = multireplace(value, from_=junk_doc_chars, to="")
            threshold = len(clean_doc) * 0.9

            if clean_doc.count("0") >= threshold:
                raise Invalid("doc_id_number")

        return value

    @field_validator("tax_number")
    def valid_tax_number(cls, value: Union[str, None]):

        if value is not None:
            clean_doc = multireplace(value, from_=junk_doc_chars, to="")
            threshold = len(clean_doc) * 0.9

            if clean_doc.count("0") >= threshold:
                raise Invalid("tax_number")

        return value


@partial_model
class UserPutSchema(UserSchema):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UserSonSchema(BaseModel):

    _wpp_user_id: Union[str, None] = PrivateAttr(default=None)
    _is_human_attendance: Optional[bool] = PrivateAttr(default=False)
    _last_subject: Optional[str] = PrivateAttr(default="")

    _sub: str = PrivateAttr(default_factory=root_ref)
    ref: str = Field(default=None, description="User Reference")

    role: UserRoles = Field(default=UserRoles.customer, description="User Role", json_schema_extra={"role": [UserRoles.admin, UserRoles.manager]})
    password: Union[str, None] = Field(description="Password", default=None, min_length=password_min_length, max_length=password_max_length, json_schema_extra={"role": [UserRoles.admin, UserRoles.manager]})

    name: str = Field(description="Username")
    email: EmailStr = Field(description="User Email")
    phone: Union[str, None] = Field(description="User Phone", default=None)
    cellphone: Union[str, None] = Field(description="User Cellphone, for whatsapp and sms", default=None)

    doc_number: Union[str, None] = Field(description="CPF", default=None, json_schema_extra={"role": [UserRoles.admin, UserRoles.manager]})
    tax_number: Union[str, None] = Field(description="CNPJ", default=None, json_schema_extra={"role": [UserRoles.admin, UserRoles.manager]})
    doc_id_number: Union[str, None] = Field(description="ID/RG", default=None, json_schema_extra={"role": [UserRoles.admin, UserRoles.manager]})

    parent_assigned_status: Union[str, None] = Field(description="String for user set a status to customer", default=None)
    obs: Union[str, None] = Field(description="String for user set a obs to customer", default=None)

    language: str = Field(description="Language for message translation", default="pt")
    google_sync: bool = Field(description="Activate the google statement synchronization for the current user", default=False)
    institutions: Union[List[UserInstitutionSetting], list, None] = Field(examples=[[UserInstitutionSetting(**{"status":True, "institution_ref": str("65dbfb92b01fc2f7ebe66620"), "email": "a@b.com", "password": "123456"})]], description="Store the user information for the institutions to be integrated", default=[])
    google: Optional[GoogleInformation] = Field(default=GoogleInformation())

    @classmethod
    @field_validator("cellphone")
    def validate_cellphone(cls, cellphone):
        if cellphone is not None:
            return cellphone
        else:
            raise Invalid("cellphone")

    @classmethod
    @field_validator("password")
    def validate_password(cls, password):
        if password is not None:
            if len(password) >= password_min_length:
                return password
            else:
                raise Invalid("password")


    @classmethod
    @field_validator("institutions")
    def valid_institutions(cls, institutions: list):
        result = []

        for institution in institutions:
            if not isinstance(institution, UserInstitutionSetting):
                result.append(UserInstitutionSetting(**institution))
            else:
                result.append(institution)

        return result

    @classmethod
    @field_validator("doc_number")
    def valid_doc_number(cls, value: Union[str, None]):

        if value is not None:
            clean_doc = multireplace(value, from_=junk_doc_chars, to="")
            threshold = len(clean_doc) * 0.9

            if clean_doc.count("0") >= threshold:
                raise Invalid("doc_number")

        return value

    @classmethod
    @field_validator("doc_id_number")
    def valid_doc_id_number(cls, value: Union[str, None]):
        if value is not None:
            clean_doc = multireplace(value, from_=junk_doc_chars, to="")
            threshold = len(clean_doc) * 0.9

            if clean_doc.count("0") >= threshold:
                raise Invalid("doc_id_number")

        return value

    @classmethod
    @field_validator("tax_number")
    def valid_tax_number(cls, value: Union[str, None]):
        if value is not None:
            clean_doc = multireplace(value, from_=junk_doc_chars, to="")
            threshold = len(clean_doc) * 0.9

            if clean_doc.count("0") >= threshold:
                raise Invalid("tax_number")

        return value

    def get_google(self):
        return self.google


class ResponseUserScope(PyBaseModel):

    me: UserRoles = Field()
    groups: list = Field([])


class ResponseUserSonPatch(PyBaseModel):

    email: str = Field(description="Returns the Email: User Reference", examples=[generate_reference()], alias="$email")


class ResponseUserPut(PyBaseModel):

    ref: str = Field(description="Return the user reference")


# noinspection PyClassVar
class ResponseUserGet(UserSonSchema):
    password: ClassVar[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


