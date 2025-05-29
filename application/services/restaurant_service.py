from fastapi import HTTPException, status
from passlib.context import CryptContext

from application.repositories.restaurant_repository import RestaurantRepository
from application.services.image_service import ImageService
from application.services.toke_service import TokenService
from domain.entities.restaurant import RestaurantDBEntity, RestaurantRequestEntity


class RestaurantService:
    def __init__(
        self,
        restaurant_respository: RestaurantRepository,
        image_service: ImageService,
        token_service: TokenService,
        pwd_context: CryptContext,
    ):
        self.image_service = image_service
        self.pwd_context = pwd_context
        self.restaurant_respository = restaurant_respository
        self.token_service = token_service

    async def create_restaurant(
        self,
        restaurant: RestaurantRequestEntity,
        image: bytes,
        icon: bytes,
    ):
        image_url = await self.image_service.upload_image(
            f"restaurant_image_{restaurant.name}_{restaurant.email}",
            image,
        )
        icon_url = await self.image_service.upload_image(
            f"restaurant_icon_{restaurant.name}_{restaurant.email}",
            icon,
        )

        if (image_url is None) or (icon_url is None):
            raise HTTPException(status_code=400, detail="Something wrong =(")

        new_restaurant = RestaurantDBEntity(
            name=restaurant.name,
            email=restaurant.email,
            tin=restaurant.tin,
            image_url=image_url,
            icon_url=icon_url,
            hash_password=self.pwd_context.hash(restaurant.password),
        )

        return await self.restaurant_respository.create_restaurant(new_restaurant)

    async def get_all_restaurants(self):
        res = await self.restaurant_respository.all_restaurants()
        
        for x in res:
            x.image_url = "/files/" + x.image_url + ".png"
            x.icon_url = "/files/" + x.icon_url + ".png"
        
        return res
    
    async def get_restaurant_by_email(self, email: str) -> RestaurantDBEntity:
        restaurant = await self.restaurant_respository.get_restaurant_by_email(email)
        
        restaurant.image_url = "/files/" + restaurant.image_url + ".png"
        restaurant.icon_url = "/files/" + restaurant.icon_url + ".png"
        
        return restaurant
    
    async def get_current_restaurant(self, token: str) -> RestaurantDBEntity:
        restaurant = await self.restaurant_respository.get_restaurant_by_id(self.token_service.decode_token(token).id)

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        restaurant.image_url = "/files/" + restaurant.image_url + ".png"
        restaurant.icon_url = "/files/" + restaurant.icon_url + ".png"

        return restaurant
    