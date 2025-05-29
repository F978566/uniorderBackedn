from uuid import UUID

from application.repositories.menu_repository import MenuRepository
from application.repositories.restaurant_repository import RestaurantRepository
from application.services.image_service import ImageService
from application.services.toke_service import TokenService
from domain.entities.menu import MenuDBEntity, MenuItemDBEntity, MenuItemRequestEntity


class MenuService:
    def __init__(
        self,
        menu_repository: MenuRepository,
        image_service: ImageService,
        restaurant_repository: RestaurantRepository,
        token_service: TokenService,
    ):
        self.menu_repository = menu_repository
        self.restaurant_repository = restaurant_repository
        self.image_service = image_service
        self.token_service = token_service
        
    async def get_menu_with_items_by_restaurant_tin(self, restaurant_tin: int) -> MenuDBEntity:
        menu = await self.menu_repository.get_menu_with_items_by_restaurant_tin(restaurant_tin)
        
        if menu is None:
            return None
        
        for x in menu.menu_items:
            x.image_url = "/files/" + x.image_url + ".png"
            
        return menu
    
    async def create_menu_item_by_restaurant_token(
        self,
        restaurant_access_token: str,
        menu_item: MenuItemRequestEntity,
        menu_image: bytes,
    ):
        restaurant_id = self.token_service.decode_token(restaurant_access_token).id

        image_url = await self.image_service.upload_image(
            f"menu_item_image_{restaurant_id}_{menu_item.name}_{menu_item.price}",
            menu_image,
        )

        if image_url is None:
            return
        
        new_menu_item = MenuItemDBEntity(
            name=menu_item.name,
            image_url=image_url,
            price=menu_item.price,
            currency=menu_item.currency,
        )
        
        return await self.menu_repository.create_menu_item(restaurant_id, new_menu_item)
    
    async def delete_menu_item(self, menu_item_id: UUID):
        return await self.menu_repository.delete_menu_item(menu_item_id)