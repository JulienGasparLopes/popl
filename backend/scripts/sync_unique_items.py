import html
from typing import cast

from connectors.poe_wiki_connector import PoeWikiConnetor, ResourceQuery
from domain.items.application_service.service import ItemService, make_item_service
from domain.items.model.item import Item
from log import get_logger

logger = get_logger(__name__)

RUN_AS_TEST = False


def main() -> None:
    """Synchronize all uniques items from PoB Wiki"""

    item_service = make_item_service()
    item_service = cast(ItemService, item_service)

    poe_wiki_conn = PoeWikiConnetor()

    query_func = (
        poe_wiki_conn._single_query_resource
        if RUN_AS_TEST
        else poe_wiki_conn.query_resource
    )

    raw_items = query_func(
        query=ResourceQuery(
            table_name="items",
            fields="drop_areas,drop_monsters,drop_text,metadata_id,is_drop_restricted,acquisition_tags,name,rarity_id,class_id,tags",
            filters={"rarity": "Unique", "is_in_game": "1", "drop_enabled": "1"},
        )
    )

    if not RUN_AS_TEST:
        item_service._repository.delete_many({})

    items = []
    for raw_item in raw_items:
        item = Item.model_validate(
            {**raw_item, "name": html.unescape(raw_item.get("name"))}
        )
        if RUN_AS_TEST:
            logger.info(item)
            logger.info("======")
        else:
            logger.info(f"Adding Item {item.name}")
            items.append(item)

    item_service.add_items(items=items)


if __name__ == "__main__":
    main()
