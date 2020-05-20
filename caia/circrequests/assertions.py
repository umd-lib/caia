import os
from typing import List
from urllib.parse import urlparse
from caia.core.job_config import JobConfig
from json import load, JSONDecodeError


def assert_key_exists(job_config: JobConfig, key: str, errors: List[str]) -> bool:
    """
    Returns True if the given key is in the JobConfig, false otherwise.
    """
    if key in job_config:
        return True
    else:
        errors.append(f"'{key}' is missing")
        return False


def assert_value_not_none(job_config: JobConfig, key: str, errors: List[str]) -> bool:
    """
    Returns True if the value at the given key is not None, False otherwise.
    """
    if not assert_key_exists(job_config, key, errors):
        return False

    value = job_config[key]
    if value is not None:
        return True
    else:
        errors.append(f"'{key}' has a value of None")
        return False


def assert_nonempty_value(job_config: JobConfig, key: str, errors: List[str]) -> bool:
    """
    Returns True if the given key has a value that is not empty or filled
    only with whitespace, False otherwise.
    """
    if not assert_key_exists(job_config, key, errors):
        return False

    if not assert_value_not_none(job_config, key, errors):
        return False

    value = job_config[key]

    result = bool(value.strip())
    if not result:
        errors.append(f"'{key}' has an empty value")

    return result


def assert_directory_exists(job_config: JobConfig, key: str, errors: List[str]) -> bool:
    """
    Returns True if the directory at the given key exists, False otherwise.
    """
    if not assert_key_exists(job_config, key, errors):
        return False

    if not assert_value_not_none(job_config, key, errors):
        return False

    if not assert_nonempty_value(job_config, key, errors):
        return False

    directory = job_config[key]

    result = os.path.isdir(directory)

    if not result:
        errors.append(f"'{key}': '{directory}' does not exist")

    return result


def assert_valid_url(job_config: JobConfig, key: str, errors: List[str]) -> bool:
    """
    Returns True if the given key has a string representing a valid URL,
    False otherwise.
    """
    if not assert_key_exists(job_config, key, errors):
        return False

    if not assert_value_not_none(job_config, key, errors):
        return False

    if not assert_nonempty_value(job_config, key, errors):
        return False

    url = job_config[key]
    try:
        parse_result = urlparse(url)
        if parse_result.scheme and parse_result.netloc and parse_result.path:
            return True
    except ValueError:
        pass

    errors.append(f"'{key}': '{url}' is not a valid URL")
    return False


def assert_file_exists(job_config: JobConfig, key: str, errors: List[str]) -> bool:
    """
    Returns True if the given file exists, False otherwise.
    """

    if not assert_key_exists(job_config, key, errors):
        return False

    if not assert_nonempty_value(job_config, key, errors):
        return False
    file = job_config[key]

    if not os.path.exists(file):
        errors.append(f"'{file}' does not exist")
        return False
    elif not os.path.isfile(file):
        errors.append(f"'{file}' exists but is not a file")
        return False
    else:
        return True


def assert_valid_json_file(job_config: JobConfig, key: str, errors: List[str]) -> bool:
    """
    Returns True if the given file contains parseable JSON, False otherwise.
    """

    if not assert_key_exists(job_config, key, errors):
        return False

    if not assert_nonempty_value(job_config, key, errors):
        return False

    filepath = job_config[key]

    with open(filepath) as file:
        try:
            load(file)
            return True
        except JSONDecodeError:
            errors.append(f"'{filepath}' is not a parseable JSON file")
            return False
