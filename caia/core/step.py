import abc
from typing import Any, List
import logging

logger = logging.getLogger(__name__)


class StepResult:
    """
    Encapsulates the result of a Step.
    """
    def __init__(self, success: bool, result: Any, errors: List[str] = []):
        """
        StepResult Constructor
        success: True if the step was successful, False otherwise.
        result: The result (return value) of the Step. May be None.
        errors: A list of errors, indicating why the step failed.
        """
        self.success = success
        self.result = result
        self.errors = errors

    def was_successful(self) -> bool:
        return self.success

    def get_result(self) -> Any:
        return self.result

    def get_errors(self) -> List[str]:
        return self.errors

    def __str__(self) -> str:
        """
         Returns a string representation of this object.
         """
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}[success: {self.success}, result: {self.result},  errors: {self.errors}]"


class Step(metaclass=abc.ABCMeta):
    """
    An interface for individual steps in the pipeline.
    """
    @abc.abstractmethod
    def execute(self) -> StepResult:
        """
        Returns True is the step succeeded, False otherwise. If execution fails,
        the "errors" method should return a meaningful error message.
        """
        raise NotImplementedError
