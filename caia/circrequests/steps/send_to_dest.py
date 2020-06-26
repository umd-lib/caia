import json
import logging
from typing import List

from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from caia.core.http import http_post_request
from caia.core.step import Step, StepResult

logger = logging.getLogger(__name__)


class SendToDest(Step):
    """
    Sends request to destination
    """
    def __init__(self, job_config: CircrequestsJobConfig):
        self.job_config = job_config
        self.errors: List[str] = []

    def execute(self) -> StepResult:
        dest_request_body_filepath = self.job_config['dest_request_body_filepath']

        with open(dest_request_body_filepath) as fp:
            body_str = fp.read()

        headers = {'X-API-Key': self.job_config['caiasoft_api_key'], 'Content-Type': 'application/json'}
        dest_url = self.job_config['dest_url']

        step_result = http_post_request(dest_url, headers, body_str)

        if step_result.was_successful():
            SendToDest.log_response(step_result.get_result())

        return step_result

    @staticmethod
    def log_response(response_body_text: str) -> None:
        response = json.loads(response_body_text)
        request_count = int(response["request_count"])
        results = response["results"]
        processed_count = 0
        denied_count = 0
        denied_entries = []

        for result in results:
            deny = result["deny"]
            if deny == "N":
                processed_count = processed_count + 1
            else:
                denied_count = denied_count + 1
                denied_entries.append(result["item"])

        logger.info(f"Total requests: {request_count}, Processed: {processed_count}, Denied: {denied_count}")
        if request_count == processed_count:
            logger.info("SUCCESS - All requests were processed")
        else:
            logger.warning(f"WARNING - {denied_count} request(s) were denied")
            logger.warning(f"denied_entries: {denied_entries}")

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
