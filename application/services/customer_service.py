from http.client import HTTPException
from fastapi import status
from passlib.context import CryptContext

from application.repositories.customer_repository import CustomerRepository
from application.services.toke_service import TokenService
from domain.entities.customer_profile import (
    CustomerProfileDBEntity,
    CustomerProfileEntity,
    CustomerProfileRequestEntity,
)


class CustomerService:
    def __init__(
        self,
        token_service: TokenService,
        customer_repository: CustomerRepository,
        pwd_context: CryptContext,
    ):
        self.token_service = token_service
        self.customer_repository = customer_repository
        self.pwd_context = pwd_context

    async def get_current_customer(self, token: str) -> CustomerProfileEntity:
        customer = await self.customer_repository.get_customer_by_id(self.token_service.decode_token(token).id)

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return customer

    async def create_customer(self, new_customer: CustomerProfileRequestEntity) -> CustomerProfileEntity:
        new_bd_customer = CustomerProfileDBEntity(
            id=new_customer.id,
            name=new_customer.name,
            role=new_customer.role,
            surname=new_customer.surname,
            patronymic=new_customer.patronymic,
            email=new_customer.email,
            hash_password=self.pwd_context.hash(new_customer.password),
        )
        return await self.customer_repository.create_customer(new_bd_customer)
