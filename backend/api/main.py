import uuid
from typing import Any, cast

from domain.build.application_service.build_service import make_build_service
from domain.build.ports.build_service import ItemsObtained
from domain.items.application_service.service import ItemService, make_item_service
from domain.items.ports.service import ItemFilters
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
