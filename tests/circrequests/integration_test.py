import datetime
import json
import os
import tempfile

from hamcrest import assert_that, is_not
from mbtest.imposters import Imposter, Predicate, Response, Stub
from mbtest.matchers import had_request

from caia.commands.circrequests import Command


def setup_environment(imposter, temp_storage_dir, temp_success_filename,
                      temp_denied_keys_filename="storage/circrequests/circrequests_denied_keys.json"):
    os.environ["CIRCREQUESTS_SOURCE_URL"] = f"{imposter.url}/src"
    os.environ["CIRCREQUESTS_DEST_URL"] = f"{imposter.url}/dest"
    os.environ["CIRCREQUESTS_STORAGE_DIR"] = temp_storage_dir
    os.environ["CIRCREQUESTS_LAST_SUCCESS_LOOKUP"] = temp_success_filename
    os.environ["CIRCREQUESTS_DENIED_KEYS"] = temp_denied_keys_filename
    os.environ["CAIASOFT_API_KEY"] = 'TEST_KEY'


# def test_successful_job(mock_server):
#     with open("tests/resources/circrequests/valid_src_response.json") as file:
#         valid_src_response = file.read()
#
#     with open("tests/resources/circrequests/valid_dest_response.json") as file:
#         valid_dest_response = file.read()
#
#     # Set up mock server with required behavior
#     imposter = Imposter([
#         Stub(Predicate(path="/src"), Response(body=valid_src_response)),
#         Stub(Predicate(path="/dest", method="POST"), Response(body=valid_dest_response)),
#         ])
#
#     try:
#         # Create a temporary file to use as last success lookup
#         [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
#         with open(temp_success_filename, 'w') as f:
#             f.write('etc/circrequests_FIRST.json')
#
#         with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
#             setup_environment(imposter, temp_storage_dir, temp_success_filename)
#
#             start_time = '20200521132905'
#             args = []
#
#             command = Command()
#             result = command(start_time, args)
#             assert result.was_successful() is True
#
#             assert_that(server, had_request().with_path("/src").and_method("GET"))
#             assert_that(server, had_request().with_path("/dest").and_method("POST"))
#     finally:
#         # Clean up the temporary file
#         os.close(temp_file_handle)
#         os.remove(temp_success_filename)
#
#
# def test_no_diff_job(mock_server):
#     with open("tests/resources/circrequests/valid_src_response.json") as file:
#         valid_src_response = file.read()
#
#     with open("tests/resources/circrequests/valid_dest_response.json") as file:
#         valid_dest_response = file.read()
#
#     # Set up mock server with required behavior
#     imposter = Imposter([
#         Stub(Predicate(path="/src"), Response(body=valid_src_response)),
#         Stub(Predicate(path="/dest", method="POST"), Response(body=valid_dest_response)),
#         ])
#
#     # Create a temporary file to use as last success lookup
#     # This will be comparing against the same response
#     # (tests/resources/circrequests/valid_src_response.json)
#     # so there will be no difference
#     try:
#         [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
#         with open(temp_success_filename, 'w') as f:
#             f.write('tests/resources/circrequests/valid_src_response.json')
#
#         with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
#             setup_environment(imposter, temp_storage_dir, temp_success_filename)
#
#             start_time = '20200521132905'
#             args = []
#
#             command = Command()
#             result = command(start_time, args)
#             assert result.was_successful() is True
#
#             # There should be only one request to the server (the /src request)
#             assert 1 == len(server.get_actual_requests()[imposter.port])
#             assert_that(server, had_request().with_path("/src").and_method("GET"))
#     finally:
#         # Clean up the temporary file
#         os.close(temp_file_handle)
#         os.remove(temp_success_filename)
#
#
# def test_src_returns_404_error(mock_server):
#     with open("tests/resources/circrequests/valid_dest_response.json") as file:
#         valid_dest_response = file.read()
#
#     # Set up mock server with required behavior
#     imposter = Imposter([
#         Stub(Predicate(path="/src"), Response(status_code=404)),
#         Stub(Predicate(path="/dest", method="POST"), Response(body=valid_dest_response)),
#         ])
#
#     # Create a temporary file to use as last success lookup
#     # This will be comparing against the same response
#     # (tests/resources/circrequests/valid_src_response.json)
#     # so there will be no difference
#     try:
#         [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
#         with open(temp_success_filename, 'w') as f:
#             f.write('etc/circrequests_FIRST.json')
#
#         with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
#             setup_environment(imposter, temp_storage_dir, temp_success_filename)
#
#             start_time = '20200521132905'
#             args = []
#             # job_config = CircrequestsJobConfig(config, 'test')
#
#             command = Command()
#             result = command(start_time, args)
#             assert result.was_successful() is False
#             assert 1 == len(result.get_errors())
#
#             # There should be only one request to the server (the /src request)
#             assert 1 == len(server.get_actual_requests()[imposter.port])
#             assert_that(server, had_request().with_path("/src").and_method("GET"))
#     finally:
#         # Clean up the temporary file
#         os.close(temp_file_handle)
#         os.remove(temp_success_filename)
#
#
# def test_dest_returns_404_error(mock_server):
#     with open("tests/resources/circrequests/valid_src_response.json") as file:
#         valid_src_response = file.read()
#
#     # Set up mock server with required behavior
#     imposter = Imposter([
#         Stub(Predicate(path="/src"), Response(body=valid_src_response)),
#         Stub(Predicate(path="/dest", method="POST"), Response(status_code=404)),
#         ])
#
#     # Create a temporary file to use as last success lookup
#     # This will be comparing against the same response
#     # (tests/resources/circrequests/valid_src_response.json)
#     # so there will be no difference
#     try:
#         [temp_file_handle, temp_success_filename] = tempfile.mkstemp()
#         with open(temp_success_filename, 'w') as f:
#             f.write('etc/circrequests_FIRST.json')
#
#         with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
#             setup_environment(imposter, temp_storage_dir, temp_success_filename)
#
#             start_time = '20200521132905'
#             args = []
#
#             command = Command()
#             result = command(start_time, args)
#             assert result.was_successful() is False
#             assert 1 == len(result.get_errors())
#
#             assert_that(server, had_request().with_path("/src").and_method("GET"))
#             assert_that(server, had_request().with_path("/dest").and_method("POST"))
#     finally:
#         # Clean up the temporary file
#         os.close(temp_file_handle)
#         os.remove(temp_success_filename)
#
#
# def test_dest_returns_denied_key(mock_server):
#     with open("tests/resources/circrequests/valid_src_response.json") as file:
#         valid_src_response = file.read()
#
#     with open("tests/resources/circrequests/valid_dest_response_denied_key.json") as file:
#         valid_dest_response_denied_key = file.read()
#
#     # Set up mock server with required behavior
#     imposter = Imposter([
#         Stub(Predicate(path="/src"), Response(body=valid_src_response)),
#         Stub(Predicate(path="/dest", method="POST"), Response(body=valid_dest_response_denied_key)),
#         ])
#
#     try:
#         # Create a temporary file to use as last success lookup
#         [temp_success_file_handle, temp_success_filename] = tempfile.mkstemp()
#         with open(temp_success_filename, 'w') as f:
#             f.write('etc/circrequests_FIRST.json')
#
#         # Create a temporary file to use as denied keys file
#         [temp_denied_keys_file_handle, temp_denied_keys_filename] = tempfile.mkstemp()
#         with open(temp_denied_keys_filename, 'w') as f:
#             f.write('{}')
#
#         with tempfile.TemporaryDirectory() as temp_storage_dir, mock_server(imposter) as server:
#             setup_environment(imposter, temp_storage_dir, temp_success_filename, temp_denied_keys_filename)
#
#             start_time = '20200521132905'
#             args = []
#
#             command = Command()
#             result = command(start_time, args)
#             assert result.was_successful() is True
#
#             assert_that(server, had_request().with_path("/src").and_method("GET"))
#             assert_that(server, had_request().with_path("/dest").and_method("POST"))
#     finally:
#         # Clean up the temporary files
#         os.close(temp_success_file_handle)
#         os.remove(temp_success_filename)
#
#         os.close(temp_denied_keys_file_handle)
#         # Verify that "denied keys" file contains denied entry
#         with open(temp_denied_keys_filename) as file:
#             denied_keys = json.load(file)
#             denied_item_time = datetime.datetime.strptime(start_time, '%Y%m%d%H%M%S').isoformat()
#             assert denied_keys == {'31430023550355': denied_item_time}
#         os.remove(temp_denied_keys_filename)
#
#
# def test_denied_key_wait_interval(mock_server):
#     with open("tests/resources/circrequests/valid_src_response.json") as file:
#         valid_src_response = file.read()
#
#     with open("tests/resources/circrequests/valid_dest_response_denied_key.json") as file:
#         valid_dest_response_denied_key = file.read()
#
#     # Set up mock server with required behavior
#     imposter = Imposter([
#         Stub(Predicate(path="/src"), Response(body=valid_src_response)),
#         Stub(Predicate(path="/dest", method="POST"), Response(body=valid_dest_response_denied_key)),
#         ])
#
#     try:
#         # Create a temporary file to use as last success lookup
#         [temp_success_file_handle, temp_success_filename] = tempfile.mkstemp()
#         with open(temp_success_filename, 'w') as f:
#             f.write('etc/circrequests_FIRST.json')
#
#         # Create a temporary file to use as denied keys file
#         [temp_denied_keys_file_handle, temp_denied_keys_filename] = tempfile.mkstemp()
#         with open(temp_denied_keys_filename, 'w') as f:
#             f.write('{}')
#
#         with tempfile.TemporaryDirectory() as temp_storage_dir:
#             with mock_server(imposter) as server:
#                 # First request generates a deny
#                 setup_environment(imposter, temp_storage_dir, temp_success_filename, temp_denied_keys_filename)
#                 os.environ['CIRCREQUESTS_DENIED_ITEMS_WAIT_INTERVAL'] = '2700'  # 45 minutes
#
#                 start_time = '20200701000000'  # 12:00am, July 1
#                 args = []
#
#                 command = Command()
#                 result = command(start_time, args)
#                 assert result.was_successful() is True
#
#                 assert_that(server, had_request().with_path("/src").and_method("GET"))
#                 assert_that(server, had_request().with_path("/dest").and_method("POST"))
#
#                 # Verify that "denied keys" file contains denied entry
#                 with open(temp_denied_keys_filename) as file:
#                     denied_keys = json.load(file)
#                     denied_item_time = datetime.datetime.strptime(start_time, '%Y%m%d%H%M%S').isoformat()
#                     assert denied_keys == {'31430023550355': denied_item_time}
#
#             with mock_server(imposter) as server:
#                 # Second request does not send any items, as only item is in
#                 # denied list and wait time has not expired
#                 start_time = '20200701003000'  # 12:30am, July 1
#                 args = []
#                 command = Command()
#                 result = command(start_time, args)
#                 assert result.was_successful() is True
#                 assert_that(server, had_request().with_path("/src").and_method("GET"))
#                 assert_that(server, is_not(had_request().with_path("/dest").and_method("POST")))
#
#             with mock_server(imposter) as server:
#                 # Third request occurs after wait interval expires, so
#                 # denied items should be sent again
#                 start_time = '20200701010000'  # 1:00am, July 1
#                 args = []
#                 command = Command()
#                 result = command(start_time, args)
#                 assert result.was_successful() is True
#                 assert_that(server, had_request().with_path("/src").and_method("GET"))
#                 assert_that(server, had_request().with_path("/dest").and_method("POST"))
#
#     finally:
#         # Clean up the temporary files
#         os.close(temp_success_file_handle)
#         os.remove(temp_success_filename)
#
#         os.close(temp_denied_keys_file_handle)
#         os.remove(temp_denied_keys_filename)


def test_denied_key_wait_interval(mock_server):
    with open("tests/resources/circrequests/valid_src_modified_response.1.json") as file:
        modified_response1 = file.read()

    with open("tests/resources/circrequests/valid_src_modified_response.2.json") as file:
        modified_response2 = file.read()

    with open("tests/resources/circrequests/valid_dest_response.json") as file:
        valid_dest_response = file.read()

    # Set up mock server with required behavior
    source_responses = [
        Response(body=modified_response1),
        Response(body=modified_response2)
    ]
    imposter = Imposter([
        Stub(Predicate(path="/src"), source_responses),
        Stub(Predicate(path="/dest", method="POST"), Response(body=valid_dest_response)),
    ])

    try:
        # Create a temporary file to use as last success lookup
        [temp_success_file_handle, temp_success_filename] = tempfile.mkstemp()
        with open(temp_success_filename, 'w') as f:
            f.write('etc/circrequests_FIRST.json')

        # Create a temporary file to use as denied keys file
        [temp_denied_keys_file_handle, temp_denied_keys_filename] = tempfile.mkstemp()
        with open(temp_denied_keys_filename, 'w') as f:
            f.write('{}')

        with tempfile.TemporaryDirectory() as temp_storage_dir:
            with mock_server(imposter) as server:
                # First request is a success
                setup_environment(imposter, temp_storage_dir, temp_success_filename, temp_denied_keys_filename)

                start_time = '20200701000000'  # 12:00am, July 1
                args = []

                command = Command()
                result = command(start_time, args)
                assert result.was_successful() is True

                # Verify that CaiaSoft submission was made
                assert_that(server, had_request().with_path("/src").and_method("GET"))
                assert_that(server, had_request().with_path("/dest").and_method("POST"))

                # Second request should make another request, with the modified item
                start_time = '20200701003000'  # 12:30am, July 1
                args = []
                command = Command()
                result = command(start_time, args)
                assert result.was_successful() is True
                assert_that(server, had_request().with_path("/src").and_method("GET"))
                assert_that(server, had_request().with_path("/dest").and_method("POST"))
    finally:
        # Clean up the temporary files
        os.close(temp_success_file_handle)
        os.remove(temp_success_filename)

        os.close(temp_denied_keys_file_handle)
        os.remove(temp_denied_keys_filename)
