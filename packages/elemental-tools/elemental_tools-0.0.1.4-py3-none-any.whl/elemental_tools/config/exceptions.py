from elemental_tools.logger import Logger
from elemental_tools.tools import get_package_name


class DOTEnvException(Logger):

    def __init__(self, missing: str):

        super().__init__(app_name=get_package_name(__name__), owner="dotenv-exception")
        self.log("critical", f"""Check your .env file for {missing.upper()}. """)


class DOTEnvInstructions(Logger):

    def __init__(self):
        super().__init__(app_name=get_package_name(__name__), owner="cli-instructions")
        self.log("alert", f"""Type elemental --generate_env "path/to/.env" in order to generate a new environment file. """)

