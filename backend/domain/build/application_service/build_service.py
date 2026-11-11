import uuid

from connectors.mongo_connector import MongoConnector
from domain.build.model.build import Build
from domain.build.ports.build_service import BuildServicePort, ItemsObtained, WantedItem
from log import get_logger

logger = get_logger(__name__)


class BuildService(BuildServicePort):

    def __init__(self):
        conn = MongoConnector()
        self._repository = conn.get_collection("builds")

    def get_builds(self, *, build_id: uuid.UUID | None = None) -> list[Build]:
        filters = {}
        if build_id is not None:
            filters["id"] = str(build_id)
        raw_builds = self._repository.find(filters)
        return [Build.model_validate(raw_build) for raw_build in raw_builds]

    def save_build(self, *, build: Build) -> str:
        data = {
            **build.model_dump(exclude=["id"]),
            "id": str(build.id),
            "owner_id": str(build.owner_id),
        }
        self._repository.update_one({"id": str(build.id)}, {"$set": data}, upsert=True)

    def delete_builds(self, *, build_ids: list[uuid.UUID]) -> None:
        self._repository.delete_many({"id": {"$in": [str(b) for b in build_ids]}})

    def set_item_obtained(
        self, *, build_id: uuid.UUID, items_obtained: ItemsObtained
    ) -> None:
        build = self.get_builds(build_id=build_id)[0]

        if items_obtained.helmet is not None:
            build.equipment.helmet.obtained = items_obtained.helmet
        if items_obtained.body is not None:
            build.equipment.body.obtained = items_obtained.body
        if items_obtained.gloves is not None:
            build.equipment.gloves.obtained = items_obtained.gloves
        if items_obtained.boots is not None:
            build.equipment.boots.obtained = items_obtained.boots
        if items_obtained.left_hand is not None:
            build.equipment.left_hand.obtained = items_obtained.left_hand
        if items_obtained.right_hand is not None:
            build.equipment.right_hand.obtained = items_obtained.right_hand
        if items_obtained.left_ring is not None:
            build.equipment.left_ring.obtained = items_obtained.left_ring
        if items_obtained.right_ring is not None:
            build.equipment.right_ring.obtained = items_obtained.right_ring
        if items_obtained.amulet is not None:
            build.equipment.amulet.obtained = items_obtained.amulet
        if items_obtained.belt is not None:
            build.equipment.belt.obtained = items_obtained.belt

        if items_obtained.jewels is not None:
            for index, obtained in items_obtained.jewels.items():
                build.jewels[index].obtained = obtained

        self.save_build(build=build)

    def get_wanted_items(self) -> list[WantedItem]:
        wanted_items: list[WantedItem] = []
        builds = self.get_builds()

        for build in builds:
            for required_item in build.required_items:
                if not required_item.obtained:
                    wanted_items.append(
                        WantedItem(
                            user_id="Pinzen",
                            item_name=required_item.name,
                        )
                    )

        return wanted_items


def make_build_service() -> BuildServicePort:
    return BuildService()
