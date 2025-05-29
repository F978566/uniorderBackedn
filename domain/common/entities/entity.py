from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Entity(BaseModel):
    id: UUID = Field(default_factory=lambda: str(uuid4()))