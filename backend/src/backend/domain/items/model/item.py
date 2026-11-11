from typing import Literal

from pydantic import BaseModel, Field

type Rarity = Literal["normal", "magic", "rare", "unique"]

# Fields aliases are relative to PoE Wiki API and should be part of a repository


class Item(BaseModel):
    name: str
    rarity: Rarity = Field(alias="rarity id")
    item_class: str = Field(alias="class id")

    is_drop_restricted: str = Field(alias="is drop restricted")
    drop_areas: str | None = Field(alias="drop areas")
    drop_monsters: str | None = Field(alias="drop monsters")
    drop_text: str | None = Field(alias="drop text")

    inventory_icon: str | None = Field(alias="inventory icon")

    acquisition_tags: str | None = Field(alias="acquisition tags")

    metadata_id: str | None = Field(alias="metadata id")
    tags: str = Field(alias="tags")
