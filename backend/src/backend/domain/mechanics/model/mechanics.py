import uuid
from typing import Literal

from pydantic import BaseModel, Field

type RunLevel = Literal["primary", "secondary", "none"]


class LootMechanics(BaseModel):
    abyss: RunLevel = Field(default="none")
    bestiary: RunLevel = "none"
    betrayal: RunLevel = "none"
    beyond: RunLevel = "none"
    blight: RunLevel = "none"
    breach: RunLevel = "none"
    delirium: RunLevel = "none"
    delve: RunLevel = "none"
    essence: RunLevel = "none"
    expedition: RunLevel = "none"
    harvest: RunLevel = "none"
    heist: RunLevel = "none"
    incursion: RunLevel = "none"
    legion: RunLevel = "none"
    mercenaries: RunLevel = "none"
    ritual: RunLevel = "none"
    sanctum: RunLevel = "none"
    settlers: RunLevel = "none"
    ultimatum: RunLevel = "none"
    warbands: RunLevel = "none"


# Not used currently
class OtherMechanics(BaseModel):
    affliction: RunLevel = "none"
    ambush: RunLevel = "none"
    anarchy: RunLevel = "none"
    domination: RunLevel = "none"
    # rampage: RunLevel = "none" # Not really a mechanics but listed on wiki
    sentinel: RunLevel = "none"
    tempest: RunLevel = "none"
    torment: RunLevel = "none"


LEAGUE_LOOT_MECHANICS = list(LootMechanics.model_fields.keys())

# Not used currently
LEAGUE_OTHER_MECHANICS = list(OtherMechanics.model_fields.keys())


class MechanicsMapping(BaseModel):
    owner_id: uuid.UUID

    loot_mechanics: LootMechanics
    # other_mechanics: OtherMechanics
