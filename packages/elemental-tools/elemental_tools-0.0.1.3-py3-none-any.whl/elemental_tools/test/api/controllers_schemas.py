import os

from elemental_tools.asserts import root_ref
from elemental_tools.db import SQLModel, select, insert, delete, update
from elemental_tools.test import Test, NewTest
from elemental_tools.system import generate_reference


repeat_times = 1
user_ref = generate_reference()


class UserControllerTest(Test):
    from elemental_tools.api.controllers.user import UserController
    from elemental_tools.api.schemas.user import UserSchema

    _test_controller = UserController()
    _update_ref = generate_reference()
    _new = UserSchema(sub=root_ref(), ref=user_ref, email="user@domain.com", name="Test Company", password="123456789")

    load = [
        NewTest(
            name="elemental_tools.api.controllers.user.__orm__.__tablename__",
            expected_result=True,
            function=lambda x: True if x == "user" else False,
            args=(_test_controller.__orm__.__tablename__,)
        ),
        NewTest(
            name="elemental_tools.api.controllers.user.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=user_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.user.insert",
            expected_result=[(user_ref,)],
            function=lambda controller, stmt: controller.insert(stmt),
            args=(_test_controller, insert(_test_controller.__orm__).values(**_new.model_dump()))
        ),
        NewTest(
            name="elemental_tools.api.controllers.user.query",
            expected_result=True,
            function=lambda controller, stmt, ref: controller.query(stmt)['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=user_ref), user_ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.user.update",
            expected_result=[(_update_ref,)],
            function=lambda controller, stmt: controller.update(stmt),
            args=(_test_controller, update(_test_controller.__orm__).filter_by(ref=user_ref).values(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.user.query_all",
            expected_result=True,
            function=lambda controller, stmt, ref: next(controller.query_all(stmt))['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_update_ref), _update_ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.user.delete",
            expected_result=1,
            function=lambda controller, stmt: controller.delete(stmt),
            args=(_test_controller, delete(_test_controller.__orm__).filter_by(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.user.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_update_ref))
        ),
    ]

    def __init__(self):
        super().__init__(title='elemental_tools.api.controllers.user', supress_log=True, repeat_load=repeat_times)


class DeviceControllerTest(Test):
    from elemental_tools.api.controllers.device import DeviceController
    from elemental_tools.api.schemas.auth import DeviceSchema

    _test_controller = DeviceController()

    _ref = generate_reference()
    _update_ref = generate_reference()

    _new = DeviceSchema(ref=_ref, sub=generate_reference(), fingerprint=generate_reference())

    load = [
        NewTest(
            name="elemental_tools.api.controllers.device.__orm__.__tablename__",
            expected_result=True,
            function=lambda x: True if x == "device" else False,
            args=(_test_controller.__orm__.__tablename__,)
        ),
        NewTest(
            name="elemental_tools.api.controllers.device.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.device.insert",
            expected_result=[(_ref,)],
            function=lambda controller, stmt: controller.insert(stmt),
            args=(_test_controller, insert(_test_controller.__orm__).values(**_new.model_dump()))
        ),
        NewTest(
            name="elemental_tools.api.controllers.device.query",
            expected_result=True,
            function=lambda controller, stmt, ref: controller.query(stmt)['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref), _ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.device.update",
            expected_result=[(_update_ref,)],
            function=lambda controller, stmt: controller.update(stmt),
            args=(_test_controller, update(_test_controller.__orm__).filter_by(ref=_ref).values(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.device.query_all",
            expected_result=True,
            function=lambda controller, stmt, ref: next(controller.query_all(stmt))['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_update_ref), _update_ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.device.delete",
            expected_result=1,
            function=lambda controller, stmt: controller.delete(stmt),
            args=(_test_controller, delete(_test_controller.__orm__).filter_by(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.device.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref))
        ),
    ]

    def __init__(self):
        super().__init__(title='elemental_tools.api.controllers.device', supress_log=True, repeat_load=repeat_times)


class NotificationControllerTest(Test):
    from elemental_tools.api.controllers.notification import NotificationController
    from elemental_tools.api.schemas.notification import NotificationSchema

    _test_controller = NotificationController()

    _ref = generate_reference()
    _sub = root_ref()
    _update_ref = generate_reference()

    _new = NotificationSchema(ref=_ref, sub=_sub, content="")

    load = [
        NewTest(
            name="elemental_tools.api.controllers.notification.__orm__.__tablename__",
            expected_result=True,
            function=lambda x: True if x == "notification" else False,
            args=(_test_controller.__orm__.__tablename__,)
        ),
        NewTest(
            name="elemental_tools.api.controllers.notification.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.notification.insert",
            expected_result=[(_ref,)],
            function=lambda controller, stmt: controller.insert(stmt),
            args=(_test_controller, insert(_test_controller.__orm__).values(**_new.model_dump()))
        ),
        NewTest(
            name="elemental_tools.api.controllers.notification.query",
            expected_result=True,
            function=lambda controller, stmt, ref: controller.query(stmt)['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref), _ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.notification.update",
            expected_result=[(_update_ref,)],
            function=lambda controller, stmt: controller.update(stmt),
            args=(_test_controller, update(_test_controller.__orm__).filter_by(ref=_ref).values(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.notification.query_all",
            expected_result=True,
            function=lambda controller, stmt, ref: next(controller.query_all(stmt))['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_update_ref), _update_ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.notification.delete",
            expected_result=1,
            function=lambda controller, stmt: controller.delete(stmt),
            args=(_test_controller, delete(_test_controller.__orm__).filter_by(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.notification.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref))
        ),
    ]

    def __init__(self):
        super().__init__(title='elemental_tools.api.controllers.notification', supress_log=True, repeat_load=repeat_times)


class InstitutionControllerTest(Test):
    from elemental_tools.api.controllers.institution import InstitutionController
    from elemental_tools.api.schemas.institution import InstitutionSchema

    _test_controller = InstitutionController()

    _ref = generate_reference()
    _update_ref = generate_reference()

    _new = InstitutionSchema(ref=_ref, sub=generate_reference(), tax_number="00.000.001/0001-00", name="test")

    load = [
        NewTest(
            name="elemental_tools.api.controllers.institution.__orm__.__tablename__",
            expected_result=True,
            function=lambda x: True if x == "institution" else False,
            args=(_test_controller.__orm__.__tablename__,)
        ),
        NewTest(
            name="elemental_tools.api.controllers.institution.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.institution.insert",
            expected_result=[(_ref,)],
            function=lambda controller, stmt: controller.insert(stmt),
            args=(_test_controller, insert(_test_controller.__orm__).values(**_new.model_dump()))
        ),
        NewTest(
            name="elemental_tools.api.controllers.institution.query",
            expected_result=True,
            function=lambda controller, stmt, ref: controller.query(stmt)['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref), _ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.institution.update",
            expected_result=[(_update_ref,)],
            function=lambda controller, stmt: controller.update(stmt),
            args=(_test_controller, update(_test_controller.__orm__).filter_by(ref=_ref).values(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.institution.query_all",
            expected_result=True,
            function=lambda controller, stmt, ref: next(controller.query_all(stmt))['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_update_ref), _update_ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.institution.delete",
            expected_result=1,
            function=lambda controller, stmt: controller.delete(stmt),
            args=(_test_controller, delete(_test_controller.__orm__).filter_by(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.institution.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref))
        ),
    ]

    def __init__(self):
        super().__init__(title='elemental_tools.api.controllers.device', supress_log=True, repeat_load=repeat_times)


class SmtpControllerTest(Test):
    from elemental_tools.api.controllers.smtp import SMTPController
    from elemental_tools.api.schemas.smtp import SMTPSchema

    _test_controller = SMTPController()

    _ref = generate_reference()
    _update_ref = generate_reference()

    _new = SMTPSchema(ref=_ref, sub=generate_reference(), server="smtpout.secureserver.net", port=587, email="test@domain.com", password="123456789")

    load = [
        NewTest(
            name="elemental_tools.api.controllers.smtp.__orm__.__tablename__",
            expected_result=True,
            function=lambda x: True if x == "smtp" else False,
            args=(_test_controller.__orm__.__tablename__,)
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.insert",
            expected_result=[(_ref,)],
            function=lambda controller, stmt: controller.insert(stmt),
            args=(_test_controller, insert(_test_controller.__orm__).values(**_new.model_dump()))
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.query",
            expected_result=True,
            function=lambda controller, stmt, ref: controller.query(stmt)['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref), _ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.update",
            expected_result=[(_update_ref,)],
            function=lambda controller, stmt: controller.update(stmt),
            args=(_test_controller, update(_test_controller.__orm__).filter_by(ref=_ref).values(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.query_all",
            expected_result=True,
            function=lambda controller, stmt, ref: next(controller.query_all(stmt))['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_update_ref), _update_ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.delete",
            expected_result=1,
            function=lambda controller, stmt: controller.delete(stmt),
            args=(_test_controller, delete(_test_controller.__orm__).filter_by(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref))
        ),
    ]

    def __init__(self):
        super().__init__(title='elemental_tools.api.controllers.device', supress_log=True, repeat_load=repeat_times)


class StatementControllerTest(Test):
    from elemental_tools.api.controllers.smtp import SMTPController
    from elemental_tools.api.schemas.smtp import SMTPSchema

    _test_controller = SMTPController()

    _ref = generate_reference()
    _update_ref = generate_reference()

    _new = SMTPSchema(ref=_ref, sub=generate_reference(), server="smtpout.secureserver.net", port=587, email="test@domain.com", password="123456789")

    load = [
        NewTest(
            name="elemental_tools.api.controllers.smtp.__orm__.__tablename__",
            expected_result=True,
            function=lambda x: True if x == "smtp" else False,
            args=(_test_controller.__orm__.__tablename__,)
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.insert",
            expected_result=[(_ref,)],
            function=lambda controller, stmt: controller.insert(stmt),
            args=(_test_controller, insert(_test_controller.__orm__).values(**_new.model_dump()))
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.query",
            expected_result=True,
            function=lambda controller, stmt, ref: controller.query(stmt)['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref), _ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.update",
            expected_result=[(_update_ref,)],
            function=lambda controller, stmt: controller.update(stmt),
            args=(_test_controller, update(_test_controller.__orm__).filter_by(ref=_ref).values(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.query_all",
            expected_result=True,
            function=lambda controller, stmt, ref: next(controller.query_all(stmt))['ref'] == ref,
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_update_ref), _update_ref)
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.delete",
            expected_result=1,
            function=lambda controller, stmt: controller.delete(stmt),
            args=(_test_controller, delete(_test_controller.__orm__).filter_by(ref=_update_ref))
        ),
        NewTest(
            name="elemental_tools.api.controllers.smtp.query",
            expected_result=None,
            function=lambda controller, stmt: controller.query(stmt),
            args=(_test_controller, select(_test_controller.__orm__).filter_by(ref=_ref))
        ),
    ]

    def __init__(self):
        super().__init__(title='elemental_tools.api.controllers.device', supress_log=True, repeat_load=repeat_times)


# GroupControllerTest()
DeviceControllerTest()
NotificationControllerTest()
UserControllerTest()
InstitutionControllerTest()
SmtpControllerTest()


