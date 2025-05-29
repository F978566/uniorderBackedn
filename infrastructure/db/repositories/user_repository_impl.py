from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.repositories.user_repository import UserRepository
from domain.common.role_enum import RoleEnum
from domain.entities.user import UserDBEntity, UserEntity
from infrastructure.db.models.user import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> UserEntity | None:
        user = (
            await self._session.scalars(
                select(UserModel).where(UserModel.id == user_id)
            )
        ).one_or_none()

        if user is None:
            return None

        return UserDBEntity(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            hash_password=user.hashed_password,
        )
        
    async def get_user_by_email(
        self,
        email: str,
        role: RoleEnum,
    ) -> UserDBEntity | None:
        user = (
            await self._session.scalars(
                select(UserModel)
                .where(
                    UserModel.email == email,
                    UserModel.role == role,
                )
            )
        ).one_or_none()

        if user is None:
            return None

        return UserDBEntity(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            hash_password=user.hashed_password,
        )

    async def get_all_users(
        self,
    ) -> list[UserDBEntity]:
        users = (await self._session.scalars(select(UserModel))).all()
        return list(
            map(
                lambda user: UserDBEntity(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role=user.role,
                    hash_password=user.hashed_password,
                ),
                users,
            )
        )
