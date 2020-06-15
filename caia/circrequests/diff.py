from __future__ import annotations  # Needed for Python typing on "from_dict" static method

from typing import Dict, List


class DiffResult:
    """
    Encapsulates the result of diffing two source responses
    """
    def __init__(self, new_entries: List[Dict[str, str]], modified_entries: List[Dict[str, str]],
                 deleted_entries: List[Dict[str, str]]):
        self.new_entries = new_entries
        self.modified_entries = modified_entries
        self.deleted_entries = deleted_entries

    def as_dict(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Returns a Dictionary representation of this object.
        """
        result = {
            "new_entries": self.new_entries,
            "modified_entries": self.modified_entries,
            "deleted_entries": self.deleted_entries
        }
        return result

    @staticmethod
    def from_dict(dictionary: Dict[str, List[Dict[str, str]]]) -> DiffResult:
        """
        Returns a DiffResult from the given Dictionary, created the "as_dict"
        """
        new_entries = dictionary["new_entries"]
        modified_entries = dictionary["modified_entries"]
        deleted_entries = dictionary["deleted_entries"]
        return DiffResult(new_entries, modified_entries, deleted_entries)

    def __str__(self) -> str:
        """
        Returns a string representation of this object.
        """
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}[new_entries: {self.new_entries},"\
            f"modified_entries: {self.modified_entries}, deleted_entries: {self.deleted_entries}]"


def diff(key_field: str,
         previous: List[Dict[str, str]], current: List[Dict[str, str]],
         denied_keys: List[str]) -> DiffResult:
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
    denied_keys_in_current_set = set(current_keys).intersection(set(denied_keys))
    # Combine new and modified keys into a single set
    new_or_modified_keys_set = set(new_keys) | set(modified_keys)
    # Denied keys in current, and not already in "new or modified" set need to be added
    denied_keys_to_add = denied_keys_in_current_set - new_or_modified_keys_set

    for key in denied_keys_to_add:
        new_entries.append(current_as_dict[key])

    diff_result = DiffResult(new_entries, modified_entries, deleted_entries)
    return diff_result
