from abc import abstractmethod
from typing import List, Protocol
from uuid import UUID

from domain.entities.order import (
    OrderDBEntity,
    OrderEnrichedDBEntity,
    OrderRequestEntity,
)


class OrderRepository(Protocol):
    @abstractmethod
    async def create_cash_order(
        self, order: OrderRequestEntity, customer_id: UUID
    ) -> bool: ...

    @abstractmethod
    async def pay_order(self, order_id: UUID) -> bool: ...

    @abstractmethod
    async def order_ready(self, order_id: UUID) -> bool: ...

    @abstractmethod
    async def get_enriched_customer_orders(
        self,
        customer_id: UUID,
    ) -> List[OrderEnrichedDBEntity]: ...

    @abstractmethod
    async def get_enriched_branch_office_orders(
        self,
        branch_office_id: UUID,
    ) -> List[OrderEnrichedDBEntity]: ...
