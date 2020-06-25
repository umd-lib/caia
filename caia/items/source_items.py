from typing import List, Dict, Optional


class SourceItems:
    """
    Encapsulates an "items" source response
    """
    def __init__(self, new_items: List[Dict[str, str]], updated_items: List[Dict[str, str]], next_item: Optional[int]):
        """
        Creates a SourceItems object from the given source response.
        """
        self.new_items = new_items
        self.updated_items = updated_items
        self.next_item = next_item

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

    def get_next_item(self) -> Optional[int]:
        """
        Returns the index of the next item to request from the source, or None
        if there are no more items
        """
        return self.next_item

    def __str__(self) -> str:
        """
        Returns a string representation of this object.
        """
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}[new_items: {self.new_items}, updated_items: {self.updated_items}," \
               f" next_item: {self.next_item}]"
