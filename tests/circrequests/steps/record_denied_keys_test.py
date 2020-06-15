import json
import os
import tempfile

from caia.circrequests.steps.record_denied_keys import RecordDeniedKeys


def test_no_denied_keys(mock_server):
    with open("tests/resources/circrequests/valid_dest_response.json") as file:
        valid_dest_response = file.read()

    try:
        # Create a temporary file to use as denied keys file
        [temp_denied_keys_file_handle, temp_denied_keys_filename] = tempfile.mkstemp()
        config = {
            'denied_keys_filepath': temp_denied_keys_filename
        }

        record_denied_keys = RecordDeniedKeys(config, valid_dest_response)
        step_result = record_denied_keys.execute()
        assert step_result.was_successful() is True
    finally:
        # Clean up the temporary file
        os.close(temp_denied_keys_file_handle)

        # Verify that "denied keys" file contains empty list
        with open(temp_denied_keys_filename) as file:
            denied_keys = json.load(file)
            assert denied_keys == []
        os.remove(temp_denied_keys_filename)


def test_denied_keys(mock_server):
    with open("tests/resources/circrequests/valid_dest_response_denied_key.json") as file:
        valid_dest_response_denied_key = file.read()

    try:
        # Create a temporary file to use as denied keys file
        [temp_denied_keys_file_handle, temp_denied_keys_filename] = tempfile.mkstemp()
        config = {
            'denied_keys_filepath': temp_denied_keys_filename
        }

        record_denied_keys = RecordDeniedKeys(config, valid_dest_response_denied_key)
        step_result = record_denied_keys.execute()
        assert step_result.was_successful() is True
    finally:
        # Clean up the temporary file
        os.close(temp_denied_keys_file_handle)

        # Verify that "denied keys" file contains a denied key
        with open(temp_denied_keys_filename) as file:
            denied_keys = json.load(file)
            assert denied_keys == ['31430023550355']

        os.remove(temp_denied_keys_filename)
