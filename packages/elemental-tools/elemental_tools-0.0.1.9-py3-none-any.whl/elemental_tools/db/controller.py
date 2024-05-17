import subprocess
from typing import Union, List, Any

from elemental_tools.code import speed_test
from elemental_tools.pydantic import BaseModel
from sqlalchemy.exc import NoSuchModuleError

from elemental_tools.exceptions import MaximumRetryTimesExceeded
from elemental_tools.config import config_initializer
from elemental_tools.db import Connect as Connect, UndefinedTable, ProgrammingError, max_retry_times, inspect
from elemental_tools.db import SQLModel, select, update, insert, delete, func, Result
from elemental_tools.logger import Logger
from elemental_tools.system import run_cmd

config = config_initializer()


class Controller:

    __current_retry__: int = 0
    
    __orm__: SQLModel
    __schema__: BaseModel

    def __init__(self):

        self.__logger__ = Logger(app_name=config.app_name, origin="controller", owner=self.__orm__.__tablename__, debug=config.debug).log

        try:
            self.__database__ = Connect()
        except NoSuchModuleError or TypeError:
            raise Exception("Invalid Database Configuration.\n\tPlease Check The Environment File.")

    def safe_session_execute(self, statement):

        if not self.__current_retry__ <= max_retry_times:

            try:
                session = self.__database__.session(autoflush=True)
                result = session.execute(statement)
                session.commit()

                return result

            except ProgrammingError:

                self.__logger__('alert', "Database Failed. Attempting Database Upgrade...")
                cmd = run_cmd(f'elemental -i', supress=False)
                self.__logger__('success', f"Upgrade Ended Successfully.\n\tResult's: {str(cmd)}")
                self.__current_retry__ += 1
                self.safe_session_execute(statement)

            # except Exception as exc:
            #     pass

            self.__current_retry__ += 1

        else:
            self.__current_retry__ = 0
            raise MaximumRetryTimesExceeded('SQLAlchemy-Cursor')

    def create_table(self):
        self.__database__.create_table()

    def query(self, statement: select) -> Union[dict, Result, None]:
        result = None

        self.__logger__('info', f'Query: {str(statement)}')

        with self.__database__.session() as session:
            result_set = session.execute(statement.limit(1))
            result = result_set.fetchone()
            if result is not None:
                result = result[0].__dict__

        self.__logger__('success', f'Query Executed Successfully!')

        return result

    def query_all(self, statement: select):
        result = None

        self.__logger__('info', f'Query All: {str(statement)}')

        with self.__database__.session() as session:
            result = session.execute(statement)
            if result is not None:
                result = result.fetchall()
                for row in result:
                    yield row[0].__dict__

        self.__logger__('success', f'Query Executed Successfully!')

    def insert(self, statement: insert, upsert: bool = False, index_elements=None):
        result = None

        self.__logger__('info', f'Insert on {self.__orm__.__tablename__}: {str(statement)}')

        if upsert:

            _index_elements = statement.table.primary_key.columns

            if index_elements is not None:
                _index_elements = index_elements

            statement = statement.on_conflict_do_update(
                index_elements=_index_elements,
                set_=statement._values
            )

        with self.__database__.session() as session:
            result = session.execute(statement.returning(self.__orm__.ref))

            if result is not None:
                result = result.fetchall()

            session.commit()

        return result

    def update(self, statement: update) -> Union[list, None]:
        result = None

        self.__logger__('info', f'Update: {statement}')

        with self.__database__.session() as session:
            update_result = session.execute(statement.returning(self.__orm__.ref))
            result = update_result.fetchall()
            session.commit()

        return result

    def delete(self, statement: delete) -> Union[int, None]:
        result = None

        self.__logger__('info', f'Deleting: {str(statement)}')

        with self.__database__.session() as session:
            execution_result = session.execute(statement)
            result = execution_result.rowcount
            session.commit()

        return result

    def get_status(self, ref) -> Union[bool, None]:
        _result = None
        query_result = self.query(select(self.__orm__).filter_by(ref=ref))

        if 'status' in query_result.keys():
            _result = query_result['status']
        if _result is not None:
            return _result

        return False

    def count_rows(self, statement: select = None) -> Union[int, None]:
        count = 0

        try:
            self.__logger__('info', f'Counting Rows on Table: {self.__orm__.__tablename__}')
            with self.__database__.session() as session:

                stmt = self.__orm__.ref
                if statement is not None:
                    stmt = statement

                count = session.query(func.count(stmt)).scalar()
                self.__logger__("success", f"""{count} Rows Counted!""")
        except Exception as e:
            self.__logger__("error", f"""Cannot Count Rows Because Exception: {str(e)}""")

        return count

    def count(self, statement: select) -> Union[int, None]:
        count = 0

        try:
            self.__logger__('info', f'Counting: {statement}')
            with self.__database__.session() as session:
                count = session.query(statement).count()
                self.__logger__("success", f"""{count} Rows Counted!""")
        except Exception as e:
            self.__logger__("error", f"""Cannot Count Rows Because Exception: {str(e)}""")

        return count
