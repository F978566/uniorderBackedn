from passlib.context import CryptContext
from fastapi import status, HTTPException

from application.repositories.user_repository import UserRepository
from domain.common.role_enum import RoleEnum
from domain.entities.user import UserEntity


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        pwd_context: CryptContext,
    ):
        self.user_repository = user_repository
        self.pwd_context = pwd_context

    async def authenticate_user(
        self,
        email: str,
        password: str,
        role: RoleEnum,
    ) -> UserEntity | None:
        user = await self.user_repository.get_user_by_email(email, role)

        if (user is None) or (not self.pwd_context.verify(password, user.hash_password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return UserEntity(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
        )