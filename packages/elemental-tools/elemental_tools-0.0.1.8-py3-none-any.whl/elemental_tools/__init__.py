import os
from time import sleep
import uvicorn


class API:

    def __init__(self, *script_pydantic_models, enable_task_monitor: bool = False):

        from elemental_tools.config import config_initializer
        from elemental_tools.logger import Logger as _Logger
        from elemental_tools.system import run_cmd as _run_cmd
        from elemental_tools.tools import get_package_name as _get_package_name
        from elemental_tools.patterns import Patterns as _Patterns
        from elemental_tools.pydantic import generate_pydantic_model_from_path as _generate_pydantic_model_from_path

        from elemental_tools.api import Api as _Api
        from elemental_tools.task_monitor import Monitor as _Monitor
        from elemental_tools.system import LoadEnvironmentFile as _LoadEnvironmentFile

        self._run_cmd = _run_cmd
        self.config = config_initializer()
        self._LoadEnvironmentFile = _LoadEnvironmentFile
        self._LoadEnvironmentFile()

        self.__logger__ = _Logger(app_name=self.config.app_name, origin="api", owner=_get_package_name(__name__), destination=self.config.log_path).log
        self.Monitor = _Monitor

        self.app_name = self.config.app_name
        self.enable_task_monitor = enable_task_monitor

        self.script_pydantic_models = {}
        for spm in script_pydantic_models:
            if spm is not None:
                for key, value in spm.items():
                    self.script_pydantic_models[key] = value

        self.app = _Api(script_pydantic_models=self.script_pydantic_models)
        self.task_thread = _Monitor(self.script_pydantic_models)

    def task_monitor(self, cpu_count: int = os.cpu_count()):
        self.__logger__("start", message="Creating Task Monitor Instance...", app_name=self.app_name)
        # the same for the monitor feel free to add as many threads you can
        self.__logger__("start", message="Starting Task Monitor...")
        self.task_thread.run(timeout=2)
        sleep(2)

    def install(self):
        if os.getenv("INSTALL", False):
            self.__logger__("installation", message="Running Database Setup/Upgrade. Remember that you can disable this behaviour by setting the env variable INSTALL to FALSE. See documentation for further information.", app_name=self.app_name)
            self._run_cmd(f"elemental -i -e {str(self._LoadEnvironmentFile.path)}")
            self.__logger__("success", origin="installation", message="Done!", app_name=self.app_name)

    def __call__(self, *args, **kwargs):
        return self.app


class APIServer:

    def __init__(self, *args, **kwargs):
        from elemental_tools.config import config_initializer
        from elemental_tools.logger import Logger as _Logger
        from elemental_tools.tools import get_package_name as _get_package_name

        self.config = config_initializer()

        self.api_specs = {
            "host": self.config.host,
            "port": self.config.port,
            "workers": 1,
            "reload": self.config.debug
        }

        if not self.config.debug:
            self.api_specs["workers"] = self.config.cpu_count

        self.__logger__ = _Logger(app_name=self.config.app_name, origin="api-server", owner=_get_package_name(__name__), destination=self.config.log_path).log
        self.__logger__("start", message="Starting API Server...")

        uvicorn.run(*args, **kwargs, **self.api_specs)

