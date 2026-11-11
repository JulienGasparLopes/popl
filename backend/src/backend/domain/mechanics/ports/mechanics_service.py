import uuid
from dataclasses import dataclass
from typing import Protocol

from src.backend.domain.mechanics.model.mechanics import LootMechanics, MechanicsMapping


@dataclass
class LeagueMechanicsFilters:
    owner_id: set[uuid.UUID] | None = None


class LeagueMechanicsServicePort(Protocol):
    def get_league_mechanics_names(self) -> list[str]: ...

    def get_league_mechanics_mappings(
        self, *, filters: LeagueMechanicsFilters
    ) -> list[MechanicsMapping]: ...

    def set_league_mechanics(
        self, *, owner_id: uuid.UUID, mechanics: LootMechanics
    ) -> None: ...
