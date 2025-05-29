import json
from typing import List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, File, UploadFile
from dishka.integrations.fastapi import FromDishka, inject
from pydantic import BaseModel

from .base import oauth2_scheme
from application.services.branch_office_service import BranchOfficeService
from domain.entities.branch_office import BranchOfficeDBEntity, BranchOfficeRequestEntity


branch_office_router = APIRouter(prefix="/branch-office", tags=["branch-office"])


class GetBranchOfficeByTINRequest(BaseModel):
    tin: int


@branch_office_router.post("/branch-office")
@inject
async def create_branch_office(
    branch_office_service: FromDishka[BranchOfficeService],
    branch_office: str = Body(
        ...,
        example={
            "address": "Leninskiy",
        },
    ),
    token: str = Depends(oauth2_scheme),
    image: UploadFile = File(...),
):
    new_branch_office = BranchOfficeRequestEntity(**json.loads(branch_office))
    read_image = await image.read()
    print(new_branch_office)
    return await branch_office_service.create_branch_office(new_branch_office, token, read_image)


@branch_office_router.get("/branch-office")
@inject
async def get_branch_office_list_by_restaurant_tin(
    branch_office_service: FromDishka[BranchOfficeService],
    restaurant_tin: int,
) -> List[BranchOfficeDBEntity]:
    return await branch_office_service.get_branch_office_list_by_restaurant_tin(restaurant_tin)


@branch_office_router.get("/branch-office/{branch_id}")
@inject
async def get_restaurant_branch_office_by_id(
    branch_office_service: FromDishka[BranchOfficeService],
    branch_id: UUID,
) -> BranchOfficeDBEntity:
    return await branch_office_service.get_single_branch_office_by_id(branch_id)


@branch_office_router.delete("/branch-office/{branch_id}")
@inject
async def delete_restaurant_branch_office_by_id(
    branch_office_service: FromDishka[BranchOfficeService],
    branch_id: UUID,
    token: str = Depends(oauth2_scheme),
) -> bool:
    return await branch_office_service.delete_branch_office(branch_id, token)