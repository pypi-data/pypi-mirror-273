from typing import List, Annotated, Union

from fastapi import Depends, Header
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from elemental_tools.constants import path_smtp_get, path_smtp_get_config, path_smtp_patch
from elemental_tools.api.controllers.smtp import SMTPController
from elemental_tools.api.controllers.user import UserController
from elemental_tools.api.depends import auth, pagination
from elemental_tools.api.schemas.pagination import PaginationSchema
from elemental_tools.api.schemas.smtp import SMTPSchema
from elemental_tools.api.schemas.user import UserSchema
from elemental_tools.config import config_initializer
from elemental_tools.exceptions import SaveException
from elemental_tools.logger import Logger
from elemental_tools.smtp import SendEmail
from elemental_tools.tools import get_package_name

router = APIRouter()

config = config_initializer()

user_controller = UserController()
smtp_controller = SMTPController()


__logger__ = Logger(app_name='api-endpoint', owner=get_package_name(__name__), destination=config.log_path).log


tags = ["SMTP"]


@router.get(path_smtp_get, tags=tags, description="Query SMTP List. With basic info such as smtp ID and it's email.")
async def get_smtp(_user: Annotated[UserSchema, Depends(auth)], pagination: Annotated[PaginationSchema, None] = Depends(pagination), sub: Union[str, None] = Header(description="User ID", default=None)):

    _result = smtp_controller.retrieve_all_smtp_config_list(_user, sub)

    result = []
    if len(_result):
        result = pagination.get_page(_result)

    return JSONResponse(content=result, status_code=200)


@router.get(path_smtp_get_config, tags=tags, description="Query SMTP Server Config")
async def get_smtp_config(_user: Annotated[UserSchema, Depends(auth)], pagination: Annotated[PaginationSchema, None] = Depends(pagination), sub: Union[str, None] = Header(description="User ID", default=None)):

    _result = smtp_controller.retrieve_all_smtp_config_list(_user, sub, supress_sensitive_data=False)

    result = []
    if len(_result):
        result = pagination.get_page(_result)

    return JSONResponse(content=result, status_code=200)


@router.patch(path_smtp_patch, tags=tags, description="Add or Edit SMTP Server Config")
async def add_smtp(body: List[SMTPSchema], _user: Annotated[UserSchema, Depends(auth)]):

    try:
        _result = {}
        _success_count = 0
        _failed_count = 0

        every_sub_user_can_edit = [company.company_ref for company in _user.companies if company.role in ['owner', 'editor']]
        every_sub_user_can_edit.append(_user._ref)

        for smtp_to_add in body:

            if smtp_to_add.sub is None:
                smtp_to_add.sub = _user._ref
            
            if smtp_to_add.sub in every_sub_user_can_edit:

                _test_send_email = SendEmail(smtp_to_add.email, smtp_to_add.password, smtp_to_add.server, smtp_to_add.port)
                
                # update or insert smtp to user model if smtp config is valid
                _smtp_is_valid = _test_send_email.check_config()
                
                if _smtp_is_valid:
                    smtp_to_add.status = True

                    _success_count += 1
                else:

                    _failed_count += 1

        result = {"items_failed": []}
        try:

            result += {"insert_items": len(smtp_controller.add([smtp_to_add.model_dump() for smtp_to_add in body if
                                                                smtp_to_add.status and smtp_to_add.ref is None]).inserted_ids)}
        except:
            pass

        try:
            update_result = smtp_controller.bulk_update(selectors=[{"ref": smtp_to_add.ref} for smtp_to_add in body if smtp_to_add.status and smtp_to_add.ref is not None], contents=[smtp_to_add.model_dump() for smtp_to_add in body if smtp_to_add.status and smtp_to_add.ref is not None], upsert=True)
            result += {"modified": update_result.modified_count, "matched": update_result.matched_count, "upserted": update_result.upserted_count}
            
        except:
            pass

        for smtp_conf in body:
            
            if not smtp_conf.status:
                
                _this_smtp = smtp_conf.model_dump()
                del _this_smtp["password"]
                result["items_failed"].append(_this_smtp)

    except Exception as e:
        raise SaveException("SMTP", exception="No valid configuration was found.")

    return JSONResponse(content={"count": _success_count, "result": result, "failed": _failed_count}, status_code=200)

