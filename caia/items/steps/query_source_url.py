import logging
from typing import List, Optional

from caia.core.http import http_get_request
from caia.core.step import Step, StepResult
from caia.items.items_job_config import ItemsJobConfig

logger = logging.getLogger(__name__)


class QuerySourceUrl(Step):
    """
    Queries the source url and stores a successful response.

    job_config: The ItemsJobConfig containing the current job information
    start_time: The date/timestamp of the beginning of the query range
    end_time: The date/timestamp of the end of the query range as returned
              by the source. Should be may be None on the first iteration
    next_item: The next_item to query for, as returned by the source when
               multiple query iterations are needed.
    """
    def __init__(self, job_config: ItemsJobConfig, start_time: str, end_time: Optional[str],
                 next_item: Optional[str]):
        self.job_config = job_config
        self.start_time = start_time
        self.end_time = end_time
        self.errors: List[str] = []
        self.next_item = next_item

    def execute(self) -> StepResult:
        source_url = self.job_config['source_url']
        headers = {'Content-Type': 'application/json'}
        query_params = {"starttime": self.start_time}
        if self.end_time is not None:
            query_params['endtime'] = self.end_time
        if self.next_item is not None:
            query_params['nextitem'] = self.next_item

        return http_get_request(source_url, headers, query_params)

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)} [start_time={self.start_time}, end_time={self.end_time}, " \
               f"next_item={self.next_item}]"
