import uuid

from pydantic import BaseModel


class User(BaseModel):
    id: uuid.UUID

    email: str
    google_id: str
