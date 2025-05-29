from typing import List
from uuid import UUID
from sqlalchemy import and_, asc, desc, select, update
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.repositories.order_repository import OrderRepository
from domain.entities.menu import MenuItemDBEntity
from domain.entities.order import (
    OrderEnrichedDBEntity,
    OrderItemDBEntity,
    OrderRequestEntity,
)
from infrastructure.db.models.branch_office import BranchOfficeModel
from infrastructure.db.models.order import OrderModel
from infrastructure.db.models.order_item import OrderItemModel


class OrderRepositoryImpl(OrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_number(self, branch_office_id: UUID):
        try:
            min_order_number = await self._session.scalar(
                select(func.min(OrderModel.order_number)).where(
                    and_(
                        OrderModel.is_ready.is_(False),
                        OrderModel.is_payed.is_(False),
                        OrderModel.branch_office_id == branch_office_id,
                    )
                )
            )

            if min_order_number is None:
                return 1
            elif min_order_number == 1:
                max_order_number = await self._session.scalar(
                    select(func.max(OrderModel.order_number))
                )

                return max_order_number + 1
            else:
                return min_order_number - 1

        except Exception:
            return None

    async def create_cash_order(
        self,
        order: OrderRequestEntity,
        customer_id: UUID,
    ) -> bool:
        try:
            number = await self.get_number(order.branch_office_id)

            if number is None:
                raise Exception()

            new_order = OrderModel(
                customer_id=customer_id,
                order_number=number,
                is_ready=False,
                is_payed=False,
                branch_office_id=order.branch_office_id,
                total_price=order.total_price,
            )
            self._session.add(new_order)

            for order_item in order.order_items:
                order_item = OrderItemModel(
                    menu_item_id=order_item.menu_item_id,
                    quantity=order_item.quantity,
                    order=new_order,
                )

                self._session.add(order_item)

            self._session.add(new_order)
            await self._session.commit()
            await self._session.refresh(new_order)

            return True

        except Exception:
            return False

    async def pay_order(self, order_id: UUID) -> bool:
        try:
            await self._session.execute(
                update(OrderModel)
                .where(OrderModel.id == order_id)
                .values(is_payed=True)
            )

            await self._session.commit()

            return True

        except Exception:
            return False

    async def order_ready(self, order_id):
        try:
            await self._session.execute(
                update(OrderModel)
                .where(OrderModel.id == order_id)
                .values(is_ready=True)
            )

            await self._session.commit()

            return True

        except Exception:
            return False

    async def get_enriched_customer_orders(
        self,
        customer_id: UUID,
    ) -> List[OrderEnrichedDBEntity]:
        try:
            orders = (
                await self._session.scalars(
                    select(OrderModel)
                    .where(OrderModel.customer_id == customer_id)
                    .options(
                        selectinload(OrderModel.branch_office).joinedload(
                            BranchOfficeModel.restaurant
                        )
                    )
                    .options(
                        selectinload(OrderModel.order_items).joinedload(
                            OrderItemModel.menu_item
                        )
                    )
                    .options(selectinload(OrderModel.customer))
                    .order_by(desc(OrderModel.created_on), desc(OrderModel.id))
                )
            ).all()

            return list(
                map(
                    lambda order: OrderEnrichedDBEntity(
                        id=order.id,
                        order_items=list(
                            map(
                                lambda y: OrderItemDBEntity(
                                    id=y.id,
                                    quantity=y.quantity,
                                    menu_item=MenuItemDBEntity(
                                        id=y.menu_item.id,
                                        name=y.menu_item.name,
                                        image_url=y.menu_item.image_url,
                                        price=y.menu_item.price,
                                        currency=y.menu_item.currency,
                                    ),
                                ),
                                order.order_items,
                            )
                        ),
                        restaurant_name=order.branch_office.restaurant.name,
                        branch_office_address=order.branch_office.address,
                        is_ready=order.is_ready,
                        is_payed=order.is_payed,
                        order_number=order.order_number,
                        total_price=sum(
                            order_item.menu_item.price * order_item.quantity
                            for order_item in order.order_items
                        ),
                        customer_email=order.customer.email,
                    ),
                    orders,
                )
            )

        except Exception:
            return None

    async def get_enriched_branch_office_orders(
        self,
        branch_office_id: UUID,
    ) -> List[OrderEnrichedDBEntity]:
        try:
            orders = (
                await self._session.scalars(
                    select(OrderModel)
                    .where(
                        and_(
                            OrderModel.branch_office_id == branch_office_id,
                            OrderModel.is_payed.is_(False),
                        )
                    )
                    .options(
                        selectinload(OrderModel.branch_office).joinedload(
                            BranchOfficeModel.restaurant
                        )
                    )
                    .options(
                        selectinload(OrderModel.order_items).joinedload(
                            OrderItemModel.menu_item
                        )
                    )
                    .options(selectinload(OrderModel.customer))
                    .order_by(desc(OrderModel.id))
                )
            ).all()

            print(orders)

            return list(
                map(
                    lambda order: OrderEnrichedDBEntity(
                        id=order.id,
                        order_items=list(
                            map(
                                lambda y: OrderItemDBEntity(
                                    id=y.id,
                                    quantity=y.quantity,
                                    menu_item=MenuItemDBEntity(
                                        id=y.menu_item.id,
                                        name=y.menu_item.name,
                                        image_url=y.menu_item.image_url,
                                        price=y.menu_item.price,
                                        currency=y.menu_item.currency,
                                    ),
                                ),
                                order.order_items,
                            )
                        ),
                        restaurant_name=order.branch_office.restaurant.name,
                        branch_office_address=order.branch_office.address,
                        is_ready=order.is_ready,
                        is_payed=order.is_payed,
                        order_number=order.order_number,
                        total_price=sum(
                            order_item.menu_item.price * order_item.quantity
                            for order_item in order.order_items
                        ),
                        customer_email=order.customer.email,
                    ),
                    orders,
                )
            )
        except Exception:
            return None
