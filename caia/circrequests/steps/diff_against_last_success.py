from caia.core.step import Step, StepResult
from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from typing import Any, Dict, List
from caia.circrequests.diff import diff
import json
import logging

logger = logging.getLogger(__name__)


class DiffAgainstLastSuccess(Step):
    """
    Diffs the source response against the last successful response, creating
    a list of new/modified/deleted entries
    """
    def __init__(self, job_config: CircrequestsJobConfig):
        self.job_config = job_config
        self.errors: List[str] = []

    @staticmethod
    def parse_source_response(response: Dict[Any, Any]) -> List[Dict[str, str]]:
        """
        Parses a source response for diffing
        """
        if 'holds' in response:
            return response['holds']
        return []

    def execute(self) -> StepResult:
        last_success_filepath = self.job_config['last_success_filepath']
        logger.info(f"Diffing against: {last_success_filepath}")

        # Retrieve source response from last success
        with open(last_success_filepath) as fp:
            last_success_response = json.load(fp)
            last_success = self.parse_source_response(last_success_response)

        # Retrieve source response from current load
        source_response_body_filepath = self.job_config['source_response_body_filepath']
        with open(source_response_body_filepath) as fp:
            source_response = json.load(fp)
            current = self.parse_source_response(source_response)

        key_field = self.job_config['application_config']['circrequests']['source_key_field']

        # Generate the diff result
        diff_result = diff(key_field, last_success, current)

        step_result = StepResult(True, diff_result)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
