from datetime import datetime, timedelta
from typing import Union

from icecream import ic

from elemental_tools.logger import Logger
from elemental_tools.config import config_initializer
from elemental_tools.api.orm.task import TableTask
from elemental_tools.db import Index, update, select, text, and_, or_
from elemental_tools.db.controller import Controller
from elemental_tools.exceptions import SaveException
from elemental_tools.system import current_timestamp
from elemental_tools.tools import get_package_name

config = config_initializer()
__logger__ = Logger(app_name=config.app_name, owner=get_package_name(__name__)).log


class TaskController(Controller):
    __orm__ = TableTask
    __logger__ = __logger__

    def set_loop_count(self, ref: str, loops: int):
        self.__logger__('info', f"Setting loop count: {loops} for task ref: {str(ref)} ")

        try:
            _update_result = self.update(update(self.__orm__).filter_by(ref=ref).values(loops=loops))
            if _update_result is None:
                raise SaveException("Task Loop Count")

        except Exception as e:
           self.__logger__('error', f'Cannot set loop count for task because of exception: {str(e)}')

        return False

    def set_last_execution(self, ref: str):
        self.__logger__('info', f'Setting last execution for task ref: {str(ref)}')

        try:
            _current_date = current_timestamp()

            _update_result = self.update(update(self.__orm__).filter_by(ref=ref).values(last_execution=_current_date))

            if not _update_result:
                raise Exception('Cannot set task last execution date.')

        except Exception as e:
            self.__logger__('error', f'Cannot set last execution for task because of exception: {str(e)}')

        return False

    def query_not_processed_tasks(self):

        _current_date = current_timestamp()
        _too_old = datetime.now() - timedelta(days=100)

        stmt_infinite_tasks = select(self.__orm__).filter(
            and_(
                self.__orm__.status,
                self.__orm__.schedule_date == None,
                self.__orm__.timer != None,
                self.__orm__.loops == None
            )
        )

        stmt_new_tasks = select(self.__orm__).filter(
            and_(
                self.__orm__.status == True,
                self.__orm__.last_execution == None,
            )
        )

        _pipeline_functions_counter = [
            {
                '$addFields': {
                    'functionType': 'counter',
                    'currentTime': {'$toLong': {"$toDate": str(_current_date)}},
                    'lastExecutionInMS': {'$toLong': {"$toDate": '$last_execution'}}
                }
            },
            {
                "$match": {
                    "$and": [
                        {'status': True},
                        {"$or": [{'state': None}, {'state': {"$exists": False}}]},
                        {'schedule_date': None},
                        {'timer': {'$ne': None}},
                        {'loops': {'$gt': 0}},
                        {'$expr': {'$gte': [{'$subtract': ['$currentTime', '$lastExecutionInMS']}, '$timer']}}
                    ]
                }
            }
        ]
        _pipeline_functions_infinite = [
            {
                '$addFields': {
                    'functionType': 'infinite',
                    'currentTime': {'$toLong': {"$toDate": str(_current_date)}},
                    'lastExecutionInMS': {'$toLong': {"$toDate": '$last_execution'}}
                }
            },
            {
                "$match": {
                    "$and": [
                        {'$expr': {'$gte': [{'$subtract': ['$currentTime', '$lastExecutionInMS']}, '$timer']}}
                    ]
                }
            }
        ]
        _pipeline_functions_scheduled = [
            {
                '$addFields': {
                    'functionType': 'scheduled',
                    'currentTime': {'$toLong': {"$toDate": str(_current_date)}},
                    'lastExecutionInMS': {'$toLong': {"$toDate": '$last_execution'}}
                }
            },
            {
                "$match": {
                    "$and": [
                        {'status': True},
                        {"$or": [{'state': None}, {'state': {"$exists": False}}]},
                        {'schedule_date': {'$ne': None}},
                        {'$expr': {'$gte': [{'$subtract': ['$currentTime', '$lastExecutionInMS']}, '$timer']}}
                    ]
                }
            }
        ]

        _result = list(self.query_all(stmt_infinite_tasks))
        _result += list(self.query_all(stmt_new_tasks))

        return _result

    def set_status(self, _id: str, status: bool):
        __logger__('info', f'Setting status task _id: {str(_id)}')

        try:
            update_result = self.update(update(self.__orm__).filter_by(ref=_id).values(status=status))
            if update_result is None:
                raise SaveException("Task Status")

        except Exception as e:
            __logger__('error', f'Cannot set task status because of exception: {str(e)}')

        return False

    def set_state(self, _id: str, state: Union[str, None] = None):
        __logger__('info', f'Setting state task _id: {str(_id)}')

        try:
            update_result = self.update(update(self.__orm__).filter_by(ref=_id).values(state=state))
            if update_result is None:
                raise SaveException("Task State")

        except Exception as e:
            __logger__('error', f'Cannot set task state because of exception: {str(e)}')

        return False
