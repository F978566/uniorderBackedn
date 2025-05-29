from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from dishka.integrations.fastapi import FromDishka, inject

from application.repositories.order_repository import OrderRepository
from application.services.order_service import OrderService
from domain.entities.order import OrderEnrichedDBEntity, OrderRequestEntity
from .base import oauth2_scheme


order_router = APIRouter(prefix="/order", tags=["order"])


@order_router.post("/order")
@inject
async def create_order(
    order_service: FromDishka[OrderService],
    order: OrderRequestEntity,
    token: str = Depends(oauth2_scheme),
) -> bool:
    return await order_service.create_cash_order(order, token)


@order_router.get("/order")
@inject
async def get_enriched_user_order(
    order_service: FromDishka[OrderService],
    token: str = Depends(oauth2_scheme),
) -> List[OrderEnrichedDBEntity] | None:
    res = await order_service.get_enriched_user_orders(token)
    return res


@order_router.get("/order/branch-office-order")
@inject
async def get_enriched_branch_office_order(
    order_service: FromDishka[OrderService],
    branch_office_id: UUID,
    token: str = Depends(oauth2_scheme),
) -> List[OrderEnrichedDBEntity]:
    return await order_service.get_enriched_branch_orders(token, branch_office_id)


@order_router.patch("/order/pay/{order_id}")
@inject
async def pay_order(
    order_repo: FromDishka[OrderRepository],
    order_id: UUID,
) -> bool:
    return await order_repo.pay_order(order_id)


@order_router.patch("/order/ready/{order_id}")
@inject
async def set_order_ready(
    order_repo: FromDishka[OrderRepository],
    order_id: UUID,
) -> bool:
    return await order_repo.order_ready(order_id)
