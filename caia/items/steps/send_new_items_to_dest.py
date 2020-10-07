import json
import logging
from typing import List

from caia.core.io import write_to_file
from caia.core.http import http_post_request
from caia.core.step import Step, StepResult
from caia.items.items_job_config import ItemsJobConfig

logger = logging.getLogger(__name__)


class SendNewItemsToDest(Step):
    """
    Sends request to destination
    """
    def __init__(self, job_config: ItemsJobConfig):
        self.job_config = job_config
        self.errors: List[str] = []

    def execute(self) -> StepResult:
        dest_request_body_filepath = self.job_config["dest_new_items_request_body_filepath"]

        with open(dest_request_body_filepath) as fp:
            body_str = fp.read()

        headers = {'X-API-Key': self.job_config['caiasoft_api_key'], 'Content-Type': 'application/json'}
        dest_url = self.job_config["dest_new_url"]

        step_result = http_post_request(dest_url, headers, body_str)

        # Write new items dest response body to a file
        write_to_file(self.job_config['dest_new_items_response_body_filepath'], step_result.get_result())

        if step_result.was_successful():
            SendNewItemsToDest.log_response(step_result.get_result())

        return step_result

    @staticmethod
    def log_response(response_body_text: str) -> None:
        response = json.loads(response_body_text)
        incoming_count = int(response["incoming_count"])
        rejected_count = int(response["rejected_count"])
        rejects = response["rejects"]

        logger.info(f"New items request: Total: {incoming_count}, Rejected: {rejected_count}, reject: {rejects}")
        if rejected_count == 0:
            logger.info("SUCCESS - All new items were processed")
        else:
            logger.warning(f"WARNING - {rejected_count} new items(s) were rejected")

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
