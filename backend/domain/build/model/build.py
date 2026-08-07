import uuid

from pydantic import BaseModel


class RequiredItem(BaseModel):
    name: str
    obtained: bool = False


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
    helmet: RequiredItem | None = None
    body: RequiredItem | None = None
    left_hand: RequiredItem | None = None
    right_hand: RequiredItem | None = None
    left_ring: RequiredItem | None = None
    right_ring: RequiredItem | None = None
    amulet: RequiredItem | None = None
    belt: RequiredItem | None = None
    gloves: RequiredItem | None = None
    boots: RequiredItem | None = None


class Build(BaseModel):
    id: uuid.UUID

    character_class: str
    character_ascendancy: str
    character_attributes: CharacterAttributes

    equipment: Equipment
    gems: list[RequiredItem]
    jewels: list[RequiredItem]
