from pydantic import BaseModel
from domain.common.entities.entity import Entity
from domain.common.role_enum import RoleEnum


class UserEntity(Entity):
    name: str
    email: str
    role: RoleEnum


class UserDBEntity(UserEntity):
    hash_password: str


class UserRequestEntity(UserEntity):
    password: str
