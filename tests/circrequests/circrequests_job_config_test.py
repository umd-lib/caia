import json
import os
import tempfile
from caia.circrequests.circrequests_job_config import CircrequestsJobConfig


def test_denied_keys_file_is_created_if_it_does_not_exist():
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_dir = temp_dir
        config = {
            'storage_dir': storage_dir,
            'last_success_lookup': 'etc/circrequests_FIRST.json',
            'denied_keys_filepath': f"{storage_dir}denied_keys.json"
        }
        job_config = CircrequestsJobConfig(config)
        denied_keys_filepath = job_config['denied_keys_filepath']
        assert os.path.exists(denied_keys_filepath)
        with open(denied_keys_filepath) as denied_keys_file:
            denied_keys = json.load(denied_keys_file)
            assert {} == denied_keys


def test_denied_keys_file_is_not_created_if_already_exists():
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_dir = temp_dir
        config = {
            'storage_dir': storage_dir,
            'last_success_lookup': 'etc/circrequests_FIRST.json',
            'denied_keys_filepath': f"{storage_dir}/denied_keys.json"
        }

        expected_denied_keys = {
            'june15': '2020-06-15T12:50:32.100736',
            'june30': '2020-06-30T12:50:32.100736',
        }
        denied_keys_filepath = os.path.join(storage_dir, "denied_keys.json")

        with open(denied_keys_filepath, "w") as denied_keys_file:
            json.dump(expected_denied_keys, denied_keys_file)

        job_config = CircrequestsJobConfig(config, "test", "test")
        denied_keys_filepath = job_config['denied_keys_filepath']
        print(f"denied_keys_filepath: {denied_keys_filepath}")
        assert os.path.exists(denied_keys_filepath)
        with open(denied_keys_filepath) as denied_keys_file:
            denied_keys = json.load(denied_keys_file)
            assert expected_denied_keys == denied_keys
