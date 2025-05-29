from abc import abstractmethod
from typing import List, Protocol
from uuid import UUID

from domain.entities.branch_office import (
    BranchOfficeDBEntity,
    BranchOfficeRequestEntity,
)
from domain.entities.restaurant import RestaurantDBEntity


class BranchOfficeRepository(Protocol):
    @abstractmethod
    async def create_branch_office(
        self,
        new_branch_office: BranchOfficeDBEntity,
        restaurant: RestaurantDBEntity,
    ) -> BranchOfficeDBEntity: ...

    @abstractmethod
    async def get_all_branches_by_restaurant_id(
        self,
        restaurant_id: UUID,
    ) -> List[BranchOfficeDBEntity]: ...

    @abstractmethod
    async def get_branch_office(
        self,
        branch_office_id: UUID,
    ) -> BranchOfficeDBEntity: ...

    @abstractmethod
    async def delete_branch_office(
        self,
        branch_office_id: UUID,
        restaurant_id: UUID,
    ) -> bool: ...
