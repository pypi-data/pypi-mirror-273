import os
from elemental_tools.test import Test, NewTest
from elemental_tools.db.controller import Controller
from elemental_tools.db import SQLModel, select, insert, delete, update
from elemental_tools.system import generate_reference


class TestController(Controller):

    def __init__(self, table):
        self.__orm__ = table
        super().__init__()


class TestTable(SQLModel):
    __tablename__ = "test"


class DatabaseTest(Test):
    _test_table = TestTable
    _ref = generate_reference()
    _new_ref = generate_reference()

    load = [
        NewTest(
            name="elemental_tools.db.SQLModel.__tablename__",
            expected_result=True,
            function=lambda x: True if x == "test" else False,
            args=(_test_table.__tablename__,)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller",
            expected_result=_test_table.__tablename__,
            function=lambda table: TestController(table).__orm__.__tablename__,
            args=(_test_table,)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.query",
            expected_result=None,
            function=lambda table, stmt: TestController(table).query(stmt),
            args=(_test_table, select(_test_table).filter_by(ref=_ref),)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.insert",
            expected_result=[(_ref,)],
            function=lambda table, stmt: TestController(table).insert(stmt),
            args=(_test_table, insert(_test_table).values(ref=_ref, sub=_ref),)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.query",
            expected_result=True,
            function=lambda table, stmt, _ref: TestController(table).query(stmt)['ref'] == _ref,
            args=(_test_table, select(_test_table).filter_by(ref=_ref), _ref)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.update",
            expected_result=[(_new_ref,)],
            function=lambda table, stmt: TestController(table).update(stmt),
            args=(_test_table, update(_test_table).filter_by(ref=_ref, sub=_ref).values(ref=_new_ref),)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.query",
            expected_result=None,
            function=lambda table, stmt: TestController(table).query(stmt),
            args=(_test_table, select(_test_table).filter_by(ref=_ref))
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.query",
            expected_result=True,
            function=lambda table, stmt, _new_ref: TestController(table).query(stmt)['ref'] == _new_ref,
            args=(_test_table, select(_test_table).filter_by(ref=_new_ref), _new_ref)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.delete",
            expected_result=True,
            function=lambda table, stmt: TestController(table).delete(stmt) == 1,
            args=(_test_table, delete(_test_table).filter_by(ref=_new_ref, sub=_ref),)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.query_all",
            expected_result=[],
            function=lambda table, stmt: next(TestController(table).query_all(stmt)),
            args=(_test_table, select(_test_table).filter_by(ref=_new_ref),)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.insert",
            expected_result=[(_ref,)],
            function=lambda table, stmt: TestController(table).insert(stmt),
            args=(_test_table, insert(_test_table).values(ref=_ref, sub=_ref),)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.query_all",
            expected_result=_ref,
            function=lambda table, stmt: next(TestController(table).query_all(stmt))["ref"],
            args=(_test_table, select(_test_table).filter_by(ref=_ref),)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.get_status",
            expected_result=False,
            function=lambda table, ref: TestController(table).get_status(ref),
            args=(_test_table, _ref,)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.count_rows",
            expected_result=True,
            function=lambda table: TestController(table).count_rows() >= 1,
            args=(_test_table,)
        ),
        NewTest(
            name="elemental_tools.db.controller.Controller.delete",
            expected_result=True,
            function=lambda table, stmt: TestController(table).delete(stmt) >= 1,
            args=(_test_table, delete(_test_table))
        ),
    ]

    def __init__(self):
        TestController(self._test_table).create_table()
        super().__init__(title='elemental_tools.api.controllers', supress_log=True, repeat_load=repeat_times)


class SettingTest(Test):
    from elemental_tools.system import generate_reference
    from elemental_tools.settings import SettingController, SettingSchema, TableSetting

    _supress_log = True

    _ref = generate_reference()
    _value = generate_reference()
    _name = str(generate_reference())
    _setting_controller = SettingController()

    _sec_value = generate_reference()

    load = [
        NewTest(
            name="SettingController.set",
            expected_result=[(_ref,)],
            function=_setting_controller.test.set,
            kwargs={"sub": _ref, "ref": _ref, "value": _value}
        ),
        NewTest(
            name="SettingController.get",
            expected_result=_value,
            function=_setting_controller.test.get,
            kwargs={"sub": _ref}
        ),
        NewTest(
            name="SettingController.set",
            expected_result=[(_ref,)],
            function=_setting_controller.test.set,
            kwargs={"sub": _ref, "value": _sec_value}
        ),
        NewTest(
            name="SettingController.get",
            expected_result=_sec_value,
            function=_setting_controller.test.get,
            kwargs={"sub": _ref}
        ),
    ]

    def __init__(self):
        super().__init__(title='elemental_tools.settings', supress_log=False, repeat_load=repeat_times)


repeat_times = 1


test_setting = SettingTest
# test_controller = DatabaseTest()


