import os

import requests
from icecream import ic
from pydantic import EmailStr

from elemental_tools.api.controllers.device import DeviceController
from elemental_tools.api.controllers.user import UserController
from elemental_tools.api.depends import generate_device_fingerprint
from elemental_tools.constants import path_user_post, path_auth_login, path_auth_refresh, path_user_get_me, \
    path_user_put, path_health_check, path_auth_device, path_user_son_patch, path_user_son_get, \
    path_user_son_delete
from elemental_tools.db import select, delete, update
from elemental_tools.exceptions import Unauthorized, NotFound
from elemental_tools.pydantic import UserRoles
from elemental_tools.system import LoadEnvironmentFile

os.environ['elemental-supress-log'] = "TRUE"

LoadEnvironmentFile.validate()

api_url = f"""http://{os.getenv("HOST")}:{os.getenv("PORT")}"""
cookies = {"device-info": "123456789"}

customer_register_json = {
    "tax_number": "00.000.001/0001-00",
    "doc_number": "000.001.001-00",
    "doc_id_number": "00001",
    "name": "string",
    "email": "customer@domain.com",
    "password": "string",
    "phone": "string",
    "cellphone": "string",
    "language": "pt",
    "google_sync": False,
    "institutions": []
}
employee_register_json = {
    "role": UserRoles.employee,
    "doc_id_number": "00002",
    "name": "string",
    "email": "employee@domain.com",
    "password": "string",
    "phone": "554799999999",
    "cellphone": "554799999999",
    "language": "pt",
    "google_sync": False,
    "institutions": []
}


admin_login_headers = {
    "email": "admin@domain.com",
    "password": "administrator"
}
customer_login_headers = {
    "email": customer_register_json["email"],
    "password": customer_register_json["password"]
}

employee_login_headers = {
    "email": employee_register_json["email"],
    "password": employee_register_json["password"]
}

device_controller = DeviceController()
user_controller = UserController()


def _authentication(headers):
    first_login_response = requests.post(f"{api_url}{path_auth_login}", headers=headers, cookies=cookies)

    this_user = user_controller.query(select(user_controller.__orm__).filter_by(email=headers["email"]))
    device_ = None

    if this_user is not None:
        device_ = device_controller.query(
            select(device_controller.__orm__).filter_by(sub=this_user["ref"], status=True))

        if device_ is None:
            device_ = device_controller.query(select(device_controller.__orm__).filter_by(sub=this_user["ref"], status=False))
            if device_ is not None:
                if first_login_response.status_code != Unauthorized.status_code:
                    print(f"MSG: {str(first_login_response.json())}")
                assert first_login_response.status_code == Unauthorized.status_code

                device_auth = requests.put(f"{api_url}{path_auth_device}",
                                           headers={"email": headers["email"], "password": headers["password"],
                                                    "device": device_["ref"]}, cookies=cookies)

                print(f"MSG device_auth: {str(device_auth.json())}")
                assert device_auth.status_code == 200

    auth_login_response = requests.post(f"{api_url}{path_auth_login}", headers=headers, cookies=cookies)

    auth_login_response_json = auth_login_response.json()
    if auth_login_response.status_code != 200:
        print(f"MSG: {str(auth_login_response.json())}\nHeaders:{str(headers)}")

    assert auth_login_response.status_code == 200

    headers = {"access-token": auth_login_response_json["access-token"]}

    auth_refresh_response = requests.post(f"{api_url}{path_auth_refresh}", headers=headers, cookies=cookies)
    auth_refresh_response_json = auth_refresh_response.json()
    if auth_refresh_response.status_code != 200:
        print(f"MSG: {str(auth_refresh_response.json())}")

    assert auth_refresh_response.status_code == 200

    headers["access-token"], headers["refresh-token"] = auth_refresh_response_json["access-token"], auth_refresh_response_json["refresh-token"]

    return headers


def _user_get_me(_login_headers, expected_status: int = 200):
    get_me_response = requests.get(f"{api_url}{path_user_get_me}", headers=_authentication(_login_headers), cookies=cookies)
    get_me_response_json = get_me_response.json()
    if get_me_response.status_code != expected_status:
        print(f"Response: {str(get_me_response_json)}")
    assert get_me_response.status_code == expected_status


def _user_edit(_login_headers: dict, old_email: EmailStr, expected_status: int):
    json_content = {"email": "edit@domain.com"}

    edit_email_response = requests.put(f"{api_url}{path_user_put}", json=json_content,
                                       headers=_authentication(_login_headers), cookies=cookies)
    try:
        user_controller.update(update(user_controller.__orm__).filter_by(**json_content).values(
            email=old_email))
    except Exception as e:
        print(str(e))
    assert edit_email_response.status_code == expected_status


def _user_register_son(_login_headers: dict, register_json: dict, expected_status: int, keep: bool = False):
    user = user_controller.query(select(user_controller.__orm__).filter_by(email=register_json["email"]))

    if user is not None:
        device_controller.delete(delete(device_controller.__orm__).filter_by(sub=user["ref"]))
        user_controller.delete(delete(user_controller.__orm__).filter_by(email=user["email"]))

    auth = _authentication(_login_headers)
    add_son = requests.patch(f"{api_url}{path_user_son_patch}", json=[register_json], headers=auth, cookies=cookies)
    if not keep:
        user_controller.delete(delete(user_controller.__orm__).filter_by(email=register_json["email"]))

    assert add_son.status_code == expected_status


def _user_son_get(_login_headers: dict, expected_status: int):
    sons = requests.get(f"{api_url}{path_user_son_get}", headers=_authentication(_login_headers), cookies=cookies)
    assert sons.status_code == expected_status


def _user_son_delete(_login_headers: dict, expected_status: int):
    delete_user_json = employee_register_json
    delete_user_json["email"] = "delete@domain.com"
    delete_user_json["role"] = UserRoles.customer

    user_controller.delete(delete(user_controller.__orm__).filter_by(email=delete_user_json["email"]))

    # admin son
    add_son = requests.patch(f"{api_url}{path_user_son_patch}", json=[delete_user_json], headers=_authentication(_login_headers), cookies=cookies)
    assert add_son.status_code == expected_status

    if add_son.status_code == 200:
        user_ref = add_son.json()[delete_user_json["email"]]

        son_delete = requests.delete(f"{api_url}{path_user_son_delete}", json=[user_ref], headers=_authentication(_login_headers), cookies=cookies)
        assert son_delete.status_code == 200


def test_health():

    url = f"{api_url}{path_health_check}"
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200


def test_user_register():
    user = user_controller.query(select(user_controller.__orm__).filter_by(email=customer_register_json["email"]))

    if user is not None:
        device_controller.delete(delete(device_controller.__orm__).filter_by(sub=user["ref"]))
        user_controller.delete(delete(user_controller.__orm__).filter_by(email=user["email"]))

    register_response = requests.post(f"{api_url}{path_user_post}", json=customer_register_json, cookies=cookies)

    if register_response.status_code != 200:
        print(f"MSG: {str(register_response.json())}")
    assert register_response.status_code == 200

    customer_register_json["ref"] = register_response.json()["ref"]


def test_user_auth():
    ic(_authentication(customer_login_headers))


def test_admin_auth():
    ic(_authentication(admin_login_headers))


def test_user_get_me():
    _user_get_me(customer_login_headers)
    _user_get_me(admin_login_headers)


def test_user_edit():
    _user_edit(customer_login_headers, customer_login_headers["email"], Unauthorized.status_code)
    _user_edit(admin_login_headers, admin_login_headers["email"], 200)


def test_user_son():
    _user_son_get(customer_login_headers, Unauthorized.status_code)
    _user_son_get(admin_login_headers, 200)

    _user_register_son(customer_login_headers, employee_register_json, Unauthorized.status_code)
    _user_register_son(admin_login_headers, employee_register_json, 200, True)

    _user_son_delete(customer_login_headers, Unauthorized.status_code)
    _user_son_delete(employee_login_headers, Unauthorized.status_code)
    _user_son_delete(admin_login_headers, 200)

    new_user = employee_register_json
    del new_user["role"]
    new_user["email"] = "employeeson@domain.com"
    _user_register_son(employee_login_headers, new_user, Unauthorized.status_code)

    del new_user["doc_id_number"]
    _user_register_son(employee_login_headers, new_user, Unauthorized.status_code)

    del new_user["password"]
    _user_register_son(employee_login_headers, new_user, 200, True)


def test_generate_device_fingerprint():

    postman_headers = {}
    chrome_headers = {}
    safari_headers = {}

