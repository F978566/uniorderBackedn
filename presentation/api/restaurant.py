from typing import List
from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka, inject
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from .base import oauth2_scheme
from application.services.restaurant_service import RestaurantService
from domain.entities.restaurant import RestaurantDBEntity


restaurant_router = APIRouter(prefix="/restaurant", tags=["restaurant"])


class GetRestaurantResponse(BaseModel):
    email: str


@restaurant_router.get("/all_restaurant")
@inject
async def all_restaurant(
    restaurant_service: FromDishka[RestaurantService],
) -> List[RestaurantDBEntity]:
    return await restaurant_service.get_all_restaurants()


@restaurant_router.get("/restaurant")
@inject
async def get_restaurant(
    email: GetRestaurantResponse,
    restaurant_service: FromDishka[RestaurantService],
) -> RestaurantDBEntity:
    return await restaurant_service.get_restaurant_by_email(email.email)
