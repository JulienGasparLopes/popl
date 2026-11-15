import os
import uuid
from functools import wraps
from typing import Any, cast

from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask, g, jsonify, redirect, request, session, url_for
from flask_cors import CORS
from log import get_logger
from src.backend.domain.build.application_service.build_service import (
    make_build_service,
)
from src.backend.domain.build.application_service.pob_build_service import (
    make_pob_build_service,
)
from src.backend.domain.build.ports.build_service import ItemsObtained
from src.backend.domain.items.application_service.service import (
    ItemService,
    make_item_service,
)
from src.backend.domain.items.ports.service import ItemFilters
from src.backend.domain.mechanics.application_service.mechanics_service import (
    make_mechanics_service,
)
from src.backend.domain.mechanics.model.mechanics import LootMechanics
from src.backend.domain.mechanics.ports.mechanics_service import LeagueMechanicsFilters
from src.backend.domain.users.application_service.service import make_user_service
from src.backend.domain.users.model.user import User
from src.backend.domain.users.ports.service import UserFilters

logger = get_logger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:3000"], supports_credentials=True)

app.config.update(
    SESSION_COOKIE_NAME="session",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,  # True in production with HTTPS
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_PATH="/",
    SESSION_COOKIE_DOMAIN=None,
)

app.secret_key = os.getenv("FLASK_AUTH_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=(
        "https://accounts.google.com/.well-known/openid-configuration"
    ),
    client_kwargs={"scope": "openid email profile"},
)


# ----- LOGIN -----
@app.route("/auth/google/login")
def google_login():
    redirect_uri = url_for("google_callback", _external=True)

    return oauth.google.authorize_redirect(redirect_uri)


@app.route("/auth/google/callback")
def google_callback():
    token = oauth.google.authorize_access_token()

    google_user = token["userinfo"]

    google_id = google_user["sub"]
    email = google_user["email"]

    user_service = make_user_service()
    found_users = user_service.get_users(filters=UserFilters(google_id={google_id}))

    user: User | None = None
    if len(found_users) > 1:
        logger.error("Multiple user match during auth should NEVER happen")
    elif found_users:
        user = found_users[0]

    if not user:
        pseudo = f"User {str(uuid.uuid4()).replace("-", "")[:8]}"
        # TODO: manage colisions
        user = User(
            id=uuid.uuid4(),
            pseudo=pseudo,
            email=email,
            google_id=google_id,
        )
        user_service.create_user(user=user)

    session.clear()
    session["user_id"] = str(user.id)

    return redirect("http://127.0.0.1:3000/mechanics")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("http://127.0.0.1:3000/mechanics")


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")

        if not user_id:
            logger.error("Unable to parse user_id during auth process")
            return jsonify({"error": "Unauthorized"}), 401

        user_service = make_user_service()
        found_users = user_service.get_users(filters=UserFilters(id={user_id}))

        if len(found_users) > 1:
            logger.error(
                "Multiple user match during token processing should NEVER happen"
            )
            return jsonify({"error": "Unauthorized"}), 401
        if not found_users:
            session.clear()
            return jsonify({"error": "Unauthorized"}), 401

        g.current_user = found_users[0]

        return func(*args, **kwargs)

    return wrapper


@app.route("/auth/me")
@login_required
def get_current_user():
    user: User = g.current_user

    return jsonify({"id": str(user.id), "email": user.email, "pseudo": user.pseudo})


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
    user_service = make_user_service()

    builds = build_service.get_builds()
    user_ids = {b.owner_id for b in builds}

    user_id_to_pseudo = {
        user.id: user.pseudo
        for user in user_service.get_users(filters=UserFilters(id=user_ids))
    }

    return {
        "builds": [
            {
                **build.model_dump(),
                "owner": {
                    "id": build.owner_id,
                    "pseudo": user_id_to_pseudo.get(build.owner_id),
                },
            }
            for build in builds
        ],
    }, 200


@app.route("/builds/<build_id>", methods=["GET"])
def get_build(build_id: str) -> list[dict[str, Any]]:
    build_service = make_build_service()
    item_service = make_item_service()

    builds = build_service.get_builds(build_id=uuid.UUID(build_id))
    build = builds[0]

    # A little bit overkill
    user_service = make_user_service()
    user_ids = {b.owner_id for b in builds}
    user_id_to_pseudo = {
        user.id: user.pseudo
        for user in user_service.get_users(filters=UserFilters(id=user_ids))
    }

    item_names = {item.name for item in build.required_items}
    items = item_service.get_items(filters=ItemFilters(name=item_names))

    return {
        "build": {
            **build.model_dump(),
            "owner": {
                "id": build.owner_id,
                "pseudo": user_id_to_pseudo.get(build.owner_id),
            },
            "item_name_to_inventory_icon": {i.name: i.inventory_icon for i in items},
        },
    }, 200


@app.route("/pob/parse_build_sets", methods=["POST"])
@login_required
def parse_build_sets() -> list[dict[str, Any]]:
    pob_code = request.json.get("pob_code")
    build_service = make_pob_build_service()
    build_set_mapping = build_service.get_build_sets_from_pob_code(pob_code=pob_code)

    return {"build_sets": build_set_mapping}, 200


@app.route("/pob/create_build", methods=["POST"])
@login_required
def post_build() -> list[dict[str, Any]]:
    user: User = g.current_user

    pob_code = request.json.get("pob_code")
    build_set_id = request.json.get("build_set_id")
    pob_build_service = make_pob_build_service()
    build_service = make_build_service()

    build = pob_build_service.parse_pob_code(
        pob_code=pob_code, build_set_id=build_set_id, owner_id=user.id
    )
    build_service.save_build(build=build)

    return {
        "status": "ok",
        "build_id": str(build.id),
    }, 200


@app.route("/builds/<build_id_str>/set_items_obtained", methods=["POST"])
@login_required
def set_items_obtained(build_id_str: str) -> list[dict[str, Any]]:
    build_id = uuid.UUID(build_id_str)
    user: User = g.current_user

    build_service = make_build_service()

    builds = build_service.get_builds(build_id=build_id)
    if not builds or builds[0].owner_id != user.id:
        return {}, 401

    items_obtained = ItemsObtained.model_validate(request.json)
    build_service.set_item_obtained(build_id=build_id, items_obtained=items_obtained)

    return {"status": "ok"}, 200


@app.route("/mechanics", methods=["GET"])
def get_mechanics_mapping() -> list[dict[str, Any]]:
    mechanics_service = make_mechanics_service()
    user_service = make_user_service()

    mechanics_mapping = mechanics_service.get_league_mechanics_mappings(
        filters=LeagueMechanicsFilters()
    )
    league_mechanics_names = mechanics_service.get_league_mechanics_names()

    user_ids = {b.owner_id for b in mechanics_mapping}
    user_id_to_pseudo = {
        user.id: user.pseudo
        for user in user_service.get_users(filters=UserFilters(id=user_ids))
    }

    return {
        "mechanics_mappings": [
            {**m.model_dump(), "pseudo": user_id_to_pseudo.get(m.owner_id)}
            for m in mechanics_mapping
        ],
        "league_mechanics": league_mechanics_names,
        "owner_ids": [m.owner_id for m in mechanics_mapping],
    }


@app.route("/mechanics/<owner_id_str>", methods=["POST"])
@login_required
def set_user_mechanics_mapping(owner_id_str: str) -> list[dict[str, Any]]:
    user: User = g.current_user

    owner_id = uuid.UUID(owner_id_str)

    if user.id != owner_id:
        return {}, 401

    mechanics_service = make_mechanics_service()
    mechanics_mappings = mechanics_service.get_league_mechanics_mappings(
        filters=LeagueMechanicsFilters(owner_id={owner_id})
    )

    if not mechanics_mappings:
        loot_mechanics = LootMechanics()
    else:
        loot_mechanics = mechanics_mappings[0].loot_mechanics

    for key, value in request.json.items():
        loot_mechanics.__setattr__(key, value)

    mechanics_service.set_league_mechanics(owner_id=owner_id, mechanics=loot_mechanics)

    return {"status": "ok"}, 200


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
