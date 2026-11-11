from connectors.mongo_connector import MongoConnector
from domain.users.model.user import User
from domain.users.ports.service import UserFilters, UserServicePort


class UserService(UserServicePort):
    def __init__(self):
        self._mongo_conn = MongoConnector()
        self._repository = self._mongo_conn.get_collection("users")

    def get_users(self, *, filters: UserFilters) -> list[User]:
        query_filters = {}
        if filters.id is not None:
            query_filters["id"] = {"$in": list(filters.id)}
        if filters.google_id is not None:
            query_filters["google_id"] = {"$in": list(filters.google_id)}

        raw_users = self._repository.find(query_filters)

        return [User.model_validate(raw_user, by_name=True) for raw_user in raw_users]

    def create_user(self, *, user: User) -> None:
        data = {**user.model_dump(exclude=["id"]), "id": str(user.id)}
        self._repository.insert_one(data)


def make_user_service() -> UserServicePort:
    return UserService()
