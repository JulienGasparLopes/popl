from typing import Any, cast

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
