from typing import List
from uuid import UUID
from sqlalchemy import select, exc
from sqlalchemy.ext.asyncio import AsyncSession

from application.repositories.menu_repository import MenuRepository
from application.repositories.restaurant_repository import RestaurantRepository
from domain.common.role_enum import RoleEnum
from domain.entities.restaurant import RestaurantDBEntity
from infrastructure.db.models.user import RestaurantProfileModel


class RestaurantRepositoryImpl(RestaurantRepository):
    def __init__(
        self,
        session: AsyncSession,
        menu_repository: MenuRepository,
    ):
        self._session = session
        self.menu_repository = menu_repository

    async def create_restaurant(
        self, restaurant: RestaurantDBEntity
    ) -> RestaurantDBEntity:
        try:
            new_restaurant = RestaurantProfileModel(
                name=restaurant.name,
                email=restaurant.email,
                role=RoleEnum.RESTAURANT,
                hashed_password=restaurant.hash_password,
                image_url=restaurant.image_url,
                icon_url=restaurant.icon_url,
                tin=restaurant.tin,
            )
            
            self._session.add(new_restaurant)
            await self._session.commit()
            await self._session.refresh(new_restaurant)
            
            await self.menu_repository.create_menu(restaurant.tin)

            return new_restaurant
        except exc.IntegrityError:
            return None

    async def all_restaurants(self) -> List[RestaurantDBEntity]:
        try:
            res = (await self._session.scalars(select(RestaurantProfileModel))).all()

            return list(
                map(
                    lambda x: RestaurantDBEntity(
                        id=x.id,
                        name=x.name,
                        email=x.email,
                        tin=x.tin,
                        image_url=x.image_url,
                        icon_url=x.icon_url,
                        hash_password=x.hashed_password,
                    ),
                    res,
                )
            )

        except Exception:
            return None

    async def get_restaurant_by_email(self, email: str) -> RestaurantDBEntity:
        try:
            res = await self._session.scalar(
                select(RestaurantProfileModel).where(
                    RestaurantProfileModel.email == email
                )
            )

            return RestaurantDBEntity(
                id=res.id,
                name=res.name,
                email=res.email,
                tin=res.tin,
                image_url=res.image_url,
                icon_url=res.icon_url,
                hash_password=res.hashed_password,
            )

        except Exception:
            return None

    async def get_restaurant_by_id(self, id: UUID) -> RestaurantDBEntity:
        try:
            res = await self._session.scalar(
                select(RestaurantProfileModel).where(RestaurantProfileModel.id == id)
            )

            return RestaurantDBEntity(
                id=res.id,
                name=res.name,
                email=res.email,
                tin=res.tin,
                image_url=res.image_url,
                icon_url=res.icon_url,
                hash_password=res.hashed_password,
            )

        except Exception:
            return None

    async def get_restaurant_by_tin(self, tin: int) -> RestaurantDBEntity:
        try:
            res = await self._session.scalar(
                select(RestaurantProfileModel).where(RestaurantProfileModel.tin == tin)
            )

            return RestaurantDBEntity(
                id=res.id,
                name=res.name,
                email=res.email,
                tin=res.tin,
                image_url=res.image_url,
                icon_url=res.icon_url,
                hash_password=res.hashed_password,
            )

        except Exception:
            return None
