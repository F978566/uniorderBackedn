from sqlalchemy import select
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from application.repositories.customer_repository import CustomerRepository
from domain.common.role_enum import RoleEnum
from domain.entities.customer_profile import (
    CustomerProfileDBEntity,
    CustomerProfileEntity,
)
from infrastructure.db.models.user import CustomerProfileModel


class CustomerRepositoryImpl(CustomerRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_customer(
        self,
        customer: CustomerProfileDBEntity,
    ) -> CustomerProfileEntity:
        try:
            new_customer = CustomerProfileModel(
                name=customer.name,
                email=customer.email,
                role=RoleEnum.CUSTOMER,
                surname=customer.surname,
                patronymic=customer.patronymic,
                hashed_password=customer.hash_password,
            )
            self._session.add(new_customer)
            await self._session.commit()
            await self._session.refresh(new_customer)

            return CustomerProfileEntity(
                id=new_customer.id,
                name=new_customer.name,
                email=new_customer.email,
                surname=new_customer.surname,
                patronymic=new_customer.patronymic,
                role=new_customer.role,
            )
        except sqlalchemy.exc.IntegrityError:
            return None

    async def get_customer_by_email(
        self,
        email: str,
    ) -> CustomerProfileEntity:
        return (
            await self._session.scalars(
                select(CustomerProfileModel).where(CustomerProfileModel.email == email)
            )
        ).one()

    async def get_customer_by_id(
        self,
        user_id: UUID,
    ) -> CustomerProfileEntity:
        customer = (
            await self._session.scalars(
                select(CustomerProfileModel).where(CustomerProfileModel.id == user_id)
            )
        ).one()

        return CustomerProfileEntity(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            surname=customer.surname,
            patronymic=customer.patronymic,
            role=customer.role,
        )

    async def delete_customer(self, user_id: UUID) -> bool:
        customer = (
            await self._session.execute(
                select(CustomerProfileModel).filter(CustomerProfileModel.id == user_id)
            )
        ).one()
        
        if customer:
            await self._session.delete(customer)
            await self._session.commit()
            
            return True

        return False
