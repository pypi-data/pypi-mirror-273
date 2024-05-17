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
task_monitor.run(timeout=5)

