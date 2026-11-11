import uuid

from pydantic import BaseModel


class User(BaseModel):
    id: uuid.UUID
    pseudo: str

    email: str
    google_id: str
