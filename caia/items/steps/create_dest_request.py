import json
import logging
from typing import Dict, List

from caia.core.step import Step, StepResult
from caia.items.source_items import SourceItems

logger = logging.getLogger(__name__)

# CaiaSoft value for indicating that field contents should be cleared
CAIASOFT_CLEAR_FIELD_SENTINEL_VALUE = "CLEARFIELD*"


def parse_item(item_from_source: Dict[str, str], convert_null_values: bool) -> Dict[str, str]:
    """
    Converts source map into a destination map, sending all fields in the source
    to the destination.

    If "convert_null_values" is True, any keys with null values will be replaced
    by CAIASOFT_CLEAR_FIELD_SENTINEL_VALUE in the destination request.
    """
    item_map = {}
    for source_key in item_from_source:
        source_value = item_from_source[source_key]
        if convert_null_values and source_value is None:
            source_value = CAIASOFT_CLEAR_FIELD_SENTINEL_VALUE

        item_map[source_key] = source_value

    return item_map


class CreateDestNewItemsRequest(Step):
    """
    Constructs the POST request body to send to the destination
    """
    def __init__(self, source_items: SourceItems):
        self.source_items = source_items
        self.errors: List[str] = []

    def execute(self) -> StepResult:
        items_array = []

        new_items = self.source_items.get_new_items()
        for item in new_items:
            # Null values should be preserved for new items
            items_array.append(parse_item(item, False))

        request_body = {"incoming": items_array}
        json_str = json.dumps(request_body)

        step_result = StepResult(True, json_str)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"


class CreateDestUpdatedItemsRequest(Step):
    """
    Constructs the POST request body to send to the destination
    """
    def __init__(self, source_items: SourceItems):
        self.source_items = source_items
        self.errors: List[str] = []

    def execute(self) -> StepResult:
        items_array = []

        new_items = self.source_items.get_updated_items()
        for item in new_items:
            # Null values should be converted for updated items
            items_array.append(parse_item(item, True))

        request_body = {"items": items_array}
        json_str = json.dumps(request_body)

        step_result = StepResult(True, json_str)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
