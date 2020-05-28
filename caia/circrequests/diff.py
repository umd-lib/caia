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


def diff(key_field: str, list1: List[Dict[str, str]], list2: List[Dict[str, str]]) -> DiffResult:
    """
    Compares Dictionary entries in the lists based on the given key_field,
    returning a DiffResult of new/modified/deleted entries.
    """
    list1_as_dict = {entry[key_field]: entry for entry in list1}
    list2_as_dict = {entry[key_field]: entry for entry in list2}
    list1_keys = list1_as_dict.keys()
    list2_keys = list2_as_dict.keys()

    # Keys in list2 only (new)
    new_keys = list(set(list2_keys) - set(list1_keys))
    new_entries = []
    for key in new_keys:
        new_entries.append(list2_as_dict[key])

    # Keys in list1 only (deleted)
    deleted_keys = list(set(list1_keys) - set(list2_keys))
    deleted_entries = []
    for key in deleted_keys:
        deleted_entries.append(list1_as_dict[key])

    # Keys in both lists (modified?)
    possibly_modified_keys = list(set(list1_keys) & set(list2_keys))
    modified_entries = []
    for key in possibly_modified_keys:
        list1_value = list1_as_dict[key]
        list2_value = list2_as_dict[key]

        if list1_value != list2_value:
            modified_entries.append(list2_as_dict[key])

    diff_result = DiffResult(new_entries, modified_entries, deleted_entries)
    return diff_result
