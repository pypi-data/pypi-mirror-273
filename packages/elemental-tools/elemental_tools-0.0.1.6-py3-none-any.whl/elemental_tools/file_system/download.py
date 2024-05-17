import os
import re
import tempfile

import pandas as pd
import requests
from requests import ReadTimeout

from elemental_tools.config import config_initializer
from elemental_tools.file_system import is_file_format
from elemental_tools.file_system.extensions import CSV, JSON, HTML
from elemental_tools.logger import Logger


config = config_initializer()
__logger__ = Logger(app_name=config.app_name, owner='file-system', origin='download').log


def search_csv_download_and_load(url, debug: bool = True, _retrying: bool = False, retry_times: int = 3, sub_levels: int = 5, csv_limit: int = 128000, timeout: int = 2):
    __logger__('info', 'Initializing CSV Scrape', debug=debug)
    csv_content = None

    def retrieve_children_csv_url(content: str):
        __logger__('info', 'Retrieving Possible Nested Links...', debug=debug)
        pattern = r'"(https?://[^"]+\.csv(?:\?raw=true)?)\"'
        csv_urls = re.findall(pattern, content)

        if len(csv_urls):
            __logger__('success', f'Nested Links Found: {str(len(csv_urls))}', debug=debug)
        else:
            if len(csv_urls):
                __logger__('alert', f'No Nested Links Found at: {url}', debug=debug)

        return csv_urls

    # Download the file
    __logger__('info', f'Get on: {url}', origin='REST-Request', debug=debug)
    try:
        response = requests.get(url, timeout=timeout)

        if response.status_code != 200:
            __logger__('alert', f'Response Status Code is Throwing an Error', origin='REST-Request', debug=debug)
            raise ValueError(f"Failed to download file from {url}")
    except ReadTimeout:
        __logger__('alert', f'Server Takes Too Long to Respond', origin='REST-Request', debug=debug)
        return None

    __logger__('success', f"Get Executed Successfully!", origin='REST-Request', debug=debug)

    __logger__('info', f"Validating if file is CSV", debug=debug)
    if is_file_format(response.text) == CSV:
        __logger__('success', f"File is CSV", debug=debug)
        if not _retrying:
            csv_content = response.text
        else:
            return response.text

    elif is_file_format(response.text) == HTML or is_file_format(response.text) == JSON:
        __logger__('info', f"Searching for peripheral links...", debug=debug)
        this_level = 0
        for possible_url in retrieve_children_csv_url(response.text):
            __logger__('info', f"Validating Relevance on Link: {possible_url}", debug=debug)
            this_level += 1
            if this_level < sub_levels:
                csv_content = search_csv_download_and_load(url=possible_url, _retrying=True)
                if is_file_format(csv_content) == CSV:
                    __logger__('info', f"Valid CSV Content Found!", debug=debug)
                    break
            else:
                break

    if csv_content is not None:
        __logger__('info', f"Validating CSV Content Length Limit", debug=debug)

    if csv_content is not None and len(csv_content) <= csv_limit:
        # Create a temporary file to store the content
        __logger__('info', f"Writing CSV Content on Temporary File", debug=debug)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            temp_file.write(csv_content.encode('utf-8'))

        __logger__('success', f"CSV File Downloaded!", debug=debug)
        try:
            __logger__('info', f"Reading CSV File Content to Dataframe...", debug=debug)
            # Load content into pandas DataFrame
            df = pd.read_csv(temp_file.name)
            __logger__('success', f"CSV File Loaded to Dataframe", debug=debug)
            # Remove the temporary file
            os.unlink(temp_file.name)

            return df

        except:
            return None


