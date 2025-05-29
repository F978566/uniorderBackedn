from typing import List

from sqlalchemy import UUID
from application.repositories.branch_office_repository import BranchOfficeRepository
from application.repositories.restaurant_repository import RestaurantRepository
from application.services.image_service import ImageService
from application.services.toke_service import TokenService
from domain.common.role_enum import RoleEnum
from domain.entities.branch_office import (
    BranchOfficeDBEntity,
    BranchOfficeRequestEntity,
)


class BranchOfficeService:
    def __init__(
        self,
        branch_office_repository: BranchOfficeRepository,
        restaurant_repository: RestaurantRepository,
        token_service: TokenService,
        image_service: ImageService,
    ):
        self.branch_office_repository = branch_office_repository
        self.restaurant_repository = restaurant_repository
        self.token_service = token_service
        self.image_service = image_service

    async def create_branch_office(
        self,
        branch_office: BranchOfficeRequestEntity,
        restaurant_access_token: str,
        branch_office_image: bytes,
    ) -> BranchOfficeDBEntity:
        image_url = await self.image_service.upload_image(
            f"branch_office_image_{branch_office.address}",
            branch_office_image,
        )

        restaurant = await self.restaurant_repository.get_restaurant_by_id(
            self.token_service.decode_token(restaurant_access_token).id
        )

        new_branch_office = BranchOfficeDBEntity(
            address=branch_office.address,
            image_url=image_url,
            longitude=branch_office.longitude,
            latitude=branch_office.latitude,
        )

        return await self.branch_office_repository.create_branch_office(
            new_branch_office,
            restaurant,
        )

    async def get_branch_office_list_by_restaurant_tin(
        self, restaurant_tin: str
    ) -> List[BranchOfficeDBEntity]:
        # restaurant = await self.restaurant_repository.get_restaurant_by_id()
        restaurant = await self.restaurant_repository.get_restaurant_by_tin(
            restaurant_tin
        )

        if restaurant is None:
            return []

        restaurant_id = restaurant.id

        res = await self.branch_office_repository.get_all_branches_by_restaurant_id(
            restaurant_id
        )

        for x in res:
            x.image_url = "/files/" + x.image_url + ".png"

        return res

    async def get_restaurant_branch_office_list_by_token(
        self, restaurant_access_token: str
    ) -> List[BranchOfficeDBEntity]:
        restaurant = await self.restaurant_repository.get_restaurant_by_id(
            self.token_service.decode_token(restaurant_access_token).id
        )

        res = await self.branch_office_repository.get_all_branches_by_restaurant_id(
            restaurant.id
        )

        for x in res:
            x.image_url = "/files/" + x.image_url + ".png"

        return res

    async def get_single_branch_office_by_id(
        self,
        branch_office_id: UUID,
    ) -> BranchOfficeDBEntity:
        res = await self.branch_office_repository.get_branch_office(branch_office_id)
        res.image_url = "/files/" + res.image_url + ".png"

        return res

    async def delete_branch_office(
        self,
        branch_office_id: UUID,
        restaurant_token: str,
    ) -> bool:
        decode_token = self.token_service.decode_token(restaurant_token)
        if decode_token.role == RoleEnum.CUSTOMER:
            return False

        res = await self.branch_office_repository.delete_branch_office(
            branch_office_id,
            decode_token.id,
        )

        return res
