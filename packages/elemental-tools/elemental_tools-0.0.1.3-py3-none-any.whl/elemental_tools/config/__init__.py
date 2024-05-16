import json
import os
import random
import string
import sys
from json import JSONDecodeError
from typing import Optional, Union

from fastapi import BackgroundTasks
from pydantic import BaseModel, Field, field_validator, ValidationError, PrivateAttr
from pydantic_core.core_schema import ValidationInfo
from selenium.webdriver.chrome.options import Options

from elemental_tools.config.exceptions import DOTEnvException, DOTEnvInstructions
from elemental_tools.logger import Logger
from elemental_tools.tools import get_package_name
from elemental_tools.system import LoadEnvironmentFile

cache = {}


class BaseConfig:
    """
    A class for managing configuration settings and persisting them to a file.

    Attributes:
        target (args):
        _debug (bool): Flag indicating whether debug mode is enabled.
        _path (str): Path to the configuration file.

    Methods:
        __init__(): Initializes the Config object by loading configuration from file.
        _dump(): Serializes the non-private attributes to JSON and writes to the config file.
        _load(): Loads configuration from the config file, or creates a new one if not found.
        update_config(**kwargs): Updates configuration settings with new values and writes them to file.
    """
    _debug: bool = True
    _path: str = os.path.join(os.path.abspath('./'), '.config')
    _log: Logger.log = Logger(app_name='system', owner='config').log
    _loaded: bool = False

    def __init__(self, *target):
        """
        Initializes the Config object by loading configuration from file.

        Parameters:
            target (Union[object, callable]): Methods or Classes to bound the config.\
             So whenever the config changes, the assigned items gets propagated to its bound Methods and Classes;

        """
        self._target = target
        self._load()

    def _dump(self):
        """
        Serializes the non-private attributes to JSON and writes to the config file.
        """
        content = self._attributes()

        with open(self._path, 'w') as config_file:
            json.dump(content, config_file, indent=4)

    def __setattr__(self, key, value):

        object.__setattr__(self, key, value)
        if self._loaded:
            self._dump()

    def _load(self):
        """
        Loads configuration from the config file, or creates a new one if not found.
        """

        _path = object.__getattribute__(self, '_path')
        _dump = object.__getattribute__(self, '_dump')
        _targets = [*object.__getattribute__(self, '_target')]
        _attributes = object.__getattribute__(self, '_attributes')().items
        __logger__ = object.__getattribute__(self, '_log')

        try:
            with open(_path, 'r') as config_file:
                try:
                    content = json.load(config_file)
                    # Assign loaded values to class attributes
                    for name, value in content.items():
                        object.__setattr__(self, name, value)

                except JSONDecodeError as json_e:
                    _dump()

        # If the file doesn't exist, dump default configuration
        except FileNotFoundError as file_e:
            _dump()

        for target in _targets:
            for attr, value in _attributes():
                try:
                    __logger__('info', f'Assigning Config: {attr} to {value}', origin=target)
                    object.__setattr__(target, attr, value)
                    __logger__('success', f'Config Assigned', origin=target)
                except AttributeError as e:
                    __logger__('alert', f'Failed Assigning {attr}: {str(e)}', origin=target)

        for attr, value in _attributes():
            try:
                __logger__('info', f'Assigning Config: {attr} to {value}')
                object.__setattr__(self, attr, value)
                __logger__('success', f'Config Assigned')
            except AttributeError as e:
                __logger__('alert', f'Failed Assigning {attr}: {str(e)}')

        object.__setattr__(self, '_loaded', True)

    def _attributes(self):
        content = {name: value for name, value in object.__getattribute__(self, '__dict__').items() if
                   not name.startswith('_') and not name == 'update_config'}
        return content

    def __getattr__(self, attr):
        self._load()
        return None

    def __getattribute__(self, item):
        object.__getattribute__(self, '_load')()
        return object.__getattribute__(self, item)


class _Config(BaseModel, extra="allow", arbitrary_types_allowed=True):
    _bg_task: BackgroundTasks = PrivateAttr(default_factory=BackgroundTasks)

    app_name: str = Field(default="elemental-tools")
    __logger__ = Logger(app_name=os.environ.get("APP_NAME", "elemental-tools"), owner=get_package_name(__name__)).log

    # system
    install: bool = Field(default=False)
    cpu_count: int = Field(default=1)

    log_path: Union[str, None] = Field(default=None)
    envi: Union[str, None] = Field()
    debug: Union[str, bool, None] = Field()

    enable_local_adb: bool = Field()

    db_url: str = Field()
    db_name: Union[str, None] = Field(default=None)

    # api
    host: str = Field(default=os.environ.get("HOST", "127.0.0.1"))
    port: int = Field(default=int(os.environ.get("PORT", 10200)))

    scripts_root_path: str = Field(default=os.environ.get("SCRIPTS_ROOT", "scripts"))
    download_path: str = Field(default=os.environ.get("DOWNLOAD_PATH", "/tmp/downloads"))

    def __init__(self, _raise_validation: bool = True, **kwargs):
        try:
            super().__init__(**kwargs)
        except ValidationError as exc:
            if _raise_validation:
                errors = exc.errors()
                for e in errors:
                    DOTEnvException(e["loc"][0])

                DOTEnvInstructions()
                sys.exit(0)
            else:
                kwargs["db_url"] = ""
                kwargs["envi"] = "debug"
                kwargs["enable_local_adb"] = True

                super().__init__(**kwargs)

        self.__logger__ = Logger(app_name=self.app_name, owner=get_package_name(__name__), destination=self.log_path).log

        self.__logger__("info", "Loading secrets and keys, shhh...")
        self.binance_key: str = os.environ.get("BINANCE_KEY", None)
        self.binance_secret: str = os.environ.get("BINANCE_SECRET", None)

        self.b4u_url: str = os.environ.get("B4U_API_URL", None)
        self.b4u_key: str = os.environ.get("B4U_API_KEY", None)
        self.b4u_secret: str = os.environ.get("B4U_API_SECRET", None)
        self.__logger__("success", "The configuration secrets were successfully set.")

        if not os.path.isdir(self.download_path):
            self.__logger__("info", "Ensuring Download Path...")

            try:
                os.makedirs(self.download_path, exist_ok=True)
                self.__logger__("success", "Download Path Available!")
            except:
                self.__logger__("alert",
                                f"Failed to generate Download Folder at: {str(self.download_path)}. If you will gonna need it, please check write permissions on the desired folder or change the environment variable DOWNLOAD_PATH.")

    @field_validator("envi")
    @classmethod
    def valid_envi(cls, value):
        if value is None:
            cls.__logger__("info", "Setting Environment (debug, production) based on platform.")

            if sys.platform == "darwin" or sys.platform == "win32":
                return "debug"
            else:
                return "production"

        cls.__logger__("success", "The current environment is set to " + value)
        return value

    @field_validator("db_name")
    @classmethod
    def valid_db_name(cls, input_value, values: ValidationInfo):
        if input_value is None:
            return str(values.data["app_name"] + f"""_{values.data["envi"]}""")
        return input_value

    @field_validator("debug")
    @classmethod
    def valid_debug(cls, input_value, values: ValidationInfo) -> bool:
        if input_value is None and values.data["envi"] == "debug" or input_value.upper() == "TRUE":
            return True

        return False

    @field_validator("install")
    @classmethod
    def valid_install(cls, input_value, values: ValidationInfo) -> bool:
        if input_value is None and values.data["debug"] or input_value.upper() == "TRUE":
            return True

        return False

    def __selenium__(self):
        self.__logger__("info", "Initializing Chrome configuration")
        self.enable_grid: bool = os.environ.get("ENABLE_GRID", False)
        self.webdriver_url: str = os.environ.get("WEBDRIVER_URL", "http://localhost:4444/")
        self.chrome_data_dir: str = os.environ.get("CHROME_USER_DATA_DIR", "/tmp")
        self.chrome_options: Options = Options()

        self.chrome_options.add_argument("start-maximized")
        self.user_data_dir: str = ''.join(random.choices(string.ascii_letters, k=8))
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-software-rasterizer")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.__logger__("success", "Chrome was configured successfully!")

    @classmethod
    def to_dotenv(cls, path):

        __logger__ = Logger(app_name=os.environ.get("APP_NAME", "elemental-tools"), owner=get_package_name(__name__)).log

        if not os.path.isfile(path):
            __logger__("info", f"Exporting Dotenv to: {path}")
            with open(path, "w") as dest:
                for key, value in cache["conf"].model_dump().items():
                    if not str(key).startswith("_"):
                        if str(value) == "None":
                            value = ""

                        dest.write(f"{str(key).upper()}={value}\n")

                __logger__("success", f"Dotenv saved at: {path}")

        else:
            __logger__("alert", f"Dotenv already exists. Skipping...")


def config_initializer(raise_validation: bool = True, reload: bool = False) -> _Config:

    if cache.get("conf", None) is None or reload:
        if not reload or cache.get("conf", None) is None:
            LoadEnvironmentFile()

        __logger__ = Logger(app_name=os.environ.get("APP_NAME", "elemental-tools"), owner=get_package_name(__name__)).log

        LoadEnvironmentFile.validate()

        cache["conf"] = _Config(
            _raise_validation=raise_validation,
            _bg_task=BackgroundTasks(),
            cpu_count=os.environ.get("CPU_COUNT", os.cpu_count()),
            app_name=os.environ.get("APP_NAME", "elemental-tools"),
            log_path=os.environ.get("LOG_PATH", None),
            envi=os.environ.get("ENVIRONMENT", None),
            debug=os.environ.get("DEBUG", None),
            enable_local_adb=os.environ.get("ENABLE_LOCAL_ADB", False),
            db_url=os.environ.get("DB_URL", None),
            db_name=os.environ.get("DB_NAME", None),
            host=os.environ.get("HOST", "127.0.0.1"),
            port=int(os.environ.get("PORT", 10200)),
            scripts_root_path=os.environ.get("SCRIPTS_ROOT", "scripts"),
            download_path=os.environ.get("DOWNLOAD_PATH", "/tmp/downloads"),
        )

        __logger__("success", "Config Loaded!")

    return cache["conf"]

