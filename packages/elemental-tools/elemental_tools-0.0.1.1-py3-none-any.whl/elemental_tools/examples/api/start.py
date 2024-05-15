import os

from elemental_tools import API, APIServer
from elemental_tools.config import config_initializer
from elemental_tools.pydantic import generate_pydantic_model_from_path
from elemental_tools.scripts import internal_scripts

config = config_initializer()

# generate pydantic models from the scripts path
script_pydantic_models = generate_pydantic_model_from_path(config.scripts_root_path)

# start the scriptize api
api = API(script_pydantic_models, internal_scripts)


if __name__ == "__main__":
    api.install()

    APIServer("start:api")


