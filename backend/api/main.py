import uuid
from typing import Any, cast

from domain.build.application_service.build_service import make_build_service
from domain.build.ports.build_service import ItemsObtained
from domain.items.application_service.service import ItemService, make_item_service
from domain.items.ports.service import ItemFilters
from domain.mechanics.application_service.mechanics_service import (
    make_mechanics_service,
)
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Welcome to the API !</p>"


@app.route("/items", methods=["GET"])
def get_all_users() -> list[dict[str, Any]]:
    item_class = request.args.get("item_class")

    item_service = make_item_service()
    items = item_service.get_items(
        filters=ItemFilters(item_class={item_class} if item_class is not None else None)
    )

    return {
        "items": [item.model_dump() for item in items],
        "count": len(items),
    }, 200


@app.route("/item_class", methods=["GET"])
def get_all_item_class() -> list[dict[str, Any]]:
    item_service = make_item_service()
    item_service = cast(ItemService, item_service)
    item_classes = item_service._repository.distinct("item_class")

    return {"item_classes": item_classes}, 200


@app.route("/builds", methods=["GET"])
def get_builds() -> list[dict[str, Any]]:
    build_service = make_build_service()
    builds = build_service.get_builds()

    return {
        "builds": [build.model_dump() for build in builds],
    }, 200


@app.route("/builds/<build_id>", methods=["GET"])
def get_build(build_id: str) -> list[dict[str, Any]]:
    build_service = make_build_service()
    builds = build_service.get_builds(build_id=uuid.UUID(build_id))
    assert len(builds) == 1

    return {
        "build": builds[0].model_dump(),
    }, 200


@app.route("/pob/parse_build_sets", methods=["POST"])
def parse_build_sets() -> list[dict[str, Any]]:
    pob_code = request.json.get("pob_code")
    build_service = make_build_service()
    build_set_mapping = build_service.get_build_sets_from_pob_code(pob_code=pob_code)

    return {"build_sets": build_set_mapping}, 200


@app.route("/pob/create_build", methods=["POST"])
def post_build() -> list[dict[str, Any]]:
    pob_code = request.json.get("pob_code")
    build_set_id = request.json.get("build_set_id")
    build_service = make_build_service()
    build = build_service.parse_pob_code(pob_code=pob_code, build_set_id=build_set_id)
    build_service.save_build(build=build)

    return {
        "status": "ok",
        "build_id": str(build.id),
    }, 200


@app.route("/builds/<build_id>/set_items_obtained", methods=["POST"])
def set_items_obtained(build_id: str) -> list[dict[str, Any]]:
    items_obtained = ItemsObtained.model_validate(request.json)
    build_service = make_build_service()
    build_service.set_item_obtained(build_id=build_id, items_obtained=items_obtained)

    return {
        "status": "ok",
    }, 200


@app.route("/mechanics", methods=["GET"])
def get_mechanics_mapping() -> list[dict[str, Any]]:
    mechanics_service = make_mechanics_service()
    mechanics_mapping = mechanics_service.get_league_mechanics_mappings()
    league_mechanics_names = mechanics_service.get_league_mechanics_names()

    return {
        "mechanics_mappings": [m.model_dump() for m in mechanics_mapping],
        "league_mechanics": league_mechanics_names,
        "users_names": [m.user_id for m in mechanics_mapping],
    }


@app.route("/mechanics/<user_id>", methods=["POST"])
def set_user_mechanics_mapping(user_id: str) -> list[dict[str, Any]]:
    mechanics_service = make_mechanics_service()
    loot_mechanics = mechanics_service.get_league_mechanics_mappings(
        user_ids=[user_id]
    )[0].loot_mechanics

    for key, value in request.json.items():
        loot_mechanics.__setattr__(key, value)

    mechanics_service.set_league_mechanics(user_id=user_id, mechanics=loot_mechanics)

    return {
        "status": "ok",
    }, 200


@app.route("/wanted_items", methods=["GET"])
def get_wanted_items() -> list[dict[str, Any]]:
    build_service = make_build_service()
    item_service = make_item_service()

    wanted_items = build_service.get_wanted_items()

    wanted_items_mapping: dict[str, dict[str, dict[str, int]]] = {}
    for wanted_item in wanted_items:
        if not wanted_item.item_name in wanted_items_mapping:
            wanted_items_mapping[wanted_item.item_name] = {"users": {}, "total": 0}

        if (
            not wanted_item.user_id
            in wanted_items_mapping[wanted_item.item_name]["users"]
        ):
            wanted_items_mapping[wanted_item.item_name]["users"][
                wanted_item.user_id
            ] = 0

        wanted_items_mapping[wanted_item.item_name]["users"][wanted_item.user_id] += 1
        wanted_items_mapping[wanted_item.item_name]["total"] += 1

    items_info = item_service.get_items(
        filters=ItemFilters(name={k for k in wanted_items_mapping})
    )
    for item_info in items_info:
        wanted_items_mapping[item_info.name]["info"] = item_info.model_dump()

    return wanted_items_mapping, 200
