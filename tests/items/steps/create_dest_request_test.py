from caia.items.steps.create_dest_request import CreateDestNewItemsRequest, CreateDestUpdatedItemsRequest
from caia.items.steps.create_dest_request import parse_item
from caia.items.steps.parse_source_response import ParseSourceResponse


def test_parse_item():
    source_item = {"barcode": "33433096993165", "title": "Jane Eyre"}
    parsed_item = parse_item(source_item)
    assert parsed_item["barcode"] == "33433096993165"
    assert parsed_item["title"] == "Jane Eyre"


def test_parse_item_only_includes_keys_in_mapping():
    source_item = {"barcode": "33433096993165", "title": "Jane Eyre", "foobar": "quuz"}
    parsed_item = parse_item(source_item)

    assert 2 == len(parsed_item.keys())
    assert parsed_item["barcode"] == "33433096993165"
    assert parsed_item["title"] == "Jane Eyre"
    assert "foobar" not in parsed_item


def test_create_dest_new_items_request():
    source_response_file = 'tests/resources/items/valid_src_response.json'
    with open(source_response_file, 'r') as file:
        src_response_str = file.read()

    parse_source_response = ParseSourceResponse(src_response_str)
    step_result = parse_source_response.execute()
    source_items = step_result.get_result()

    create_dest_new_items_request = CreateDestNewItemsRequest(source_items)
    step_result = create_dest_new_items_request.execute()
    request_body_str = step_result.get_result()
    assert '{"incoming": [{"barcode": "33433096993165", "title": "Jane Eyre"}]}' == request_body_str


def test_create_dest_updated_items_request():
    source_response_file = 'tests/resources/items/valid_src_response.json'
    with open(source_response_file, 'r') as file:
        src_response_str = file.read()

    parse_source_response = ParseSourceResponse(src_response_str)
    step_result = parse_source_response.execute()
    source_items = step_result.get_result()

    create_dest_updated_items_request = CreateDestUpdatedItemsRequest(source_items)
    step_result = create_dest_updated_items_request.execute()
    request_body_str = step_result.get_result()
    assert '{"items": [{"barcode": "31234000023075", "title": "Wuthering Heights"}]}' == request_body_str