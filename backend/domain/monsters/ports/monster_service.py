from typing import Protocol

from domain.monsters.model.monster import Monster


class MonsterFilters:
    name: set[str] | None
    metadata_id: set[str] | None


class MonsterServicePort(Protocol):
    def add_monsters(self, *, monsters: list[Monster]) -> None: ...

    def get_monsters(self, *, filters: MonsterFilters) -> list[Monster]: ...
