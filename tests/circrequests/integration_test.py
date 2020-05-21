from hamcrest import assert_that
from mbtest.matchers import had_request
from mbtest.imposters import Imposter, Predicate, Response, Stub
from caia.commands.circrequests import Command
import tempfile
import os


def setup_environment(imposter, temp_storage_dir, temp_success_filename):
    os.environ["CIRCREQUESTS_SOURCE_URL"] = f"{imposter.url}/src"
    os.environ["CIRCREQUESTS_DEST_URL"] = f"{imposter.url}/dest"
    os.environ["CIRCREQUESTS_STORAGE_DIR"] = temp_storage_dir
    os.environ["CIRCREQUESTS_LAST_SUCCESS_LOOKUP"] = temp_success_filename
    os.environ["CAIASOFT_API_KEY"] = 'TEST_KEY'
    os.environ["CIRCREQUESTS_SOURCE_KEY_FIELD"] = 'item'


def test_successful_job(mock_server):
    with open("tests/resources/circrequests/valid_src_response.json") as file:
        valid_src_response = file.read()

    with open("tests/resources/circrequests/valid_dest_response.json") as file:
        valid_dest_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(body=valid_src_response)),
        Stub(Predicate(path="/dest", method="POST"), Response(body=valid_dest_response)),
        ])

    # Create a temporary file to use as last success lookup
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('storage/etc/circrequests_FIRST.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            setup_environment(imposter, temp_storage_dir, temp_success_filename)

            start_time = '20200521132905'
            args = []

            command = Command()
            result = command(start_time, args)
            assert result.was_successful() is True

            assert_that(server, had_request().with_path("/src").and_method("GET"))
            assert_that(server, had_request().with_path("/dest").and_method("POST"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)


def test_no_diff_job(mock_server):
    with open("tests/resources/circrequests/valid_src_response.json") as file:
        valid_src_response = file.read()

    with open("tests/resources/circrequests/valid_dest_response.json") as file:
        valid_dest_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(body=valid_src_response)),
        Stub(Predicate(path="/dest", method="POST"), Response(body=valid_dest_response)),
        ])

    # Create a temporary file to use as last success lookup
    # This will be comparing against the same response
    # (tests/resources/circrequests/valid_src_response.json)
    # so there will be no difference
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('tests/resources/circrequests/valid_src_response.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            setup_environment(imposter, temp_storage_dir, temp_success_filename)

            start_time = '20200521132905'
            args = []

            command = Command()
            result = command(start_time, args)
            assert result.was_successful() is True

            # There should be only one request to the server (the /src request)
            assert 1 == len(server.get_actual_requests())
            assert_that(server, had_request().with_path("/src").and_method("GET"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)


def test_src_returns_404_error(mock_server):
    with open("tests/resources/circrequests/valid_dest_response.json") as file:
        valid_dest_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(status_code=404)),
        Stub(Predicate(path="/dest", method="POST"), Response(body=valid_dest_response)),
        ])

    # Create a temporary file to use as last success lookup
    # This will be comparing against the same response
    # (tests/resources/circrequests/valid_src_response.json)
    # so there will be no difference
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('storage/etc/circrequests_FIRST.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            os.environ["CIRCREQUESTS_SOURCE_URL"] = f"{imposter.url}/src"
            os.environ["CIRCREQUESTS_DEST_URL"] = f"{imposter.url}/dest"
            os.environ["CIRCREQUESTS_STORAGE_DIR"] = temp_storage_dir
            os.environ["CIRCREQUESTS_LAST_SUCCESS_LOOKUP"] = temp_success_filename
            os.environ["CAIASOFT_API_KEY"] = 'TEST_KEY'
            os.environ["CIRCREQUESTS_SOURCE_KEY_FIELD"] = 'item'

            start_time = '20200521132905'
            args = []
            # job_config = CircrequestsJobConfig(config, 'test')

            command = Command()
            result = command(start_time, args)
            assert result.was_successful() is False
            assert 1 == len(result.get_errors())

            # There should be only one request to the server (the /src request)
            assert 1 == len(server.get_actual_requests())
            assert_that(server, had_request().with_path("/src").and_method("GET"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)


def test_dest_returns_404_error(mock_server):
    with open("tests/resources/circrequests/valid_src_response.json") as file:
        valid_src_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src"), Response(body=valid_src_response)),
        Stub(Predicate(path="/dest", method="POST"), Response(status_code=404)),
        ])

    # Create a temporary file to use as last success lookup
    # This will be comparing against the same response
    # (tests/resources/circrequests/valid_src_response.json)
    # so there will be no difference
    try:
        [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('storage/etc/circrequests_FIRST.json')

        with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
            os.environ["CIRCREQUESTS_SOURCE_URL"] = f"{imposter.url}/src"
            os.environ["CIRCREQUESTS_DEST_URL"] = f"{imposter.url}/dest"
            os.environ["CIRCREQUESTS_STORAGE_DIR"] = temp_storage_dir
            os.environ["CIRCREQUESTS_LAST_SUCCESS_LOOKUP"] = temp_success_filename
            os.environ["CAIASOFT_API_KEY"] = 'TEST_KEY'
            os.environ["CIRCREQUESTS_SOURCE_KEY_FIELD"] = 'item'

            start_time = '20200521132905'
            args = []
            # job_config = CircrequestsJobConfig(config, 'test')

            command = Command()
            result = command(start_time, args)
            assert result.was_successful() is False
            assert 1 == len(result.get_errors())

            assert_that(server, had_request().with_path("/src").and_method("GET"))
            assert_that(server, had_request().with_path("/dest").and_method("POST"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)
