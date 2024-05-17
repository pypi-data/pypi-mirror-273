import argparse
import multiprocessing
import re
import os
import shutil
import sys
from distutils.dir_util import copy_tree
from typing import Union

import requests

from elemental_tools.dist import version
from elemental_tools.system import NumeralMenu, run_cmd, LoadEnvironmentFile
from elemental_tools.exceptions import TestNotFound

from elemental_tools.file_system import module_path
from elemental_tools.config import config_initializer
from elemental_tools.logger import Logger

further_info = "Type --help for further information."
provide_valid = "Please provide a valid"
sys.tracebacklimit = 0


def get_examples_path(sub_folder) -> os.path:
    abs_examples_path = os.path.join(module_path, 'examples', sub_folder)
    return abs_examples_path


def generate_docker_from_examples(**variables) -> Union[bool, None]:
    abs_examples_path = get_examples_path('docker')
    destination_path: str = variables.get('destination_path', '.')
    if not os.path.isfile(os.path.join(destination_path, 'docker.env')):
        if os.path.isfile(os.path.join(destination_path, '.env')):
            shutil.copy(os.path.join(destination_path, '.env'), os.path.join(destination_path, 'docker.env'))

    files_with_variables = [f for f in os.listdir(abs_examples_path) if os.path.isfile(os.path.join(abs_examples_path, f)) and f.endswith("yml")]
    for file in files_with_variables:
        if os.path.isfile(os.path.join(abs_examples_path, file)):
            with open(os.path.join(abs_examples_path, file), 'r') as ex:
                content = ex.read()

                for variable, variable_content in variables.items():
                    content = content.replace(f"${str(variable)}", str(variable_content))

            if content is not None:

                try:
                    os.makedirs(os.path.abspath(destination_path), exist_ok=True)
                except:
                    raise Exception("Invalid Destination Path")

                with open(os.path.join(os.path.abspath(destination_path), file), 'w') as destination_file:
                    destination_file.write(content)

    for file in [f for f in os.listdir(abs_examples_path) if f not in files_with_variables and os.path.isfile(os.path.join(abs_examples_path, f))]:
        shutil.copy(os.path.join(abs_examples_path, file), os.path.join(destination_path, file))

    for file in [f for f in os.listdir(abs_examples_path) if f not in files_with_variables and os.path.isdir(os.path.join(abs_examples_path, f))]:
        copy_tree(os.path.join(abs_examples_path, file), os.path.join(destination_path, file))

    return True


def main():

    __logger__ = Logger(app_name='elemental-tools', owner='cli').log

    parser = argparse.ArgumentParser(description='Example script with a database flag.')

    # Add the -db flag with a default value
    parser.add_argument('-i', '-install', '--install', '--i', '--upgrade', '--update', action='store_true', help='Create or update the database on the provided host. Check the read-me to see the .env file configurations.\n\tAlways recommended before updating the package itself.')
    parser.add_argument('-u', '-uninstall', '--uninstall', '--u', action='store_true', help='Uninstall Database.')

    parser.add_argument('-start_api', '--start_api', action='store_true', help='Start API.')
    parser.add_argument('-start_task_monitor', '--start_task_monitor', action='store_true', help='Start Task Monitor')

    parser.add_argument('-test_api', '--test_api', action='store_true', help='Test API.')
    parser.add_argument('-test_scripts', '--test_scripts', action='store_true', help='Test Scripts.')

    parser.add_argument('-t', "-test_name", '--test_name', help='Test Name', default=None)

    parser.add_argument('-test', '--test', help='Show Test Menu', action='store_true')
    parser.add_argument('-k', '--keep_running', action='store_true', default=None)
    parser.add_argument('-e', '--env_file', default=None,
                        help='Full path to a basic .env file as described on the read-me.')

    parser.add_argument('-docker', '--docker', '-g_docker', '--g_docker', action='store_true', default=False,
                        help='Generate Docker Files for the API Environment')

    parser.add_argument('-user_folder_path', '--user_folder_path', '-user_path', '--user_path', '-docker_user_folder_path', default=f"{os.getcwd()}/docker_users",
                        help='Folder Path to where you want to persist docker user data.')

    parser.add_argument('-company_name', '--company_name', '-name', default='elemental-tools',
                        help='Company Name for the Installation')

    parser.add_argument('-port', '--port', '-api_port', default=3000,
                        help='API Port for the Installation')

    parser.add_argument('-destination_path', '--destination_path', '-path', '--path', default='.',
                        help='Destination Path. Default = current directory.')

    parser.add_argument('-g_env', '--g_env', default=False,
                        action='store_true', help='Generate a Environment File on -destination_path.')

    parser.add_argument('-g_api', '--g_api', default=False,
                        action='store_true', help='Generate API File System on -destination_path.')

    parser.add_argument('-v', '--version', action='store_true',
                        help='Display package version.')

    # load arguments
    arguments = parser.parse_args()

    if arguments.env_file is None:
        arguments.env_file = '.env'

    LoadEnvironmentFile(arguments.env_file)
    config_initializer(False, True)

    if arguments.install:
        arguments.g_env = True
        arguments.g_api = True
        arguments.docker = True

    if arguments.destination_path == ".":
        arguments.destination_path = os.getcwd()

    arg_dict = arguments.__dict__.copy()
    arg_dict['current_version'] = version

    def install_database():
        if arguments.install and arguments.env_file:
            __logger__('initializing', f'Starting Database Installation')

            __logger__('url', os.getenv("DB_URL"))
            __logger__('name', os.getenv("DB_NAME"))

            if os.getenv("DB_URL") != "" and os.getenv("DB_NAME") != "":
                from elemental_tools.install.database import InstallDatabase

                #try:
                InstallDatabase()
                    # InstallAI().install()

                #except Exception as e:
                #    __logger__('error', f'Installation Failed: {str(e)}')

            else:
                __logger__('error', f'Invalid Database Connection, please check the .env and try again')

        elif arguments.install and not arguments.env_file:
            __logger__('error', f'{provide_valid} .env file via -e argument. {further_info}')

    def generate_dotenv():
        if arguments.g_env:
            config = config_initializer(raise_validation=False)
            config.app_name = arguments.company_name
            config.to_dotenv(os.path.join(os.path.abspath(arguments.destination_path), '.env'))

    def apply_database_settings():
        if arguments.g_env:
            if arguments.company_name == "elemental-tools":
                raise Exception(f"{provide_valid} company_name. {further_info}")

            config = config_initializer(raise_validation=False)
            config.app_name = arguments.company_name

            if arguments.company_name != "elemental-tools" and arguments.env_file and config.db_url != "":
                from elemental_tools.settings import SettingController
                from elemental_tools.asserts import root_ref
                SettingController().company_name.set(sub=root_ref(), value=arguments.company_name)

    def generate_docker():
        if arguments.docker and arguments.company_name != "elemental-tools":
            __logger__('info',
                   f"Generating Docker Files for {arguments.company_name} on path: {os.path.abspath(arguments.destination_path)}")

            generate_docker_from_examples(**arg_dict)
            __logger__('success',
                   f"Docker Files Generated Successfully")

        elif arguments.docker and arguments.company_name == "elemental-tools":
            __logger__('error', f'{provide_valid} company_name. {further_info}')

    def generate_api_files() -> bool:
        if arguments.g_api:
            abs_examples_path = get_examples_path('api')

            available_examples = [f for f in os.listdir(abs_examples_path) if not f.startswith("_")]

            __logger__('info', f"Files to Generate: {str(available_examples)}")

            for file in available_examples:
                if not os.path.isfile(os.path.join(arguments.destination_path, file)):

                    if arguments.destination_path == ".":
                        arguments.destination_path = os.getcwd()
                    __logger__('info', f"Generating File: {os.path.join(arguments.destination_path, file)}")

                    try:
                        os.makedirs(arguments.destination_path, exist_ok=True)
                        __logger__('info', f"Copying from: {os.path.join(abs_examples_path, file)} to: {os.path.join(arguments.destination_path, file)} ")
                        shutil.copy(os.path.join(abs_examples_path, file), os.path.join(arguments.destination_path, file))
                    except Exception as e:
                        __logger__('error', f"Failed to Generate File, due to: {str(e)}")
                else:
                    __logger__('alert', f"File {os.path.join(arguments.destination_path, file)} Already Exists, Skipping...")

            return True

        return False

    def uninstall_database() -> bool:
        if arguments.uninstall:
            from elemental_tools.install.database import UninstallDatabase
            UninstallDatabase()
            return True

    def start_api() -> bool:
        if arguments.start_api:
            from elemental_tools.system import LoadEnvironmentFile
            LoadEnvironmentFile(arguments.env_file)
            from elemental_tools.examples.api.start import api, APIServer

            api.install()
            APIServer("elemental_tools.examples.api.start:api")

            return True

        return False

    def wait_api():
        test_request_status = None

        while not test_request_status == 200:
            try:
                test_request_status = requests.get(
                    f"""http://{os.getenv("HOST")}:{os.getenv("PORT")}/""", cookies={"device-info": "123456789"}).status_code
            except:
                pass

    def start_task_monitor() -> bool:
        if arguments.start_task_monitor:
            import os

            from elemental_tools.config import config_initializer
            from elemental_tools.task_monitor import Monitor
            from elemental_tools.pydantic import generate_pydantic_model_from_path
            from elemental_tools.scripts import internal_scripts

            config = config_initializer()
            # generate pydantic models from the scripts path
            script_pydantic_models = generate_pydantic_model_from_path(config.scripts_root_path)

            # run only task monitor
            task_monitor = Monitor(script_pydantic_models, internal_scripts)
            task_monitor.run()

        return False

    def run_api_test() -> bool:
        __test_root_path__ = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test")

        if arguments.test_name is not None:
            from elemental_tools.examples.api.start import APIServer

            api_process = multiprocessing.Process(target=APIServer,
                                                  args=("elemental_tools.examples.api.start:api",))

            __test_files__ = []
            __available_test__ = {}

            for root, dirs, files in os.walk(__test_root_path__):
                for file_name in files:
                    if file_name == "main.py":
                        __test_files__.append(os.path.join(root, file_name))

            for file in __test_files__:
                with open(file, "r") as test_file:
                    for line in test_file.readlines():
                        if "def test" in line:
                            string = re.sub(r"^def (.+):.*", r"\1", line)
                            string = re.sub(r" -> (.*)\n", r"\1", string)
                            string = re.sub(r"\(.*\)(.*)\n", r"\1", string)
                            string = re.sub(r"\(.*\)(.*)\n", r"\1", string)
                            __available_test__[string] = f"{file}::{string}"

            if arguments.test_name in __available_test__.keys():
                test_path = __available_test__[arguments.test_name]
            else:
                raise TestNotFound(arguments.test_name)

            if "api" in test_path.lower():
                api_process.start()
                wait_api()

            run_cmd(f"pytest {str(test_path)}", supress=False)

            if api_process.is_alive():
                api_process.terminate()

        if arguments.test:
            __subject_menu__ = NumeralMenu(os.listdir(__test_root_path__), title="Test",
                                           description="Choose an option")

            while True:
                selected_subject = __subject_menu__.show()
                if __subject_menu__.get(selected_subject) == "api":
                    from elemental_tools.examples.api.start import APIServer
                    api_process = multiprocessing.Process(target=APIServer,
                                                          args=("elemental_tools.examples.api.start:api",))
                    api_process.start()
                    wait_api()

                __test_path__ = os.path.join(__test_root_path__, __subject_menu__.get(selected_subject), "main.py")

                if not os.path.isfile(__test_path__):
                    raise TestNotFound(selected_subject)

                __test_list__ = []

                with open(__test_path__, "r") as __test_file__:
                    for line in __test_file__.readlines():
                        if "def test" in line:
                            string = re.sub(r"^def (.+):.*", r"\1", line)
                            string = re.sub(r" -> (.*)\n", r"\1", string)
                            string = re.sub(r"\(.*\)(.*)\n", r"\1", string)
                            string = re.sub(r"\(.*\)(.*)\n", r"\1", string)

                            __test_list__.append(string)

                __test_menu__ = NumeralMenu(__test_list__, title="Test",
                                            description="Please Choose Test\nHit Enter to Run Again or CTRL+C to Quit.")

                while True:
                    test_name = __test_menu__.show()
                    __test_menu__.__exception__ = TestNotFound(test_name)

                    try:
                        selected_test = __test_menu__.get(test_name)

                    except TestNotFound:
                        __logger__("info", "Executing Command...")
                        run_cmd(test_name, supress=False)
                        continue

                    if selected_test is not None:
                        test_path = f"{__test_path__}::{selected_test}"

                        run_cmd(f"pytest {str(test_path)}", supress=False)

        elif arguments.test_api:
            from elemental_tools.examples.api.start import api, APIServer
            from elemental_tools.install.database import UninstallDatabase

            if arguments.env_file != ".env":
                from elemental_tools.system import LoadEnvironmentFile
                LoadEnvironmentFile(arguments.env_file)

            os.environ["CPU_COUNT"] = "1"
            os.environ["INSTALL"] = "TRUE"

            if arguments.test_name is None:
                UninstallDatabase()
                api.install()

            api_process = multiprocessing.Process(target=APIServer,
                                                  args=("elemental_tools.examples.api.start:api",))
            api_process.start()
            wait_api()

            __test_path__ = os.path.join(__test_root_path__, "api", "main.py")
            __test_list__ = []

            with open(__test_path__, "r") as __test_file__:
                for line in __test_file__.readlines():
                    if "def test" in line:
                        string = re.sub(r"^def (.+):.*", r"\1", line)
                        string = re.sub(r" -> (.*)\n", r"\1", string)
                        string = re.sub(r"\(.*\)(.*)\n", r"\1", string)
                        string = re.sub(r"\(.*\)(.*)\n", r"\1", string)

                        __test_list__.append(string)

            __test_menu__ = NumeralMenu(__test_list__, title="Test",
                                        description="Please Choose Test\nHit Enter to Run Again or CTRL+C to Quit.")

            if arguments.keep_running is None:
                run_cmd(f"pytest {str(__test_path__)}", supress=False)

            while arguments.keep_running or arguments.keep_running is None:

                if not __test_path__.endswith("None"):

                    wait_api()

                    if arguments.keep_running is not None:

                        test_name = __test_menu__.show()
                        __test_menu__.__exception__ = TestNotFound(test_name)
                        try:
                            selected_test = __test_menu__.get(test_name)
                        except TestNotFound:
                            __logger__("info", "Executing Command...")
                            run_cmd(test_name, supress=False)
                            continue

                        if selected_test is not None:
                            test_path = f"{__test_path__}::{selected_test}"
                            run_cmd(f"pytest {str(test_path)}", supress=False)

                    elif arguments.keep_running is None:
                        break

            api_process.terminate()

            return True

        return False

    def run_scripts_test():
        if arguments.test_scripts:
            print('test')


    # load env file
    if arguments.env_file:
        from dotenv import load_dotenv
        load_dotenv(arguments.env_file)

    # set config for all methods
    if arg_dict['company_name']:
        arg_dict['app_name_pc_friendly'] = arg_dict['company_name'].lower().replace(' ', '_')
        arg_dict['elemental_package_path'] = os.path.dirname(os.path.dirname(__file__))

    if arg_dict['version']:

        print(f"\nVersion: {version}")
        print(f"Location: {os.path.dirname(os.path.dirname(__file__))}\n")

    else:
        generate_dotenv()
        generate_docker()
        generate_api_files()

        uninstall_database()
        install_database()

        apply_database_settings()

        start_api()
        start_task_monitor()
        run_api_test()
        run_scripts_test()
