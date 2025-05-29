from sqlalchemy import UUID, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.repositories.menu_repository import MenuRepository
from domain.entities.menu import MenuDBEntity, MenuItemDBEntity
from infrastructure.db.models.menu import MenuModel
from infrastructure.db.models.menu_item import MenuItemModel
from infrastructure.db.models.user import RestaurantProfileModel


class MenuRepositoryImpl(MenuRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_menu(self, restaurant_tin: int) -> MenuDBEntity:
        try:
            restaurant = await self._session.scalar(
                select(RestaurantProfileModel).where(
                    RestaurantProfileModel.tin == restaurant_tin
                )
            )

            new_menu = MenuModel(restaurant=restaurant)
            self._session.add(new_menu)
            await self._session.commit()
            await self._session.refresh(new_menu)

            return MenuDBEntity(
                id=new_menu.id,
                menu_items=[],
                restaurant_tin=restaurant_tin,
            )

        except Exception:
            return None

    async def get_menu_with_items_by_restaurant_tin(self, tin: int) -> MenuDBEntity:
        try:
            res = await self._session.scalar(
                select(MenuModel)
                .join(
                    RestaurantProfileModel,
                    MenuModel.restaurant_id == RestaurantProfileModel.id,
                )
                .where(RestaurantProfileModel.tin == tin)
                .options(selectinload(MenuModel.menu_items))
                .options(selectinload(MenuModel.restaurant))
            )

            menu_items = [
                MenuItemDBEntity(
                    id=x.id,
                    name=x.name,
                    image_url=x.image_url,
                    price=x.price,
                    currency="RUB",
                )
                for x in res.menu_items
            ]

            return MenuDBEntity(
                id=res.id,
                menu_items=menu_items,
                restaurant_tin=res.restaurant.tin,
            )

        except Exception:
            return None

    async def create_menu_item(
        self, restaurant_id: UUID, menu_item: MenuItemDBEntity
    ) -> MenuDBEntity:
        try:
            menu = await self._session.scalar(
                select(MenuModel)
                .join(
                    RestaurantProfileModel,
                    MenuModel.restaurant_id == RestaurantProfileModel.id,
                )
                .where(RestaurantProfileModel.id == restaurant_id)
                .options(selectinload(MenuModel.menu_items))
            )

            new_menu_item = MenuItemModel(
                name=menu_item.name,
                image_url=menu_item.image_url,
                price=menu_item.price,
                currency="RUB",
                menu=menu,
            )

            self._session.add(new_menu_item)
            await self._session.commit()
            await self._session.refresh(new_menu_item)

            return menu_item

        except Exception:
            return None

    async def delete_menu_item(self, menu_item_id: UUID) -> bool:
        try:
            await self._session.execute(
                delete(MenuItemModel)
                .where(MenuItemModel.id == menu_item_id)
            )
            
            await self._session.commit()

            return True

        except Exception:
            return True