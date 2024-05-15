import os
from time import sleep

from elemental_tools.tools import get_package_name
from elemental_tools.config import config_initializer
from elemental_tools.logger import Logger

profile_limit = 4


class InstallSeleniumGrid:

    config = config_initializer()

    __logger__ = Logger(app_name="elemental-tools", owner=get_package_name(__name__), origin="").log

    if config.enable_grid is True:
        from selenium import webdriver

        # validate for profiles:
        __logger__("installing", "Now we must provide some profile settings...", app_name="grid-setup")
        __logger__("installing", """Remember to run "sudo chmod -R 777" on your volumes folder""", app_name="grid-setup")
        __logger__("profile",
               f"Check your grid vnc and set up {str(profile_limit)} profiles. So we can get started. Remember, I will be checking one by one by one later!",
               app_name="grid-setup")
        __logger__("setting",
               f"I have checked that your chrome data dir is set to: {config.chrome_data_dir}, so we must save this profiles into it.",
               app_name="grid-setup")

        driver_options = config.chrome_options

        driver_options.add_argument(f"user-data-dir={config.chrome_data_dir}")

        __logger__("info", f"Now please provide me some profiles. {str(profile_limit)} to be exact...",
               app_name="grid-setup")
        _b = webdriver.Remote(command_executor=config.webdriver_url, options=driver_options)

        __logger__("info", f"Just press enter when your work is ready to be verified.", app_name="grid-setup")

        input()
        _b.close()
        _c_profile = 0

        for each in os.listdir(config.chrome_data_dir):
            if os.path.isdir(each):
                try:
                    _c_profile += 1
                    _driver_options = config.chrome_options
                    _driver_options.add_argument(f"profile-directory=Profile {str(_c_profile)}")
                    _driver_options.add_argument(f"user-data-dir={config.chrome_data_dir}")
                    _b = webdriver.Remote(command_executor=config.webdriver_url, options=_driver_options)

                    sleep(1)
                    _b.close()
                    sleep(1)
                except Exception as e:
                    raise Exception(
                        f"You're a liar!!! I found a error verifying the profile n {str(_c_profile)}. Get back when you're ready. Or this exception stops happen: {str(e)}")

        __logger__("success", f"All profiles verified.", app_name="grid-setup")

    else:
        raise Exception("You must enable grid-setup on the .env file or in the environment variables to be able to use the selenium grid.")

