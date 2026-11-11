from src.backend.connectors.mongo_connector import MongoConnector
from src.backend.domain.areas.model.area import Area
from src.backend.domain.areas.ports.area_service import AreaFilters, AreaServicePort


class AreaService(AreaServicePort):
    def __init__(self):
        conn = MongoConnector()
        self._repository = conn.get_collection("areas")

    def add_areas(self, *, areas: list[Area]) -> None:
        self._repository.insert_many([area.model_dump() for area in areas])

    def get_areas(self, *, filters: AreaFilters) -> list[Area]:
        filters = {}
        if filters.id is not None:
            filters["id"] = list(filters.id)
        if filters.name is not None:
            filters["name"] = list(filters.name)

        raw_areas = self._repository.find(filters)
        return [Area.model_validate(raw_area, by_name=True) for raw_area in raw_areas]


def make_area_service() -> AreaServicePort:
    return AreaService()
