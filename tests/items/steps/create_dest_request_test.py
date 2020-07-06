import json
from caia.items.steps.create_dest_request import CreateDestNewItemsRequest, CreateDestUpdatedItemsRequest
from caia.items.steps.create_dest_request import parse_item, CAIASOFT_CLEAR_FIELD_SENTINEL_VALUE
from caia.items.steps.parse_source_response import ParseSourceResponse


def test_parse_item():
    source_item = {"barcode": "33433096993165", "title": "Jane Eyre"}
    parsed_item = parse_item(source_item, False)
    assert parsed_item["barcode"] == "33433096993165"
    assert parsed_item["title"] == "Jane Eyre"


def test_parse_item_send_all_keys_in_source_to_destination():
    source_item = {"barcode": "33433096993165", "title": "Jane Eyre", "foobar": "quuz"}
    parsed_item = parse_item(source_item, False)

    assert 3 == len(parsed_item.keys())
    assert parsed_item["barcode"] == "33433096993165"
    assert parsed_item["title"] == "Jane Eyre"
    assert parsed_item["foobar"] == "quuz"


def test_create_dest_new_items_request():
    source_response_file = 'tests/resources/items/valid_simple_src_response.json'
    with open(source_response_file, 'r') as file:
        src_response_str = file.read()

    parse_source_response = ParseSourceResponse(src_response_str)
    step_result = parse_source_response.execute()
    source_items = step_result.get_result()

    create_dest_new_items_request = CreateDestNewItemsRequest(source_items)
    step_result = create_dest_new_items_request.execute()
    request_body_str = step_result.get_result()

    assert '{"incoming": [{"barcode": "33433096993165", "collection": "DEMO", "title": "Jane Eyre"}]}' ==\
           request_body_str


def test_create_dest_updated_items_request():
    source_response_file = 'tests/resources/items/valid_simple_src_response.json'
    with open(source_response_file, 'r') as file:
        src_response_str = file.read()

    parse_source_response = ParseSourceResponse(src_response_str)
    step_result = parse_source_response.execute()
    source_items = step_result.get_result()

    create_dest_updated_items_request = CreateDestUpdatedItemsRequest(source_items)
    step_result = create_dest_updated_items_request.execute()
    request_body_str = step_result.get_result()

    assert '{"items": [{"barcode": "31234000023075", "call_number": "R34.5", "physical_desc": "317 pages", "title": "Wuthering Heights"}]}' == request_body_str  # noqa


def test_null_fields_preserved():
    source_item_json = '{"barcode": "31234000023075", "call_number": null, "title": "Item with Null Fields", ' \
                       '"physical_desc": null}'
    source_item = json.loads(source_item_json)
    parsed_item = parse_item(source_item, False)
    assert parsed_item["barcode"] == "31234000023075"
    assert parsed_item["call_number"] is None
    assert parsed_item["title"] == "Item with Null Fields"
    assert parsed_item["physical_desc"] is None


def test_null_fields_convert_to_sentinel_value():
    source_item_json = '{"barcode": "31234000023075", "call_number": null, "title": "Item with Null Fields", ' \
                       '"physical_desc": null}'
    source_item = json.loads(source_item_json)
    parsed_item = parse_item(source_item, True)
    assert parsed_item["barcode"] == "31234000023075"
    assert parsed_item["call_number"] == CAIASOFT_CLEAR_FIELD_SENTINEL_VALUE
    assert parsed_item["title"] == "Item with Null Fields"
    assert parsed_item["physical_desc"] == CAIASOFT_CLEAR_FIELD_SENTINEL_VALUE
