import os
import tempfile

from hamcrest import assert_that, has_entries
from mbtest.imposters import Imposter, Predicate, Response, Stub
from mbtest.matchers import had_request

from caia.commands.items import Command


def setup_environment(imposter, temp_storage_dir, temp_success_filename):
    os.environ["ITEMS_SOURCE_URL"] = f"{imposter.url}/src"
    os.environ["ITEMS_DEST_NEW_URL"] = f"{imposter.url}/dest/new"
    os.environ["ITEMS_DEST_UPDATES_URL"] = f"{imposter.url}/dest/updated"
    os.environ["ITEMS_STORAGE_DIR"] = temp_storage_dir
    os.environ["ITEMS_LAST_SUCCESS_LOOKUP"] = temp_success_filename
    os.environ["CAIASOFT_API_KEY"] = 'TEST_KEY'


def test_successful_job(mock_server):
    with open("tests/resources/items/valid_src_iteration_0_response.json") as file:
        valid_src_iteration_0_response = file.read()

    with open("tests/resources/items/valid_src_iteration_1_response.json") as file:
        valid_src_iteration_1_response = file.read()

    with open("tests/resources/items/valid_dest_new_items_response.json") as file:
        valid_dest_new_items_response = file.read()

    with open("tests/resources/items/valid_dest_updated_items_response.json") as file:
        valid_dest_updated_items_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter([
        Stub(Predicate(path="/src", query={"nextitem": 3}), Response(body=valid_src_iteration_1_response)),
        Stub(Predicate(path="/src",), Response(body=valid_src_iteration_0_response)),
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

            assert_that(server, had_request().with_path("/src").with_method("GET").with_query(
                has_entries({'nextitem': '3'})).with_times(1))
            assert_that(server, had_request().with_path("/src").and_method("GET").with_times(2))
            assert_that(server, had_request().with_path("/dest/new").and_method("POST"))
            assert_that(server, had_request().with_path("/dest/updated").and_method("POST"))
    finally:
        # Clean up the temporary file
        os.close(temp_file_handle)
        os.remove(temp_success_filename)


