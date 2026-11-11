from src.backend.connectors.mongo_connector import MongoConnector
from src.backend.domain.monsters.model.monster import Monster
from src.backend.domain.monsters.ports.monster_service import (
    MonsterFilters,
    MonsterServicePort,
)


class MonsterService(MonsterServicePort):
    def __init__(self):
        conn = MongoConnector()
        self._repository = conn.get_collection("monsters")

    def add_monsters(self, *, monsters: list[Monster]) -> None:
        self._repository.insert_many([monster.model_dump() for monster in monsters])

    def get_monsters(self, *, filters: MonsterFilters) -> list[Monster]:
        filters = {}
        if filters.metadata_id is not None:
            filters["metadata_id"] = list(filters.metadata_id)
        if filters.name is not None:
            filters["name"] = list(filters.name)

        raw_monsters = self._repository.find(filters)
        return [
            Monster.model_validate(raw_monster, by_name=True)
            for raw_monster in raw_monsters
        ]


def make_monster_service() -> MonsterServicePort:
    return MonsterService()
