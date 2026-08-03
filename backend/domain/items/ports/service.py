from dataclasses import dataclass
from typing import Protocol

from domain.items.model.item import Item, Rarity


@dataclass
class ItemFilters:
    rarity: set[Rarity] | None = None
    item_class: set[str] | None = None


class ItemServicePort(Protocol):
    def get_items(self, *, filters: ItemFilters) -> list[Item]: ...

    def add_item(self, *, item: Item) -> None: ...
