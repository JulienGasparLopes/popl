import uuid
from typing import Protocol

from pydantic import BaseModel
from src.backend.domain.build.model.build import Build


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

    jewels: dict[int, bool] | None = None


class WantedItem(BaseModel):
    user_id: str
    item_name: str


class BuildServicePort(Protocol):

    def get_builds(self, *, build_id: uuid.UUID | None = None) -> list[Build]: ...

    def save_build(self, *, build: Build) -> str: ...

    def delete_builds(self, *, build_ids: list[uuid.UUID]) -> None: ...

    def set_item_obtained(
        self, *, build_id: uuid.UUID, items_obtained: ItemsObtained
    ) -> None: ...

    def get_wanted_items(self) -> list[WantedItem]: ...
