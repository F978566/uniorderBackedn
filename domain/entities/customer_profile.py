from domain.common.role_enum import RoleEnum
from domain.entities.user import UserDBEntity, UserEntity, UserRequestEntity


class CustomerProfileEntity(UserEntity):
    surname: str
    patronymic: str
    # orders: list[OrderEntity] | None


class CustomerProfileDBEntity(CustomerProfileEntity, UserDBEntity): ...


class CustomerProfileRequestEntity(CustomerProfileEntity, UserRequestEntity): ...


class CreateCustomerProfile(CustomerProfileEntity, UserRequestEntity):
    name: str
    email: str
    role: RoleEnum
    surname: str
    patronymic: str
