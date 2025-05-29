from typing import List
from uuid import UUID

from domain.common.entities.entity import Entity
from domain.entities.menu import MenuItemDBEntity


class OrderItemRequestEntity(Entity):
    quantity: int
    menu_item_id: UUID
    

class OrderItemDBEntity(Entity):
    quantity: int
    menu_item: MenuItemDBEntity


class OrderRequestEntity(Entity):
    # customer_id: UUID
    restaurant_tin: int
    branch_office_id: UUID
    total_price: float
    # is_ready: bool
    # is_payed: bool
    order_items: List[OrderItemRequestEntity]


class OrderDBEntity(Entity):
    customer_id: UUID
    order_number: UUID
    is_ready: bool
    is_payed: bool
    order_items: List[OrderItemDBEntity]


class OrderEnrichedDBEntity(Entity):
    order_items: List[OrderItemDBEntity]
    restaurant_name: str
    branch_office_address: str
    is_ready: bool
    is_payed: bool
    order_number: int
    total_price: float
    customer_email: str