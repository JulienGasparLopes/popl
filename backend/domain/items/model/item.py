from typing import Literal

from pydantic import BaseModel, Field

type Rarity = Literal["normal", "magic", "rare", "unique"]

# Fields aliases are relative to PoE Wiki API and should be part of a repository


class Item(BaseModel):
    name: str
    rarity: Rarity = Field(alias="rarity id")
    item_class: str = Field(alias="class id")
