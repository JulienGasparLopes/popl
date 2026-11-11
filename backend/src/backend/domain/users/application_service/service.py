from src.backend.connectors.mongo_connector import MongoConnector
from src.backend.domain.users.model.user import User
from src.backend.domain.users.ports.service import UserFilters, UserServicePort


class UserService(UserServicePort):
    def __init__(self):
        self._mongo_conn = MongoConnector()
        self._repository = self._mongo_conn.get_collection("users")

    def get_users(self, *, filters: UserFilters) -> list[User]:
        query_filters = {}
        if filters.id is not None:
            query_filters["id"] = {"$in": [str(user_id) for user_id in filters.id]}
        if filters.google_id is not None:
            query_filters["google_id"] = {"$in": list(filters.google_id)}
        if filters.pseudo is not None:
            query_filters["pseudo"] = {"$in": list(filters.pseudo)}

        raw_users = self._repository.find(query_filters)

        return [User.model_validate(raw_user, by_name=True) for raw_user in raw_users]

    def create_user(self, *, user: User) -> None:
        data = {**user.model_dump(exclude=["id"]), "id": str(user.id)}
        self._repository.insert_one(data)


def make_user_service() -> UserServicePort:
    return UserService()
