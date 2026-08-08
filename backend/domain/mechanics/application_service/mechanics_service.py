from connectors.mongo_connector import MongoConnector
from domain.mechanics.model.mechanics import (
    LEAGUE_LOOT_MECHANICS,
    LootMechanics,
    MechanicsMapping,
)
from domain.mechanics.ports.mechanics_service import LeagueMechanicsServicePort


class LeagueMechanicsService(LeagueMechanicsServicePort):
    def __init__(self):
        conn = MongoConnector()
        self._repository = conn.get_collection("mechanics")

    def get_league_mechanics_names(self) -> list[str]:
        return LEAGUE_LOOT_MECHANICS

    def get_league_mechanics_mappings(
        self, *, user_ids: list[str] | None = None
    ) -> list[MechanicsMapping]:
        filters = {}
        if user_ids is not None:
            filters = {"user_id": {"$in": user_ids}}

        raw_mechanics = self._repository.find(filters)
        return [
            MechanicsMapping.model_validate(raw_mechanic)
            for raw_mechanic in raw_mechanics
        ]

    def set_league_mechanics(self, *, user_id: str, mechanics: LootMechanics) -> None:
        data = {"user_id": user_id, "loot_mechanics": mechanics.model_dump()}
        self._repository.update_one({"user_id": user_id}, {"$set": data}, upsert=True)


def make_mechanics_service() -> LeagueMechanicsServicePort:
    return LeagueMechanicsService()
