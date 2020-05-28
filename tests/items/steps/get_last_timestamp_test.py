from caia.items.items_job_config import ItemsJobConfig
from caia.items.steps.get_last_timestamp import GetLastTimestamp
import pytest


def test_get_last_timestamp_default_timestamp():
    config = {
        'last_success_filepath': 'tests/resources/items/valid_src_response_with_no_entries.json',
        'storage_dir': '/tmp',
        'last_success_lookup': 'tests/storage/items/items_last_success.txt'
    }

    job_config = ItemsJobConfig(config, 'test')

    get_last_timestamp = GetLastTimestamp(job_config)

    step_result = get_last_timestamp.execute()
    assert step_result.was_successful() is True

    last_timestamp = step_result.get_result()
    assert "2020-05-20T23:59:59Z" == last_timestamp


def test_get_last_timestamp_no_timestamp_in_file():
    config = {
        'storage_dir': '/tmp',
        'last_success_lookup': 'tests/storage/items/items_last_success.txt'
    }

    job_config = ItemsJobConfig(config, 'test')
    # Override "last_success_filepath"
    last_success_filepath = 'tests/resources/items/no_timestamp_src_response.json'
    job_config['last_success_filepath'] = last_success_filepath

    get_last_timestamp = GetLastTimestamp(job_config)
    step_result = get_last_timestamp.execute()

    assert step_result.was_successful() is False
    assert f"Could not find timestamp in {last_success_filepath}" in step_result.get_errors()


def test_get_last_timestamp_bad_file():
    config = {
        'storage_dir': '/tmp',
        'last_success_lookup': 'tests/storage/items/items_last_success.txt'
    }

    job_config = ItemsJobConfig(config, 'test')
    # Override "last_success_filepath"
    job_config['last_success_filepath'] = 'tests/resources/items/non_existent_response.json'

    get_last_timestamp = GetLastTimestamp(job_config)

    with pytest.raises(FileNotFoundError):
        get_last_timestamp.execute()
