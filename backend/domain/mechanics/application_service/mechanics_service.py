import uuid

from connectors.mongo_connector import MongoConnector
from domain.mechanics.model.mechanics import (
    LEAGUE_LOOT_MECHANICS,
    LootMechanics,
    MechanicsMapping,
)
from domain.mechanics.ports.mechanics_service import (
    LeagueMechanicsFilters,
    LeagueMechanicsServicePort,
)


class LeagueMechanicsService(LeagueMechanicsServicePort):
    def __init__(self):
        conn = MongoConnector()
        self._repository = conn.get_collection("mechanics")

    def get_league_mechanics_names(self) -> list[str]:
        return LEAGUE_LOOT_MECHANICS

    def get_league_mechanics_mappings(
        self, *, filters: LeagueMechanicsFilters
    ) -> list[MechanicsMapping]:
        query_filters = {}
        if filters.owner_id is not None:
            query_filters = {
                "owner_id": {"$in": [str(owner_id) for owner_id in filters.owner_id]}
            }

        raw_mechanics = self._repository.find(query_filters)
        return [
            MechanicsMapping.model_validate(raw_mechanic)
            for raw_mechanic in raw_mechanics
        ]

    def set_league_mechanics(
        self, *, owner_id: uuid.UUID, mechanics: LootMechanics
    ) -> None:
        data = {"owner_id": str(owner_id), "loot_mechanics": mechanics.model_dump()}
        self._repository.update_one(
            {"owner_id": str(owner_id)}, {"$set": data}, upsert=True
        )


def make_mechanics_service() -> LeagueMechanicsServicePort:
    return LeagueMechanicsService()
