from pydantic import BaseModel
from domain.common.entities.entity import Entity


class BranchOfficeRequestEntity(BaseModel):
    address: str
    longitude: float
    latitude: float

class BranchOfficeDBEntity(Entity):
    address: str
    image_url: str
    longitude: float
    latitude: float
