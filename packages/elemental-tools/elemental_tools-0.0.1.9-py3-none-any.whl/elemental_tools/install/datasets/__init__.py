import importlib
import os
from typing import Union

import numpy as np
import pandas as pd
from icecream import ic

from elemental_tools.config import config_initializer
from elemental_tools.asserts import root_ref

from elemental_tools.db import insert
from elemental_tools.exceptions import InvalidExtension
from elemental_tools.json import apply_variables_on_json, json_to_bson
from elemental_tools.logger import Logger

current_file_path = os.path.abspath(__file__)

config = config_initializer()


def newest_version_available(current_folder_path=os.path.dirname(current_file_path)):
    this_version = -1
    with open(os.path.join(current_folder_path, ".version"), 'r') as version_file:
        this_version = int(version_file.read().replace('.', ''))

    return this_version


def install_dataset(session, dataset_path: Union[str, os.PathLike], table_name):
    __logger__ = Logger(app_name=config.app_name, owner='database', origin='installation').log
    __logger__("info", f"Reading JSON {table_name}...")

    if os.path.isfile(dataset_path):

        if dataset_path.upper().endswith('.JSON'):
            df = pd.read_json(dataset_path)
        elif dataset_path.upper().endswith('.CSV'):
            df = pd.read_csv(dataset_path)
        else:
            raise InvalidExtension(dataset_path)

        df = df.replace(np.nan, None)
        data = df.to_dict(orient='records')
        data = apply_variables_on_json(data)

        __logger__("info", f"Inserting {str(data)}")

        # Insert data into the Postgresql Table via Session:
        try:
            module = importlib.import_module(f'elemental_tools.api.orm.{table_name}')
            __orm__ = module.__getattribute__(f"Table{table_name.capitalize()}")
            with session() as db_session:
                db_session.execute(insert(__orm__).values(data))
                db_session.commit()

        except Exception as e:
            __logger__("critical-error", f"Failed because of exception: {e}")
        return True
    else:
        __logger__("alert", f"No dataset found for: {str(dataset_path)}")


