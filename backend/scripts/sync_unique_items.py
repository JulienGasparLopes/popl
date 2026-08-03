from connectors.mongo_connector import MongoConnector
from connectors.poe_wiki_connector import PoeWikiConnetor, ResourceQuery
from domain.items.application_service.service import ItemService
from domain.items.model.item import Item
from log import get_logger

logger = get_logger(__name__)


def main() -> None:
    mongo_conn = MongoConnector()
    item_service = ItemService(mongo_connector=mongo_conn)

    poe_wiki_conn = PoeWikiConnetor()

    raw_items = poe_wiki_conn.query_resource(
        query=ResourceQuery(
            table_name="items",
            fields="name,rarity_id,class_id",
            filters={"rarity": "Unique"},
        )
    )

    for raw_item in raw_items:
        item = Item.model_validate(raw_item)
        logger.info(f"Adding Item {item}")
        item_service.add_item(item=item)


if __name__ == "__main__":
    main()
