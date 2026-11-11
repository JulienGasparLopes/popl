from pydantic import BaseModel


class Area(BaseModel):
    name: str
    id: str
