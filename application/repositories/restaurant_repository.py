from abc import abstractmethod
from typing import List
from uuid import UUID
from typing_extensions import Protocol

from domain.entities.restaurant import RestaurantDBEntity


class RestaurantRepository(Protocol):
    @abstractmethod
    async def create_restaurant(
        self,
        restaurant: RestaurantDBEntity,
    ) -> RestaurantDBEntity: ...

    @abstractmethod
    async def all_restaurants(self) -> List[RestaurantDBEntity]: ...

    @abstractmethod
    async def get_restaurant_by_email(self, email: str) -> RestaurantDBEntity: ...
    
    @abstractmethod
    async def get_restaurant_by_tin(self, tin: int) -> RestaurantDBEntity: ...

    @abstractmethod
    async def get_restaurant_by_id(self, id: UUID) -> RestaurantDBEntity: ...
