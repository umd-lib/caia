import json
import logging

from caia.core.step import Step, StepResult
from caia.items.source_items import SourceItems

logger = logging.getLogger(__name__)


class ParseSourceResponse(Step):
    """
    Converts the source response into a SourceItems object
    """
    def __init__(self, source_response: str):
        self.source_response = source_response

    def execute(self) -> StepResult:
        obj = json.loads(self.source_response)
        new_items = obj['new']
        updated_items = obj['update']

        source_items = SourceItems(new_items, updated_items)

        step_result = StepResult(True, source_items)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
