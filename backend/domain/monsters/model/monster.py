from pydantic import BaseModel, Field


class Monster(BaseModel):
    name: str
    metadata_id: str = Field(alias="metadata id")
