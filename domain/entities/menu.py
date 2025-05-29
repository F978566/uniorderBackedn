from domain.common.entities.entity import Entity


class MenuItemDBEntity(Entity):
    name: str
    # cuisines: list[CuisineEntity]
    image_url: str
    price: float
    currency: str
    

class MenuItemRequestEntity(Entity):
    name: str
    price: float
    currency: str
    

class MenuDBEntity(Entity):
    menu_items: list[MenuItemDBEntity]
    restaurant_tin: int
    # cuisines: list[CuisineEntity]