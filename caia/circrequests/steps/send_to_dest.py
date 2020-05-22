from caia.core.step import Step, StepResult
from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
import requests
import logging
import json
from typing import List

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

        logger.info(f"Sending POST request to {dest_url}")
        request = requests.post(dest_url, data=body_str, headers=headers)
        status_code = request.status_code

        logger.debug(f"POST request completed with status code: {status_code}")
        if status_code == requests.codes.ok:
            step_result = StepResult(True, request.text)
            self.log_response(request.text)
            return step_result
        else:
            error = f"POST to '{dest_url}' failed with a status code of {status_code}"
            self.errors.append(error)
            step_result = StepResult(False, request.text, self.errors)
            return step_result

    @staticmethod
    def log_response(response_body_text: str):
        response = json.loads(response_body_text)
        request_count = int(response["request_count"])
        results = response["results"]
        processed_count = 0
        denied_count = 0
        for result in results:
            deny = result["deny"]
            if deny == "N":
                processed_count = processed_count + 1
            else:
                denied_count = denied_count + 1

        logger.info(f"Total requests: {request_count}, Processed: {processed_count}, Denied: {denied_count}")
        if request_count == processed_count:
            logger.info("SUCCESS - All requests were processed")
        else:
            logger.warning(f"WARNING - {denied_count} request(s) were denied")

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
