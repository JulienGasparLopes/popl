import uuid
from typing import Protocol

from domain.build.model.build import Build
from pydantic import BaseModel


class ItemsObtained(BaseModel):
    helmet: bool | None = None
    body: bool | None = None
    left_hand: bool | None = None
    right_hand: bool | None = None
    left_ring: bool | None = None
    right_ring: bool | None = None
    amulet: bool | None = None
    belt: bool | None = None
    gloves: bool | None = None
    boots: bool | None = None


class BuildServicePort(Protocol):

    def get_builds(self, *, build_id: uuid.UUID | None = None) -> list[Build]: ...

    def save_build(self, *, build: Build) -> str: ...

    def delete_builds(self, *, build_ids: list[uuid.UUID]) -> None: ...

    def parse_pob_code(self, *, pob_code: str, build_set_id: str) -> Build: ...

    def get_build_sets_from_pob_code(self, *, pob_code: str) -> dict[str, str]: ...

    def set_item_obtained(
        self, *, build_id: uuid.UUID, items_obtained: ItemsObtained
    ) -> None: ...
