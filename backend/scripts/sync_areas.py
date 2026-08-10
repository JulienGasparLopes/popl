import html
from typing import cast

from connectors.poe_wiki_connector import PoeWikiConnetor, ResourceQuery
from domain.areas.application_service.area_service import AreaService, make_area_service
from domain.areas.model.area import Area
from log import get_logger

logger = get_logger(__name__)

RUN_AS_TEST = False


def main() -> None:
    """Synchronize all areas from PoB Wiki"""

    area_service = make_area_service()
    area_service = cast(AreaService, area_service)

    poe_wiki_conn = PoeWikiConnetor()

    query_func = (
        poe_wiki_conn._single_query_resource
        if RUN_AS_TEST
        else poe_wiki_conn.query_resource
    )

    raw_areas = query_func(
        query=ResourceQuery(
            table_name="areas",
            fields="name,id",
            filters={},
        )
    )

    if not RUN_AS_TEST:
        area_service._repository.delete_many({})

    areas = []
    for raw_area in raw_areas:
        area = Area.model_validate(
            {
                **raw_area,
                "name": html.unescape(raw_area.get("name")),
            }
        )
        if RUN_AS_TEST:
            logger.info(area)
        else:
            logger.info(area)
            areas.append(area)

    logger.info(f"Adding {len(areas)} areas")

    if areas:
        area_service.add_areas(areas=areas)


if __name__ == "__main__":
    main()
