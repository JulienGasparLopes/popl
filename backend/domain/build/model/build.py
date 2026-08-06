import uuid

from pydantic import BaseModel


class CharacterAttributes(BaseModel):
    life: int
    mana: int

    strength: int
    dexterity: int
    intelligence: int

    armour: int = 0
    energy_shield: int = 0
    evasion: int = 0

    power_charges: int = 3
    endurance_charges: int = 3
    frenzy_charges: int = 3


class Equipment(BaseModel):
    helmet: str | None = None
    body: str | None = None
    left_hand: str | None = None
    right_hand: str | None = None
    left_ring: str | None = None
    right_ring: str | None = None
    amulet: str | None = None
    belt: str | None = None
    gloves: str | None = None
    boots: str | None = None


class Build(BaseModel):
    id: uuid.UUID

    character_class: str
    character_ascendancy: str
    character_attributes: CharacterAttributes

    equipment: Equipment
    gems: list[str]
    jewels: list[str]
