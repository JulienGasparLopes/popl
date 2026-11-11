import uuid
from dataclasses import dataclass
from typing import Protocol

from domain.users.model.user import User


@dataclass
class UserFilters:
    id: set[uuid.UUID] | None = None
    google_id: set[str] | None = None


class UserServicePort(Protocol):
    def get_users(self, *, filters: UserFilters) -> list[User]: ...

    def create_user(self, *, user: User) -> None: ...
