from typing import Protocol

from src.backend.domain.areas.model.area import Area


class AreaFilters:
    name: set[str] | None
    id: set[str] | None


class AreaServicePort(Protocol):
    def add_areas(self, *, areas: list[Area]) -> None: ...

    def get_areas(self, *, filters: AreaFilters) -> list[Area]: ...
