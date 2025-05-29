from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from domain.entities.customer_profile import (
    CustomerProfileDBEntity,
    CustomerProfileEntity,
)


class CustomerRepository(Protocol):
    @abstractmethod
    async def create_customer(
        self,
        customer: CustomerProfileDBEntity,
    ) -> CustomerProfileEntity: ...

    @abstractmethod
    async def get_customer_by_email(
        self,
        email: str,
    ) -> CustomerProfileEntity: ...

    @abstractmethod
    async def get_customer_by_id(
        self,
        user_id: UUID,
    ) -> CustomerProfileEntity: ...

    @abstractmethod
    async def delete_customer(self, user_id: UUID) -> bool: ...
