import logging
import multiprocessing
import os

from datetime import datetime
from time import sleep
from typing import Union

from elemental_tools.design import UnicodeColors

bind_logs = []


def relative(path):
    return os.path.join(os.path.dirname(__file__), path)


class Logger:
    last_level = None
    clean = False
    master_clean = False
    environment = None
    log_path = None
    __color__ = {
        "INFO": UnicodeColors.success_cyan,
        "START": UnicodeColors.pink, "INITIALIZING": UnicodeColors.pink, "WAITING": UnicodeColors.pink,
        "WARNING": UnicodeColors.alert, "ALERT": UnicodeColors.alert,
        "SUCCESS": UnicodeColors.success, "OK": UnicodeColors.success,
        "CRITICAL": UnicodeColors.fail, "ERROR": UnicodeColors.fail, "FAULT": UnicodeColors.fail, "FAIL": UnicodeColors.fail, "FATAL": UnicodeColors.fail,
        "TEST": UnicodeColors.purple, "TESTING": UnicodeColors.purple,
        "TEST-RESULT": UnicodeColors.bright_purple, "INSTALLING": UnicodeColors.bright_purple, "INSTALLATION": UnicodeColors.bright_purple
    }

    def __init__(self, app_name: str, owner: str, destination: str = None, debug: bool = True, clean: bool = False,
                 **kwargs):

        self.kwargs = kwargs

        if clean:
            self.master_clean = True

        self.app_name_upper = 'ELEMENTAL-TOOLS'

        if app_name is not None and app_name:
            self.app_name_upper = str(app_name).upper()

        self.path = destination
        self.debug = debug
        self.owner = owner

        if debug:
            self.environment = "debug"

    def generate_log_path(self, timestamp) -> Union[str, None]:
        if self.path is not None and str(self.log_path) != "None":
            if self.environment is not None:
                try:
                    str_path = str(self.path) + f"_{self.environment}"
                except TypeError:
                    str_path = os.path.join('.', f"log_{self.environment}")
            else:
                str_path = str(self.path)

            try:
                os.makedirs(str_path, exist_ok=True)
            except:
                pass

            filename = timestamp.strftime('%d-%m-%Y') + ".log"
            str_path = os.path.join(str_path, filename)
            sleep(0.5)

            return str_path

    def _process_log(self, level: str, message, app_name: str = None, clean: bool = False, supress: bool = False, debug: bool = True, **kwargs):
        """

        Args:
            level:
            message:
            app_name:
            clean:
            supress:
            **kwargs:

        Returns:
        """
        if self.clean:
            os.system('cls' if os.name == 'nt' else 'clear')
            if not self.master_clean:
                self.clean = False

        timestamp = datetime.now()
        level = str(level).upper()
        owner = str(self.owner).upper()

        _current_app = self.app_name_upper

        if app_name is not None and app_name:
            _current_app = str(app_name).upper()

        message_enclose = timestamp.strftime("%d-%m-%Y %H:%M:%S") + f" - [{_current_app}]" + f" [{owner}]" + ' ' + ' '.join(
            [f'[{str(item).upper()}]' for item in [*self.kwargs.values()]]) + ' '.join(
            [f'[{str(item).upper()}]' for item in [*kwargs.values()]]) + f" [{level}]"

        content = f"\n{message_enclose.replace('  ', ' ')}: {str(message)}"

        if self.last_level != level:
            self.correspondent_clr = self.__color__.get(level, None)
            if self.correspondent_clr is None:
                self.correspondent_clr = UnicodeColors.reset

            self.last_level = level

        if clean:
            self.clean = True

        if not supress or debug or self.debug:
            if self.path is not None and str(self.path) != "None" and str(self.path) != "":
                print(self.path)
                with open(self.generate_log_path(timestamp), 'a+') as f:
                    f.write(str(content[1:]) + "\n")

            content = self.correspondent_clr + content[1:] + UnicodeColors.reset + "\n"
            os.write(1, content.encode())

            # if clean:
            #     self.clean = True

    def log(self, level: str, message, app_name: str = None, clean: bool = False, supress: bool = False, debug: bool = True, **kwargs):
        """

        Args:
            level:
            message:
            app_name:
            clean:
            supress:
            debug:
            **kwargs:

        Returns:

        """

        if self.debug and debug:
            if not bool(supress):
                self._process_log(level, message, **{"app_name": app_name, "clean": clean, "supress": supress, "debug": debug})

        #return self

    @classmethod
    def set_logger(cls, logger_name, handler):
        if logger_name not in bind_logs:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(message)s')
            custom_handler = handler()
            custom_handler.setFormatter(formatter)
            logger.addHandler(custom_handler)
            bind_logs.append(logger_name)

    def get_logger(self, logger_name: str, level: str, clean: bool = False, supress: bool = False, debug: bool = True,
                   **kwargs):

        class Handler(logging.Handler):

            log = self.log

            def __init__(self):
                # Initialize the base class
                super().__init__()

            def emit(self, record) -> None:
                if not bool(os.environ.get("elemental-supress-log", default=False)):
                    self.log(level, origin=logger_name, message=str(self.format(record)), clean=clean, supress=supress,
                             debug=debug, **kwargs)

        if all([self.debug, debug]):
            multiprocessing.Process(target=self.set_logger, args=(logger_name, Handler)).run()
