from typing import Protocol

from domain.mechanics.model.mechanics import LootMechanics, MechanicsMapping


class LeagueMechanicsServicePort(Protocol):
    def get_league_mechanics_names(self) -> list[str]: ...

    def get_league_mechanics_mappings(
        self, *, user_ids: list[str] | None = None
    ) -> list[MechanicsMapping]: ...

    def set_league_mechanics(
        self, *, user_id: str, mechanics: LootMechanics
    ) -> None: ...
