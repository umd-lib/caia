from typing import List, Dict


class SourceItems:
    """
    Encapsulates an "items" source response
    """
    def __init__(self, new_items: List[Dict[str, str]], updated_items: List[Dict[str, str]]):
        """
        Creates a SourceItems object from the given source response.
        """
        self.new_items = new_items
        self.updated_items = updated_items

    def get_new_items(self) -> List[Dict[str, str]]:
        """
        Returns a (possibly empty) list of new items
        """
        return self.new_items

    def get_updated_items(self) -> List[Dict[str, str]]:
        """
        Returns a (possibly empty) list of updated items
        """
        return self.updated_items

    def __str__(self) -> str:
        """
        Returns a string representation of this object.
        """
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}[new_items: {self.new_items}, updated_items: {self.updated_items}]"
