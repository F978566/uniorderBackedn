from domain.entities.branch_office import BranchOfficeDBEntity
from domain.common.entities.entity import Entity


class RestaurantDBEntity(Entity):
    name: str
    email: str
    tin: int
    image_url: str
    icon_url: str
    hash_password: str


class RestaurantRequestEntity(Entity):
    name: str
    email: str
    tin: int
    password: str


class RestaurantWithBranchesEntity(Entity):
    name: str
    email: str
    tin: int
    password: str
    branche_offices: list[BranchOfficeDBEntity]