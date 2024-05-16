import json
import multiprocessing
import os
from typing import List, Any

from icecream import ic

from elemental_tools.code import speed_test
from elemental_tools.code.speed_test import StorageVariable
from elemental_tools.json import json_parser
from elemental_tools.logger import Logger


from elemental_tools.pydantic import BaseModel


class NewTest(BaseModel):
    """
    Represents a test case for a function or method.

    Attributes:
        name (str): The name or description of the test case.
        expected_result (Any): The expected result of the function or method being tested.
        function (callable): The function or method to be tested.
        args (tuple): The positional arguments to be passed to the function or method.
        kwargs (dict): The keyword arguments to be passed to the function or method.

    Note:
        Inherits from `BaseModel`, which is assumed to be a base class providing common functionalities.
    """

    name: str
    description: str = None
    expected_result: Any
    function: Any
    args: tuple = tuple()
    kwargs: dict = {}


class TestResult(BaseModel):
    test_name: str
    result: bool
    function_execution_result: Any
    test_specs: dict
    time_elapsed: float = 0.0
    last_failure_cause: str = None


class Test:
    __logger__ = Logger(app_name='test', owner='result')

    _repeat_load: int = 1
    _supress_log: bool = False
    time_elapsed: float = StorageVariable()
    load: List[NewTest]
    _result: List[TestResult] = []

    def __init__(self, title: str = None, supress_log: bool = False, repeat_load: int = 1):
        self._supress_log = supress_log
        self._repeat_load = repeat_load
        self._title = title
        if self._supress_log:
            os.environ['elemental-supress-log'] = "TRUE"

        self.run()
        self.result()

    def run(self):
        time_elapsed = StorageVariable()

        def __subprocess_test__(logger, supress_log, test) -> TestResult:

            try:
                del os.environ['elemental-supress-log']
            except KeyError:
                pass

            logger.log('test', f"Starting Test: {test.name}\n\tArgs: {str(test.args)}\n\tKwargs: {str(test.kwargs)}")

            if supress_log:
                os.environ['elemental-supress-log'] = 'TRUE'

            @speed_test(store_variable=time_elapsed)
            def func():
                return test.function(*test.args, **test.kwargs)

            function_execution_result = func()

            new_result = TestResult(
                test_name=test.name,
                result=test.expected_result == function_execution_result,
                function_execution_result=str(function_execution_result),
                test_specs=json_parser(test.model_dump(), bypass_encoder=True),
            )

            return new_result

        for repeat in range(self._repeat_load):
            for test in self.load:
                new_result = __subprocess_test__(self.__logger__, self._supress_log, test)

                new_result.time_elapsed = time_elapsed.as_float()
                new_result.last_failure_cause = {
                    "Mismatch": {
                        "Function Result": str(new_result.function_execution_result),
                        "Expected Result": str(test.expected_result)
                    }
                }

                self._result.append(new_result)
                self.__logger__.log('test-result', json.dumps(json_parser(new_result.__dict__, bypass_encoder=True), indent=4))

        return self._result

    def result(self):
        _res_master = {

        }

        for res in self._result:

            if not res.test_name in _res_master.keys():
                _res_master[res.test_name] = {}
                _res_master[res.test_name]['Passed'] = 0
                _res_master[res.test_name]['Failed'] = 0
                _res_master[res.test_name]['Time Elapsed'] = 0

            _res_master[res.test_name]['Time Elapsed'] += res.time_elapsed
            _res_master[res.test_name]['Passed'] += bool(res.result)
            _res_master[res.test_name]['Failed'] += not bool(res.result)

            if _res_master[res.test_name]['Failed']:
                _res_master[res.test_name]['Last Failure Cause'] = res.last_failure_cause

            try:
                del os.environ['elemental-supress-log']
            except KeyError:
                pass

        self.__logger__.log('test-result', json.dumps(json_parser(_res_master, bypass_encoder=True), indent=4), origin=self._title)

        return _res_master

