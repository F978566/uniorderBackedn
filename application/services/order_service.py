from uuid import UUID
from application.repositories.order_repository import OrderRepository
from application.services.toke_service import TokenService
from domain.common.role_enum import RoleEnum
from domain.entities.order import OrderRequestEntity


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        token_service: TokenService,
    ):
        self.order_repository = order_repository
        self.token_service = token_service

    async def create_cash_order(self, order: OrderRequestEntity, token: str):
        decode_token = self.token_service.decode_token(token)

        if decode_token.role == RoleEnum.RESTAURANT:
            return

        return await self.order_repository.create_cash_order(order, decode_token.id)

    async def get_enriched_user_orders(self, token: str):
        decode_token = self.token_service.decode_token(token)

        if decode_token.role == RoleEnum.RESTAURANT:
            return

        orders = await self.order_repository.get_enriched_customer_orders(decode_token.id)
        
        if orders is None:
            return
        
        for order in orders:
            for order_item in order.order_items:
                order_item.menu_item.image_url = "/files/" + order_item.menu_item.image_url + ".png" 
            
        return orders

    async def get_enriched_branch_orders(self, token: str, branch_office_id: UUID):
        decode_token = self.token_service.decode_token(token)

        if decode_token.role == RoleEnum.CUSTOMER:
            return

        orders = await self.order_repository.get_enriched_branch_office_orders(branch_office_id)
        
        for order in orders:
            for order_item in order.order_items:
                order_item.menu_item.image_url = "/files/" + order_item.menu_item.image_url + ".png" 
            
        return orders