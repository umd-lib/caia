from caia.items.steps.parse_source_response import ParseSourceResponse


def test_parse_source_response_with_valid_response():
    source_response_file = 'tests/resources/items/valid_src_response.json'
    with open(source_response_file, 'r') as file:
        src_response_str = file.read()

    parse_source_response = ParseSourceResponse(src_response_str)
    step_result = parse_source_response.execute()
    assert step_result.was_successful() is True

    source_items = step_result.get_result()
    assert 2 == len(source_items.get_new_items())
    assert 2 == len(source_items.get_updated_items())
