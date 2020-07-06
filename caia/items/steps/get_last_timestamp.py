import json
import logging
from typing import Any, Dict, List

from caia.core.step import Step, StepResult
from caia.items.items_job_config import ItemsJobConfig

logger = logging.getLogger(__name__)


class GetLastTimestamp(Step):
    """
    Retrieves the query timestamp from the last successful response
    """
    def __init__(self, job_config: ItemsJobConfig):
        self.job_config = job_config
        self.errors: List[str] = []

    @staticmethod
    def parse_source_response(response: Dict[Any, Any]) -> str:
        """
        Parses a source response for the last timestamp
        """
        last_timestamp_field = "endtime"
        try:
            last_timestamp = response[last_timestamp_field] or ""
        except KeyError:
            logger.error(f"Could not find {last_timestamp_field} field")
            last_timestamp = ""

        return last_timestamp

    def execute(self) -> StepResult:
        last_success_filepath = self.job_config['last_success_filepath']
        logger.info(f"Retrieving timestamp from: {last_success_filepath}")

        # Retrieve source response from last success
        with open(last_success_filepath) as fp:
            last_success_response = json.load(fp)
            last_timestamp = self.parse_source_response(last_success_response)

        if not last_timestamp:
            error = f"Could not find timestamp in {last_success_filepath}"
            errors = [error]
            return StepResult(False, None, errors)

        logger.info(f"Last timestamp: {last_timestamp}")

        step_result = StepResult(True, last_timestamp)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
