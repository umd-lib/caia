import logging
from typing import Dict, Optional

import requests

from caia.core.step import StepResult

logger = logging.getLogger(__name__)


def http_get_request(url: str, headers: Dict[str, str], query_params: Optional[Dict[str, str]] = None) -> StepResult:
    logger.info(f"Sending GET request to {url}")

    request = requests.get(url, query_params, headers=headers)
    logger.debug(f"Full request URL was {request.url}")

    status_code = request.status_code
    logger.debug(f"request completed with status code: {status_code}")

    if status_code == requests.codes.ok:
        step_result = StepResult(True, request.text)
        return step_result
    else:
        error = f"Retrieval of '{url}' failed with a status code of {status_code}"
        errors = [error]
        step_result = StepResult(False, request.text, errors)
        return step_result


def http_post_request(url: str, headers: Dict[str, str], body: str) -> StepResult:
    logger.info(f"Sending POST request to {url}")
    request = requests.post(url, data=body, headers=headers)
    status_code = request.status_code

    logger.debug(f"POST request completed with status code: {status_code}")
    if status_code == requests.codes.ok:
        step_result = StepResult(True, request.text)
        return step_result
    else:
        error = f"POST to '{url}' failed with a status code of {status_code}"
        errors = [error]
        step_result = StepResult(False, request.text, errors)
        return step_result
