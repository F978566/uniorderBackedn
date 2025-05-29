from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from domain.common.role_enum import RoleEnum
from domain.entities.user import UserDBEntity


class UserRepository(Protocol):
    @abstractmethod
    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> UserDBEntity | None: ...
    
    @abstractmethod
    async def get_user_by_email(
        self,
        email: str,
        role: RoleEnum,
    ) -> UserDBEntity | None: ...

    @abstractmethod
    async def get_all_users(
        self,
    ) -> list[UserDBEntity]: ...
