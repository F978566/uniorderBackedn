from typing import List
from uuid import UUID
from sqlalchemy import delete, exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from application.repositories.branch_office_repository import BranchOfficeRepository
from domain.entities.branch_office import (
    BranchOfficeDBEntity,
)
from domain.entities.restaurant import RestaurantDBEntity
from infrastructure.db.models.branch_office import BranchOfficeModel
from infrastructure.db.models.user import RestaurantProfileModel


class BranchOfficeRepositoryImpl(BranchOfficeRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_branch_office(
        self,
        new_branch_office: BranchOfficeDBEntity,
        restaurant: RestaurantDBEntity,
    ) -> BranchOfficeDBEntity:
        try:
            branch_office = BranchOfficeModel(
                address=new_branch_office.address,
                image_url=new_branch_office.image_url,
                restaurant_id=restaurant.id,
                longitude=new_branch_office.longitude,
                latitude=new_branch_office.latitude,
            )

            self._session.add(branch_office)
            await self._session.commit()
            await self._session.refresh(branch_office)
            return BranchOfficeDBEntity(
                id=branch_office.id,
                address=branch_office.address,
                image_url=branch_office.image_url,
                longitude=branch_office.longitude,
                latitude=branch_office.latitude,
            )
        except exc.IntegrityError:
            return None

    async def get_all_branches_by_restaurant_id(
        self,
        restaurant_id: UUID,
    ) -> List[BranchOfficeDBEntity]:
        try:
            branch_office = (
                await self._session.scalars(
                    select(BranchOfficeModel).where(
                        BranchOfficeModel.restaurant_id == restaurant_id
                    )
                )
            ).all()

            return list(
                map(
                    lambda x: BranchOfficeDBEntity(
                        id=x.id,
                        address=x.address,
                        image_url=x.image_url,
                        longitude=x.longitude,
                        latitude=x.latitude,
                    ),
                    branch_office,
                )
            )
        except exc.IntegrityError:
            return None

    async def get_branch_office(self, branch_office_id: UUID) -> BranchOfficeDBEntity:
        try:
            branch_office = await self._session.scalar(
                select(BranchOfficeModel).where(
                    BranchOfficeModel.id == branch_office_id
                )
            )

            return BranchOfficeDBEntity(
                id=branch_office.id,
                address=branch_office.address,
                image_url=branch_office.image_url,
                longitude=branch_office.longitude,
                latitude=branch_office.latitude,
            )
        except exc.IntegrityError:
            return None

    async def delete_branch_office(
        self,
        branch_office_id: UUID,
        restaurant_id: UUID,
    ) -> bool:
        try:
            await self._session.execute(
                delete(BranchOfficeModel)
                .where(
                    BranchOfficeModel.id == branch_office_id,
                    BranchOfficeModel.restaurant_id == restaurant_id,
                )
            )

            await self._session.commit()

            return True
        except exc.IntegrityError:
            return False
