import multiprocessing
import os
import psutil

from typing import Union, List
from uuid import uuid4
from icecream import ic
from tqdm import tqdm
from time import sleep

from elemental_tools.constants import ref_length

from datetime import datetime

from dotenv import load_dotenv

from elemental_tools.logger import Logger
from elemental_tools.tools import get_package_name

# load cache into class
cache_file = './_cache/.dump'
os.environ['TERM'] = "xterm"


def current_timestamp() -> str:
    return datetime.now().isoformat()


def generate_reference(object_id: Union[str, None] = None) -> str:

    res = str(uuid4())[:ref_length]

    if object_id is not None:

        if len(object_id) == ref_length and isinstance(object_id, str):
            res = object_id

        elif len(object_id) > ref_length:
            raise ValueError(f"Failed to Convert Reference due to length restrictions. {str(len(object_id) - ref_length)} chars exceeded.")

    return res


def run_cmd(command, debug: bool = False, supress: bool = True, expected_status: int = 0):
    """
    Execute batch without struggling;

    Args:
        command: The batch command you want to execute
        debug: The log must show additional info (True) or should it run on a stealth mode (False)?
        supress: The stdout must be suppressed (True), indicating no logging at command the prompt result will be placed on the console.
        expected_status: An int that may vary on different OS`s;

    Returns:
        bool: Containing the result of the validation if the command returns the expected_status;
    """
    __logger__ = Logger(app_name=os.getenv('APP_NAME', 'DEF_APP_NAME'), owner='cmd').log

    if supress:
        # Redirect stdout and stderr to /dev/null
        command = f"{command} > /dev/null 2>&1"

    if debug:
        __logger__('info', f'Running command: {command}')
    _exec = os.system(command)
    
    if debug:
        if os.WEXITSTATUS(_exec) == expected_status:
            __logger__('success', os.WEXITSTATUS(_exec))
        else:
            __logger__('error', os.WEXITSTATUS(_exec))

    return os.WEXITSTATUS(_exec) == expected_status


class PerformanceMeter:
    cooldown: float = 0.2
    ram: float = 0.0
    cpu: float = 0.0

    def _tqdm(self):
        with tqdm(total=100, desc='cpu%', position=1) as cpubar, tqdm(total=100, desc='ram%', position=0) as rambar:
            while True:
                self.ram = psutil.virtual_memory().percent
                self.cpu = psutil.cpu_percent()
                rambar.n = self.ram
                cpubar.n = self.cpu
                rambar.refresh()
                cpubar.refresh()
                sleep(self.cooldown)

    def meter(self):

        while True:
            self.ram = psutil.virtual_memory().percent
            self.cpu = psutil.cpu_percent()
            ic(self.ram, self.cpu)
            sleep(self.cooldown)

    def __init__(self):
        multiprocessing.Process(target=self.meter).start()


class Cache:

    def __init__(self, file: str = cache_file):
        self.__cache_file__ = file
        try:
            self.__cache_file_content__ = open(cache_file, 'a+')
        except:
            self.__cache_file_content__ = ""

        if not os.path.isdir(os.path.dirname(os.path.abspath(cache_file))):
            os.makedirs(os.path.dirname(os.path.abspath(cache_file)), exist_ok=True)

        if self.__cache_file_content__.readlines():
            self.__cache_file_content__ = self.load()
            try:
                data = eval(self.__cache_file_content__.read())
                for cache_item in data:
                    for title, value in cache_item.items():
                        setattr(self, title, value)

            except SyntaxError:
                raise Exception("Failed to parse the cache file!")

    def save(self):
        self.__cache_file_content__ = open(cache_file, 'a+')
        self.__cache_file_content__.write(
            str([{title: value for title, value in self.__dict__.items() if not title.startswith('__')}]))
        self.__cache_file_content__.close()
        return open(cache_file, 'a+')

    def load(self):
        return open(self.__cache_file__, 'a+')

    def get(self, prop):
        self.__init__(self.__cache_file__)
        return getattr(self, prop, None)

    def clean(self):
        os.remove(self.__cache_file__)
        self.__cache_file_content__ = open(cache_file, 'a+')


class LoadEnvironmentFile:
    __logger__ = Logger(app_name=os.environ.get("APP_NAME", "elemental-tools"), owner=get_package_name(__name__)).log

    path: str = os.path.join(os.getcwd(), '.env')
    #if os.path.isfile(path):
        #__logger__("initializing", f"Loading dotenv at: {str(path)}")
        #load_dotenv(path)

    def __init__(self, env_path: Union[str, None] = None):
        if os.environ.get('dotenv_path', False):
            self.path = os.environ.get('dotenv_path')
        if env_path is not None:
            self.path = env_path

        self.__logger__("initializing", f"Loading dotenv at: {str(self.path)}")
        load_dotenv(self.path)

    @staticmethod
    def validate():
        return True


class NumeralMenu:
    title: str = None
    description: str = None
    prefix: str = " - "
    suffix: str = ""
    sep: str = "\n"

    __string__: str = ""
    __menu_items__: dict = {}
    __exception__ = lambda: Exception("Invalid Option.")

    def __init__(self, _list: list, prefix: str = " - ", suffix: str = "", sep: str = "\n", title: str = None,
                 description: str = None):

        self.title = title
        self.description = description
        self.suffix = suffix
        self.prefix = prefix
        self.sep = sep

        self.__string__ = ""
        self.__logger__ = Logger(app_name=f"{self.title}", owner="MENU").log

        for idx, e in enumerate(_list):
            self.__string__ += f"\t{idx}{self.prefix}{e}{self.suffix}{self.sep}"
            self.__menu_items__[str(idx)] = e

    def __repr__(self):
        return self.__string__

    def get(self, name_or_num, default=None):

        try:
            return self.__menu_items__[name_or_num]
        except KeyError:
            for val in self.__menu_items__.values():
                if name_or_num == val:
                    return self.__menu_items__

        if default is not None:
            return default
        try:
            raise self.__exception__()
        except TypeError:
            self.__exception__()

    def show(self):

        content = ""
        if self.title is not None:
            content += f"\n[{self.title} - Menu]\n\n"
        content += str(self)
        if self.description is not None:
            content += f"\n{self.description}"

        self.__logger__("WAITING", content)
        os.environ["elemental-supress-log"] = "TRUE"
        user_input = input()
        del os.environ["elemental-supress-log"]

        return user_input


def multireplace(value: str, from_: Union[List[str], str], to: Union[List[str], str]) -> str:
    if isinstance(from_, list):
        for i in range(len(from_)):
            value = value.replace(from_[i], to[i] if isinstance(to, list) else to)
    else:
        if isinstance(to, list):
            for i in to:
                value = value.replace(from_, str(i))
        else:
            value = value.replace(from_, str(to))

    return value


