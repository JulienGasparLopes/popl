import html
from typing import cast

from log import get_logger
from src.backend.connectors.poe_wiki_connector import PoeWikiConnetor, ResourceQuery
from src.backend.domain.monsters.application_service.monster_service import (
    MonsterService,
    make_monster_service,
)
from src.backend.domain.monsters.model.monster import Monster

logger = get_logger(__name__)

RUN_AS_TEST = False


def main() -> None:
    """Synchronize all monsters from PoE Wiki"""

    monster_service = make_monster_service()
    monster_service = cast(MonsterService, monster_service)

    poe_wiki_conn = PoeWikiConnetor()

    query_func = (
        poe_wiki_conn._single_query_resource
        if RUN_AS_TEST
        else poe_wiki_conn.query_resource
    )

    raw_monsters = query_func(
        query=ResourceQuery(
            table_name="monsters",
            fields="name,metadata_id",
            filters={},
        )
    )

    if not RUN_AS_TEST:
        monster_service._repository.delete_many({})

    monsters = []
    for raw_monster in raw_monsters:
        monster = Monster.model_validate(
            {
                **raw_monster,
                "name": html.unescape(raw_monster.get("name")),
            }
        )
        if RUN_AS_TEST:
            logger.info(monster)
        else:
            logger.info(monster)
            monsters.append(monster)

    logger.info(f"Adding {len(monsters)} monsters")

    if monsters:
        monster_service.add_monsters(monsters=monsters)


if __name__ == "__main__":
    main()
