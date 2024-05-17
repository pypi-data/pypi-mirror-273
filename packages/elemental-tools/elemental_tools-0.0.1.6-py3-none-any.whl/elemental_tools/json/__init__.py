import importlib
import os.path
import re
import tempfile
import uuid
from typing import Union, Any

import bson
import pandas as pd
from fastapi.encoders import jsonable_encoder

from elemental_tools.constants import ref_length

var_prefix = "$"


class NotSet:
    pass


def retrieve_var_from_df(dataframe: pd.DataFrame, var_name: str, default: Any = None) -> Any:
    """
    Retrieve variable from a DataFrame based on variable name.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame containing variables.
        var_name (str): The name of the variable to retrieve.
        default (Any, optional): Default value to return if variable not found. Defaults to None.

    Returns:
        Any: The value of the variable if found, else default value.
    """
    if var_name in dataframe.columns:
        return dataframe[var_name].iloc[0]  # Assuming the variable is in the first row
    else:
        return default


def retrieve_var_from_json(origin: Union[dict, list], var_name: str, default: Any = NotSet()) -> Any:
    """
    Retrieve variable from a JSON-like object based on variable name.

    Parameters:
        origin (Union[dict, list]): The JSON-like object containing variables.
        var_name (str): The name of the variable to retrieve.
        default (Any, optional): Default value to return if variable not found. Defaults to None.

    Returns:
        Any: The value of the variable if found, else default value.
    """

    if isinstance(origin, dict):

        if var_name in origin:
            return origin[var_name]
    elif isinstance(origin, list):

        for item in origin:
            if isinstance(item, dict):
                if var_name in item:
                    return item[var_name]
            elif isinstance(item, list):
                result = retrieve_var_from_json(item, var_name, default)
                if result is not None:
                    return result

    if isinstance(default, NotSet):
        raise Exception(f"Default Value Not Found for: {var_name}")

    return default


def _subprocess_word(word, origin, default):
    if word.startswith(var_prefix):
        var_name = word.lower().replace(var_prefix, '')
        module = None
        import_statement = None
        if isinstance(origin, str):

            if origin.lower().startswith("from"):
                import_statement = f"{origin}.{var_name}"

            elif origin.lower().startswith("import"):
                import_statement = f"{origin}"

            if import_statement is not None:

                try:
                    if import_statement == "import":

                        module = importlib.import_module(
                            f"elemental_tools.asserts"
                        ).__dict__.get(var_name, None)

                    else:
                        module = importlib.import_module(
                            import_statement
                        )

                except ImportError as ie:
                    if isinstance(default, NotSet):
                        raise ImportError(
                            f"Module '{var_name}' not found in '{import_statement}'.\n\tRaised: {str(ie)}")

        elif isinstance(origin, pd.DataFrame):

            module = retrieve_var_from_df(origin, var_name, default=default)

        elif isinstance(origin, dict) or isinstance(origin, list):

            module = retrieve_var_from_json(origin, var_name, default=default)

        return var_name, module


def apply_variables_on_plain_text(text: str, origin: Union[str, pd.DataFrame] = "import",
                                  default: Any = NotSet()) -> str:
    var_pattern = r"\$[a-zA-Z0-9_]+"
    matches = re.findall(var_pattern, text)
    for word in matches:
        var_name, module = _subprocess_word(word=word, origin=origin, default=default)
        if isinstance(module, str):
            text = text.replace(f"${var_name}", str(module))
        elif callable(module):
            text = text.replace(f"${var_name}", str(module()))
        elif isinstance(module, bytes):
            text = text.replace(f"${var_name}", module.decode())
            text = bytes(text.encode())
    return text



def json_parser(obj: Union[dict, list], bypass_encoder: bool = False):

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                obj[key] = json_parser(value, bypass_encoder)
            elif isinstance(value, bson.ObjectId):
                obj[key] = str(value)
            elif isinstance(value, bytes):
                obj[key] = str(value)
            elif callable(value):
                obj[key] = str(value)
            elif isinstance(value, int):
                pass
            elif isinstance(value, float):
                pass
            elif isinstance(value, bool):
                pass
            else:
                obj[key] = str(value)

    elif isinstance(obj, list):
        for i in range(len(obj)):
            if isinstance(obj[i], (dict, list)):
                obj[i] = json_parser(obj[i], bypass_encoder)
            elif isinstance(obj[i], bson.ObjectId):
                obj[i] = str(obj[i])
            elif isinstance(obj[i], bytes):
                obj[i] = str(obj[i])
            elif callable(obj[i]):
                obj[i] = str(obj[i])
            elif isinstance(obj[i], int):
                pass
            elif isinstance(obj[i], float):
                pass
            elif isinstance(obj[i], bool):
                pass
            else:
                obj[i] = str(obj[i])

    elif isinstance(obj, bson.ObjectId):
        obj = str(obj)
    elif isinstance(obj, bytes):
        obj = str(obj)

    if not bypass_encoder:
        return jsonable_encoder(obj)

    return obj


def json_to_bson(obj: Union[dict, list]):

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                obj[key] = json_to_bson(value)
            elif isinstance(value, str) and ("ref" in key.lower() or "sub" == key.lower() or "access_token" == key.lower() or "refresh_token" == key.lower()):
                if value is not None:
                    try:
                        obj[key] = value.encode()
                    except:
                        obj[key] = value
                else:
                    obj[key] = value
    elif isinstance(obj, list):
        for i in range(len(obj)):
            if isinstance(obj[i], (dict, list)):
                obj[i] = json_to_bson(obj[i])
            elif isinstance(obj[i], str) and len(obj[i]) == ref_length:
                try:
                    obj[i] = obj[i].encode()
                except:
                    obj[i] = obj[i]

    return obj


def json_to_temp_file(obj: Union[dict, list]):
    _file_root_path = tempfile.mkdtemp(prefix="e-json")
    _file_name = str(uuid.uuid4())

    _file_path = os.path.join(_file_root_path, _file_name)

    with open(_file_path, "w") as json_out:
        json_out.write(str(obj))

    return _file_path


def apply_variables_on_json(data: Union[dict, list, str], origin: Union[str, list, dict, pd.DataFrame] = "import", default: Any = NotSet()):
    def apply_variables(value):
        if isinstance(value, str):
            return apply_variables_on_plain_text(text=value, origin=origin, default=default)
        elif isinstance(value, dict):
            for key in list(value.keys()):

                item = value[key]

                a_key = apply_variables_on_plain_text(text=key, origin=origin, default=default)

                a_item = apply_variables_on_json(data=item, origin=origin, default=default)

                del value[key]

                value[a_key] = a_item

            return value

        elif isinstance(value, list):

            return [apply_variables_on_json(data=item, origin=origin, default=default) for item in value]
        else:

            return value

    return apply_variables(data)


def compare_and_get_different_values(dict1, dict2):
    different_values = {}
    for key, value in dict1.items():
        if key in dict2 and dict2[key] != value:
            different_values[key] = (value, dict2[key])
    return different_values

