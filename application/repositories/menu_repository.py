from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from domain.entities.menu import MenuDBEntity, MenuItemDBEntity


class MenuRepository(Protocol):
    @abstractmethod
    async def create_menu(self, restaurant_tin: int) -> MenuDBEntity: ...

    @abstractmethod
    async def get_menu_with_items_by_restaurant_tin(self, tin: int) -> MenuDBEntity: ...

    @abstractmethod
    async def create_menu_item(
        self,
        restaurant_id: UUID,
        menu_item: MenuItemDBEntity,
    ) -> MenuDBEntity: ...

    @abstractmethod
    async def delete_menu_item(self, menu_item_id: UUID) -> bool: ...
