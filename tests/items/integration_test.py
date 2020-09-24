import os
import pytest
import re
import tempfile

from json import JSONDecodeError
from hamcrest import assert_that
from mbtest.imposters import Imposter, Predicate, Response, Stub
from mbtest.matchers import had_request
from os import listdir
from os.path import isfile, join

from caia.commands.items import Command


def setup_environment(imposter, temp_storage_dir, temp_success_filename):
    os.environ["ITEMS_SOURCE_URL"] = f"{imposter.url}/src"
    os.environ["ITEMS_DEST_NEW_URL"] = f"{imposter.url}/dest/new"
    os.environ["ITEMS_DEST_UPDATES_URL"] = f"{imposter.url}/dest/updated"
    os.environ["ITEMS_STORAGE_DIR"] = temp_storage_dir
    os.environ["ITEMS_LAST_SUCCESS_LOOKUP"] = temp_success_filename
    os.environ["CAIASOFT_API_KEY"] = 'TEST_KEY'


def test_successful_job(mock_server):
    with open("tests/resources/items/valid_src_response.json") as file:
        valid_src_response = file.read()

    with open("tests/resources/items/valid_dest_new_items_response.json") as file:
        valid_dest_new_items_response = file.read()

    with open("tests/resources/items/valid_dest_updated_items_response.json") as file:
        valid_dest_updated_items_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(body=valid_src_response)),
        Stub(Predicate(path="/dest/new", method="POST"), Response(body=valid_dest_new_items_response)),
        Stub(Predicate(path="/dest/updated", method="POST"), Response(body=valid_dest_updated_items_response)),
        ])

    # Create a temporary file to use as last success lookup
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('etc/items_FIRST.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            setup_environment(imposter, temp_storage_dir, temp_success_filename)

            start_time = '20200521132905'
            args = []

            command = Command()
            result = command(start_time, args)
            assert result.was_successful() is True

            assert_that(server, had_request().with_path("/src").and_method("GET"))
            assert_that(server, had_request().with_path("/dest/new").and_method("POST"))
            assert_that(server, had_request().with_path("/dest/updated").and_method("POST"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)


def test_successful_job_no_new_items(mock_server):
    with open("tests/resources/items/valid_src_no_new_items_response.json") as file:
        valid_src_response = file.read()

    with open("tests/resources/items/valid_dest_updated_items_response.json") as file:
        valid_dest_updated_items_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(body=valid_src_response)),
        Stub(Predicate(path="/dest/new", method="POST"), Response(body="{}")),
        Stub(Predicate(path="/dest/updated", method="POST"), Response(body=valid_dest_updated_items_response)),
        ])

    # Create a temporary file to use as last success lookup
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('etc/items_FIRST.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            setup_environment(imposter, temp_storage_dir, temp_success_filename)

            start_time = '20200521132905'
            args = []

            command = Command()
            result = command(start_time, args)
            assert result.was_successful() is True

            assert 2 == len(server.get_actual_requests()[imposter.port])
            assert_that(server, had_request().with_path("/src").and_method("GET"))
            assert_that(server, had_request().with_path("/dest/updated").and_method("POST"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)


def test_successful_job_no_updated_items(mock_server):
    with open("tests/resources/items/valid_src_no_updated_items_response.json") as file:
        valid_src_response = file.read()

    with open("tests/resources/items/valid_dest_new_items_response.json") as file:
        valid_dest_new_items_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(body=valid_src_response)),
        Stub(Predicate(path="/dest/new", method="POST"), Response(body=valid_dest_new_items_response)),
        Stub(Predicate(path="/dest/updated", method="POST"), Response(body="{}")),
        ])

    # Create a temporary file to use as last success lookup
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('etc/items_FIRST.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            setup_environment(imposter, temp_storage_dir, temp_success_filename)

            start_time = '20200521132905'
            args = []

            command = Command()
            result = command(start_time, args)
            assert result.was_successful() is True

            assert 2 == len(server.get_actual_requests()[imposter.port])
            assert_that(server, had_request().with_path("/src").and_method("GET"))
            assert_that(server, had_request().with_path("/dest/new").and_method("POST"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)


def test_successful_job_no_new_or_updated_items(mock_server):
    with open("tests/resources/items/valid_src_no_new_or_updated_items_response.json") as file:
        valid_src_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(body=valid_src_response)),
        Stub(Predicate(path="/dest/new", method="POST"), Response(body="{}")),
        Stub(Predicate(path="/dest/updated", method="POST"), Response(body="{}")),
        ])

    # Create a temporary file to use as last success lookup
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('etc/items_FIRST.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            setup_environment(imposter, temp_storage_dir, temp_success_filename)

            start_time = '20200521132905'
            args = []

            command = Command()
            result = command(start_time, args)
            assert result.was_successful() is True

            assert 1 == len(server.get_actual_requests()[imposter.port])
            assert_that(server, had_request().with_path("/src").and_method("GET"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)


def test_src_returns_404_error(mock_server):
    with open("tests/resources/items/valid_dest_new_items_response.json") as file:
        valid_dest_new_items_response = file.read()

    with open("tests/resources/items/valid_dest_updated_items_response.json") as file:
        valid_dest_updated_items_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(status_code=404)),
        Stub(Predicate(path="/dest/new", method="POST"), Response(body=valid_dest_new_items_response)),
        Stub(Predicate(path="/dest/updated", method="POST"), Response(body=valid_dest_updated_items_response)),
        ])

    # Create a temporary file to use as last success lookup
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('etc/items_FIRST.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            setup_environment(imposter, temp_storage_dir, temp_success_filename)

            start_time = '20200521132905'
            args = []

            command = Command()
            result = command(start_time, args)
            assert result.was_successful() is False
            assert 1 == len(result.get_errors())

            # There should be only one request to the server (the /src request)
            assert 1 == len(server.get_actual_requests()[imposter.port])
            assert_that(server, had_request().with_path("/src").and_method("GET"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)


def test_dest_returns_404_error(mock_server):
    with open("tests/resources/items/valid_src_response.json") as file:
        valid_src_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(body=valid_src_response)),
        Stub(Predicate(path="/dest/new", method="POST"), Response(status_code=404)),
        ])

    # Create a temporary file to use as last success lookup
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('etc/items_FIRST.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            setup_environment(imposter, temp_storage_dir, temp_success_filename)

            start_time = '20200521132905'
            args = []

            command = Command()
            result = command(start_time, args)
            assert result.was_successful() is False
            assert 1 == len(result.get_errors())

            # There should be only two requests to the server
            assert 2 == len(server.get_actual_requests()[imposter.port])
            assert_that(server, had_request().with_path("/src").and_method("GET"))
            assert_that(server, had_request().with_path("/dest/new").and_method("POST"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)


def test_dest_returns_unparseable_json_response_for_new_items(mock_server):
    with open("tests/resources/items/valid_src_response.json") as file:
        valid_src_response = file.read()

    with open("tests/resources/items/unparseable_json_dest_response.json") as file:
        unparseable_json_dest_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(body=valid_src_response)),
        Stub(Predicate(path="/dest/new", method="POST"), Response(body=unparseable_json_dest_response)),
        ])

    # Create a temporary file to use as last success lookup
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('etc/items_FIRST.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            setup_environment(imposter, temp_storage_dir, temp_success_filename)

            start_time = '20200521132905'
            args = []

            with pytest.raises(JSONDecodeError):
                command = Command()
                result = command(start_time, args)
                assert result.was_successful() is False

            files_in_storage_dir = [f for f in listdir(temp_storage_dir) if isfile(join(temp_storage_dir, f))]
            expected_file_regex = re.compile('.*\\.dest_new_items_response_body\\..*')

            # There should be a "dest_updated_response_body" file, even
            # though the JSON was unparseable
            if not any(expected_file_regex.match(x) for x in files_in_storage_dir):
                pytest.fail(f"Expected file matching '#{expected_file_regex.pattern}' was not found.")

            # There should have been two requests to the server, as the updated
            # items call will not occur
            assert 2 == len(server.get_actual_requests()[imposter.port])
            assert_that(server, had_request().with_path("/src").and_method("GET"))
            assert_that(server, had_request().with_path("/dest/new").and_method("POST"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)


def test_dest_returns_unparseable_json_response_for_updated_items(mock_server):
    with open("tests/resources/items/valid_src_response.json") as file:
        valid_src_response = file.read()

    with open("tests/resources/items/valid_dest_new_items_response.json") as file:
        valid_dest_new_items_response = file.read()

    with open("tests/resources/items/unparseable_json_dest_response.json") as file:
        unparseable_json_dest_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(body=valid_src_response)),
        Stub(Predicate(path="/dest/new", method="POST"), Response(body=valid_dest_new_items_response)),
        Stub(Predicate(path="/dest/updated", method="POST"), Response(body=unparseable_json_dest_response)),
        ])

    # Create a temporary file to use as last success lookup
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('etc/items_FIRST.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            setup_environment(imposter, temp_storage_dir, temp_success_filename)

            start_time = '20200521132905'
            args = []

            with pytest.raises(JSONDecodeError):
                command = Command()
                result = command(start_time, args)
                assert result.was_successful() is False

            files_in_storage_dir = [f for f in listdir(temp_storage_dir) if isfile(join(temp_storage_dir, f))]
            expected_file_regex = re.compile('.*\\.dest_updated_items_response_body\\..*')

            # There should be a "dest_updated_response_body" file, even
            # though the JSON was unparseable
            if not any(expected_file_regex.match(x) for x in files_in_storage_dir):
                pytest.fail(f"Expected file matching '#{expected_file_regex.pattern}' was not found.")

            # There should have been three requests to the server
            assert 3 == len(server.get_actual_requests()[imposter.port])
            assert_that(server, had_request().with_path("/src").and_method("GET"))
            assert_that(server, had_request().with_path("/dest/new").and_method("POST"))
            assert_that(server, had_request().with_path("/dest/updated").and_method("POST"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)
