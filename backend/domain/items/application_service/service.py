from connectors.mongo_connector import MongoConnector
from domain.items.model.item import Item
from domain.items.ports.service import ItemFilters, ItemServicePort


class ItemService(ItemServicePort):
    def __init__(self):
        self._mongo_conn = MongoConnector()
        self._repository = self._mongo_conn.get_collection("items")

    def get_items(self, *, filters: ItemFilters) -> list[Item]:
        query_filters = {}
        if filters.rarity is not None:
            query_filters["rarity"] = {"$in": list(filters.rarity)}
        if filters.item_class is not None:
            query_filters["item_class"] = {"$in": list(filters.item_class)}

        raw_items = self._repository.find(query_filters)

        return [Item.model_validate(raw_item, by_name=True) for raw_item in raw_items]

    def add_item(self, *, item: Item) -> None:
        _result = self._repository.update_one(
            {"name": item.name},
            {"$set": item.model_dump(exclude={"id"})},
            upsert=True,
        )
        # return _result.upserted_id

    def add_items(self, *, items: list[Item]) -> None:
        self._repository.insert_many(
            [item.model_dump(exclude={"id"}) for item in items]
        )


def make_item_service() -> ItemServicePort:
    return ItemService()
