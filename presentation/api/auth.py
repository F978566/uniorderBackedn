import json
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Form
from pydantic import BaseModel

from application.repositories.user_repository import UserRepository
from application.services.auth_service import AuthService
from application.services.customer_service import CustomerService
from application.services.restaurant_service import RestaurantService
from application.services.toke_service import TokenService
from domain.common.role_enum import RoleEnum
from domain.entities.customer_profile import CustomerProfileRequestEntity
from domain.entities.restaurant import RestaurantRequestEntity
from domain.entities.tokens import TokenResponseEntity
from .base import oauth2_scheme


auth_router = APIRouter(prefix="/auth", tags=["auth"])


class CustomOAuth2PasswordRequestForm(BaseModel):
    email: str
    password: str
    role: RoleEnum


class UserRoleResponse(BaseModel):
    role: RoleEnum


async def custom_oauth2_form(
    email: str = Form(...),
    password: str = Form(...),
    role: RoleEnum = Form(...),
) -> CustomOAuth2PasswordRequestForm:
    return CustomOAuth2PasswordRequestForm(
        email=email,
        password=password,
        role=role.value,
    )


@auth_router.post("/token")
@inject
async def login_for_access_token_customer(
    auth_service: FromDishka[AuthService],
    token_service: FromDishka[TokenService],
    form_data: CustomOAuth2PasswordRequestForm = Depends(custom_oauth2_form),
):
    print(form_data.email, form_data.password, form_data.role)
    user = await auth_service.authenticate_user(
        form_data.email,
        form_data.password,
        form_data.role,
    )

    return TokenResponseEntity(
        access_token=token_service.create_access_token(user, user.role)
    )


@auth_router.post("/customer")
@inject
async def create_customer(
    new_customer: CustomerProfileRequestEntity,
    customer_service: FromDishka[CustomerService],
):
    # print(new_customer)
    return await customer_service.create_customer(new_customer)


@auth_router.get("/check-auth")
@inject
async def auth(
    token_service: FromDishka[TokenService],
    token: str = Depends(oauth2_scheme),
):
    if token_service.is_expired(token):
        raise HTTPException(status_code=401, detail="Token expired")


@auth_router.get("/customer")
@inject
async def get_customer(
    customer_service: FromDishka[CustomerService],
    token: str = Depends(oauth2_scheme),
):
    return await customer_service.get_current_customer(token)


# {"name": "My Restaurant", "email": "contact@restaurant.com", "tin": 123456789, "password": "securepassword"}


@auth_router.post("/restaurant")
@inject
async def create_restaurant(
    restaurant_service: FromDishka[RestaurantService],
    new_restaurant: str = Body(
        ...,
        description="JSON string representing a RestaurantRequestEntity",
        example={
            "name": "My Restaurant",
            "email": "contact@restaurant.com",
            "tin": 123456789,
            "password": "securepassword",
        },
    ),
    image: UploadFile = File(...),
    icon: UploadFile = File(...),
):
    new_restaurant = RestaurantRequestEntity(**json.loads(new_restaurant))
    read_image = await image.read()
    read_icon = await icon.read()
    return await restaurant_service.create_restaurant(
        new_restaurant, read_image, read_icon
    )


@auth_router.get("/all_users")
@inject
async def get_all_users(user_repo: FromDishka[UserRepository]):
    print(await user_repo.get_all_users())


@auth_router.get("/restaurant")
@inject
async def get_restaurant_by_token(
    restaurant_service: FromDishka[RestaurantService],
    token: str = Depends(oauth2_scheme),
):
    print(token)
    return await restaurant_service.get_current_restaurant(token)


@auth_router.get("/user-role")
@inject
async def get_user(
    token_service: FromDishka[TokenService],
    token: str = Depends(oauth2_scheme),
) -> UserRoleResponse:
    return UserRoleResponse(role=token_service.decode_token(token).role)
