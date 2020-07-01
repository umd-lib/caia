import datetime
import json
import os
import tempfile

from caia.circrequests.diff import DiffResult
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

        current_time = datetime.datetime.now()
        diff_result = DiffResult([], [], [], {})
        record_denied_keys = RecordDeniedKeys(config, valid_dest_response,
                                              current_time, diff_result)
        step_result = record_denied_keys.execute()
        assert step_result.was_successful() is True
    finally:
        # Clean up the temporary file
        os.close(temp_denied_keys_file_handle)

        # Verify that "denied keys" file contains empty dictionary
        with open(temp_denied_keys_filename) as file:
            denied_keys = json.load(file)
            assert denied_keys == {}
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

        current_time = datetime.datetime.now()
        diff_result = DiffResult([], [], [], {})
        record_denied_keys = RecordDeniedKeys(config, valid_dest_response_denied_key,
                                              current_time, diff_result)
        step_result = record_denied_keys.execute()
        assert step_result.was_successful() is True
    finally:
        # Clean up the temporary file
        os.close(temp_denied_keys_file_handle)

        # Verify that "denied keys" file contains a denied key
        with open(temp_denied_keys_filename) as file:
            denied_keys = json.load(file)
            assert denied_keys == {'31430023550355': current_time.isoformat()}

        os.remove(temp_denied_keys_filename)


def test_denied_keys_to_persist_no_new_denied_keys(mock_server):
    with open("tests/resources/circrequests/valid_dest_response.json") as file:
        valid_dest_response_denied_key = file.read()

    try:
        # Create a temporary file to use as denied keys file
        [temp_denied_keys_file_handle, temp_denied_keys_filename] = tempfile.mkstemp()
        config = {
            'denied_keys_filepath': temp_denied_keys_filename
        }

        current_time = datetime.datetime.now()
        june15 = '2020-06-15T11:36:33.032362'
        persisted_denied_keys = {'persisted_key1': june15}
        diff_result = DiffResult([], [], [], persisted_denied_keys)
        record_denied_keys = RecordDeniedKeys(config, valid_dest_response_denied_key,
                                              current_time, diff_result)
        step_result = record_denied_keys.execute()
        assert step_result.was_successful() is True
    finally:
        # Clean up the temporary file
        os.close(temp_denied_keys_file_handle)

        # Verify that "denied keys" file contains a denied key
        with open(temp_denied_keys_filename) as file:
            denied_keys = json.load(file)
            assert denied_keys == {'persisted_key1': june15}

        os.remove(temp_denied_keys_filename)


def test_denied_keys_to_persist_and_a_new_denied_keys(mock_server):
    with open("tests/resources/circrequests/valid_dest_response_denied_key.json") as file:
        valid_dest_response_denied_key = file.read()

    try:
        # Create a temporary file to use as denied keys file
        [temp_denied_keys_file_handle, temp_denied_keys_filename] = tempfile.mkstemp()
        config = {
            'denied_keys_filepath': temp_denied_keys_filename
        }

        current_time = datetime.datetime.now()
        june15 = '2020-06-15T11:36:33.032362'
        persisted_denied_keys = {'persisted_key1': june15}
        diff_result = DiffResult([], [], [], persisted_denied_keys)
        record_denied_keys = RecordDeniedKeys(config, valid_dest_response_denied_key,
                                              current_time, diff_result)
        step_result = record_denied_keys.execute()
        assert step_result.was_successful() is True
    finally:
        # Clean up the temporary file
        os.close(temp_denied_keys_file_handle)

        # Verify that "denied keys" file contains a denied key
        with open(temp_denied_keys_filename) as file:
            denied_keys = json.load(file)
            assert len(denied_keys) == 2
            assert 'persisted_key1' in denied_keys
            assert denied_keys['persisted_key1'] == june15
            assert '31430023550355' in denied_keys
            assert denied_keys['31430023550355'] == current_time.isoformat()

        os.remove(temp_denied_keys_filename)
