from __future__ import annotations  # Needed for Python typing on "from_dict" static method

from typing import Dict, List, Set, Union, cast
import datetime


class DiffResult:
    """
    Encapsulates the result of diffing two source responses
    """
    def __init__(self, new_entries: List[Dict[str, str]], modified_entries: List[Dict[str, str]],
                 deleted_entries: List[Dict[str, str]], denied_keys_to_persist: Dict[str, str]):
        self.new_entries = new_entries
        self.modified_entries = modified_entries
        self.deleted_entries = deleted_entries
        self.denied_keys_to_persist = denied_keys_to_persist

    def as_dict(self) -> Dict[str, Union[List[Dict[str, str]], Dict[str, str]]]:
        """
        Returns a Dictionary representation of this object.
        """
        result = {
            "new_entries": self.new_entries,
            "modified_entries": self.modified_entries,
            "deleted_entries": self.deleted_entries,
            "denied_keys_to_persist": self.denied_keys_to_persist
        }
        return cast(Dict[str, Union[List[Dict[str, str]], Dict[str, str]]], result)

    @staticmethod
    def from_dict(dictionary: Dict[str, Union[List[Dict[str, str]], Dict[str, str]]]) -> DiffResult:
        """
        Returns a DiffResult from the given Dictionary, created the "as_dict"
        """
        new_entries = cast(List[Dict[str, str]], dictionary["new_entries"])
        modified_entries = cast(List[Dict[str, str]], dictionary["modified_entries"])
        deleted_entries = cast(List[Dict[str, str]], dictionary["deleted_entries"])
        denied_keys_to_persist = cast(Dict[str, str], dictionary["denied_keys_to_persist"])
        return DiffResult(new_entries, modified_entries, deleted_entries, denied_keys_to_persist)

    def __str__(self) -> str:
        """
        Returns a string representation of this object.
        """
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}[new_entries: {self.new_entries}, "\
            f"modified_entries: {self.modified_entries}, deleted_entries: {self.deleted_entries}, " \
               f"denied_keys_to_persist: {self.denied_keys_to_persist}]"


def denied_keys_to_resubmit(possible_keys: Set[str], denied_keys: Dict[str, str],
                            current_time: datetime.datetime, wait_period_in_seconds: int) -> List[str]:
    """
    Return a List of keys from the given Dictionary that should be resubmitted
    because the elapsed time since their last deny date is greater than the
    given wait period.
    """
    result = []
    for possible_key in possible_keys:
        last_deny_date_str = denied_keys[possible_key]
        last_deny_date = datetime.datetime.fromisoformat(last_deny_date_str)
        time_diff = current_time - last_deny_date
        if wait_period_in_seconds < time_diff.total_seconds():
            result.append(possible_key)

    return result


def diff(key_field: str, previous: List[Dict[str, str]], current: List[Dict[str, str]],
         denied_keys: Dict[str, str], current_time: datetime.datetime, denied_items_wait_interval: int) -> DiffResult:
    """
    Compares Dictionary entries in the lists based on the given key_field,
    returning a DiffResult of new/modified/deleted entries.
    """
    previous_as_dict = {entry[key_field]: entry for entry in previous}
    current_as_dict = {entry[key_field]: entry for entry in current}
    previous_keys = previous_as_dict.keys()
    current_keys = current_as_dict.keys()

    # Keys in current only (new)
    new_keys = list(set(current_keys) - set(previous_keys))
    new_entries = []
    for key in new_keys:
        new_entries.append(current_as_dict[key])

    # Keys in previous only (deleted)
    deleted_keys = list(set(previous_keys) - set(current_keys))
    deleted_entries = []
    for key in deleted_keys:
        deleted_entries.append(previous_as_dict[key])

    # Keys in both lists (modified?)
    possibly_modified_keys = list(set(previous_keys) & set(current_keys))
    modified_entries = []
    modified_keys = []
    for key in possibly_modified_keys:
        list1_value = previous_as_dict[key]
        list2_value = current_as_dict[key]

        if list1_value != list2_value:
            modified_entries.append(current_as_dict[key])
            modified_keys.append(key)

    # Handle denied keys

    # Denied keys present in current list
    denied_keys_list = denied_keys.keys()
    denied_keys_in_current_set = set(current_keys).intersection(set(denied_keys_list))

    # Combine new and modified keys into a single set
    new_or_modified_keys_set = set(new_keys) | set(modified_keys)

    # Denied keys in current, and not already in "new or modified" set need to be added
    possible_denied_keys_to_add = denied_keys_in_current_set - new_or_modified_keys_set

    denied_keys_to_add = denied_keys_to_resubmit(possible_denied_keys_to_add, denied_keys,
                                                 current_time, denied_items_wait_interval)

    # Generate a list of denied keys that are still in the list, but will not
    # be resubmitted. These keys (and their associated timestamp) will be
    # persisted in the "denied_keys" file.
    denied_keys_to_persist_list = possible_denied_keys_to_add.difference(denied_keys_to_add)
    denied_keys_to_persist = {}
    for key in denied_keys_to_persist_list:
        denied_keys_to_persist[key] = denied_keys[key]

    for key in denied_keys_to_add:
        new_entries.append(current_as_dict[key])

    diff_result = DiffResult(new_entries, modified_entries, deleted_entries, denied_keys_to_persist)
    return diff_result
