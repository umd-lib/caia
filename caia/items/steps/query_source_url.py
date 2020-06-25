import logging
from typing import List, Optional

from caia.core.http import http_get_request
from caia.core.step import Step, StepResult
from caia.items.items_job_config import ItemsJobConfig

logger = logging.getLogger(__name__)


class QuerySourceUrl(Step):
    """
    Queries the source url and stores a successful response.
    """
    def __init__(self, job_config: ItemsJobConfig, last_timestamp: str, current_timestamp: str,
                 next_item: Optional[int]):
        self.job_config = job_config
        self.last_timestamp = last_timestamp
        self.current_timestamp = current_timestamp
        self.errors: List[str] = []
        self.next_item = next_item

    def execute(self) -> StepResult:
        source_url = self.job_config['source_url']
        headers = {'Content-Type': 'application/json'}
        query_params = {"starttime": self.last_timestamp, "endtime": self.current_timestamp}
        if self.next_item is not None:
            query_params['nextitem'] = str(self.next_item)

        return http_get_request(source_url, headers, query_params)

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
