import json
from uuid import UUID
from fastapi import APIRouter, Body, Depends, File, UploadFile
from dishka.integrations.fastapi import FromDishka, inject

from application.services.menu_service import MenuService
from domain.entities.menu import MenuItemRequestEntity
from .base import oauth2_scheme


menu_router = APIRouter(prefix="/menu", tags=["menu"])



@menu_router.get("/menu")
@inject
async def get_menu_by_restaurant_tin(
    menu_service: FromDishka[MenuService],
    restaurant_tin: int,
):
    print(restaurant_tin, " restaurant_tin")
    res = await menu_service.get_menu_with_items_by_restaurant_tin(restaurant_tin)
    return res


@menu_router.post("/menu-item")
@inject
async def create_menu_item(
    menu_service: FromDishka[MenuService],
    menu_item: str = Body(
        ...,
        example={
            "name": "tea",
            "price": "150",
            "currency": "RUB",
        },
    ),
    token: str = Depends(oauth2_scheme),
    image: UploadFile = File(...),
):
    image = await image.read()
    new_menu_item = MenuItemRequestEntity(**json.loads(menu_item))
    return await menu_service.create_menu_item_by_restaurant_token(token, new_menu_item, image)


@menu_router.delete("/menu-item/{menu_item_id}")
@inject
async def delete_menu_item(
    menu_service: FromDishka[MenuService],
    menu_item_id: UUID,
    token: str = Depends(oauth2_scheme),
) -> bool:
    return (await menu_service.delete_menu_item(menu_item_id))