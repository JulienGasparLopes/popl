import html
from typing import cast

from connectors.mongo_connector import MongoConnector
from connectors.poe_wiki_connector import PoeWikiConnetor, ResourceQuery
from domain.items.application_service.service import ItemService, make_item_service
from domain.items.model.item import Item
from log import get_logger
from pymongo.collection import Collection

logger = get_logger(__name__)

RUN_AS_TEST = False

IMPORT_POE_WIKI_DATA = False


def copy_poe_wiki_data(poe_wiki_repo: Collection) -> None:
    poe_wiki_conn = PoeWikiConnetor()

    query_func = (
        poe_wiki_conn._single_query_resource
        if RUN_AS_TEST
        else poe_wiki_conn.query_resource
    )

    raw_items = query_func(
        query=ResourceQuery(
            table_name="items",
            fields="drop_areas,drop_monsters,drop_text,metadata_id,is_drop_restricted,acquisition_tags,name,rarity_id,class_id,tags,inventory_icon",
            filters={"rarity": "Unique", "is_in_game": "1", "drop_enabled": "1"},
        )
    )

    poe_wiki_repo.delete_many({})
    poe_wiki_repo.insert_many(raw_items)
    logger.info(f"Inserted {len(raw_items)} items")


def transform_load_items(poe_wiki_repo: Collection) -> None:
    """Synchronize all uniques items from PoE Wiki"""

    item_service = make_item_service()
    item_service = cast(ItemService, item_service)

    if not RUN_AS_TEST:
        item_service._repository.delete_many({})

    items = []
    for raw_item in poe_wiki_repo.find({}):
        drop_text = raw_item.get("drop text")
        item = Item.model_validate(
            {
                **raw_item,
                "name": html.unescape(raw_item.get("name")),
                "drop text": (
                    html.unescape(drop_text) if drop_text is not None else None
                ),
                "inventory icon": html.unescape(raw_item.get("inventory icon"))
                .replace(" ", "_")
                .replace("File:", "FilePath/"),
            }
        )
        if RUN_AS_TEST:
            logger.info(item)
            logger.info("======")
        else:
            logger.info(f"Adding Item {item.name}")
            items.append(item)

    if items:
        item_service.add_items(items=items)


if __name__ == "__main__":
    mongo_conn = MongoConnector()
    item_repo = mongo_conn.get_collection("poe_wiki_items")

    if IMPORT_POE_WIKI_DATA:
        copy_poe_wiki_data(item_repo)

    transform_load_items(item_repo)
