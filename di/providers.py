from dishka import FromDishka, Provider, Scope, make_async_container, provide
from typing import AsyncIterator
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from application.repositories.branch_office_repository import BranchOfficeRepository
from application.repositories.customer_repository import CustomerRepository
from application.repositories.menu_repository import MenuRepository
from application.repositories.order_repository import OrderRepository
from application.repositories.restaurant_repository import RestaurantRepository
from application.repositories.user_repository import UserRepository
from application.services.auth_service import AuthService
from application.services.branch_office_service import BranchOfficeService
from application.services.customer_service import CustomerService
from application.services.image_service import ImageService
from application.services.menu_service import MenuService
from application.services.order_service import OrderService
from application.services.restaurant_service import RestaurantService
from application.services.toke_service import TokenService
from infrastructure.db.repositories.branch_office_repository_impl import (
    BranchOfficeRepositoryImpl,
)
from infrastructure.db.repositories.customer_repository_impl import (
    CustomerRepositoryImpl,
)
from infrastructure.db.repositories.menu_repository_impl import MenuRepositoryImpl
from infrastructure.db.repositories.order_repository_impl import OrderRepositoryImpl
from infrastructure.db.repositories.restaurant_repository_impl import (
    RestaurantRepositoryImpl,
)
from infrastructure.db.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.base import async_session_factory


class AppProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_db(self) -> AsyncIterator[AsyncSession]:
        async with async_session_factory() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_crypt_context(self) -> CryptContext:
        return CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    @provide(scope=Scope.REQUEST)
    def get_user_repo(self, session: FromDishka[AsyncSession]) -> UserRepository:
        return UserRepositoryImpl(session)

    @provide(scope=Scope.REQUEST)
    def get_auth_service(
        self,
        user_repository: FromDishka[UserRepository],
        pwd_context: FromDishka[CryptContext],
    ) -> AuthService:
        return AuthService(user_repository, pwd_context)

    @provide(scope=Scope.REQUEST)
    def get_token_service(
        self,
    ) -> TokenService:
        return TokenService()

    @provide(scope=Scope.REQUEST)
    def get_customer_repo(
        self, session: FromDishka[AsyncSession]
    ) -> CustomerRepository:
        return CustomerRepositoryImpl(session)

    @provide(scope=Scope.REQUEST)
    def get_customer_service(
        self,
        customer_repository: FromDishka[CustomerRepository],
        pwd_context: FromDishka[CryptContext],
        token_service: FromDishka[TokenService],
    ) -> CustomerService:
        return CustomerService(token_service, customer_repository, pwd_context)

    @provide(scope=Scope.REQUEST)
    def get_restaurant_repo(
        self,
        session: FromDishka[AsyncSession],
        menu_repository: FromDishka[MenuRepository],
    ) -> RestaurantRepository:
        return RestaurantRepositoryImpl(session, menu_repository)

    @provide(scope=Scope.REQUEST)
    def get_menu_repo(
        self,
        session: FromDishka[AsyncSession],
    ) -> MenuRepository:
        return MenuRepositoryImpl(session)

    @provide(scope=Scope.REQUEST)
    def get_order_repo(
        self,
        session: FromDishka[AsyncSession],
    ) -> OrderRepository:
        return OrderRepositoryImpl(session)

    @provide(scope=Scope.REQUEST)
    def get_image_service(
        self,
    ) -> ImageService:
        return ImageService()

    @provide(scope=Scope.REQUEST)
    def get_branch_office_repository(
        self,
        session: FromDishka[AsyncSession],
    ) -> BranchOfficeRepository:
        return BranchOfficeRepositoryImpl(session)

    @provide(scope=Scope.REQUEST)
    def get_restaurant_service(
        self,
        customer_repository: FromDishka[RestaurantRepository],
        pwd_context: FromDishka[CryptContext],
        image_service: FromDishka[ImageService],
        token_service: FromDishka[TokenService],
    ) -> RestaurantService:
        return RestaurantService(
            customer_repository, image_service, token_service, pwd_context
        )

    @provide(scope=Scope.REQUEST)
    def get_branch_office_service(
        self,
        branch_office_repository: FromDishka[BranchOfficeRepository],
        restaurant_repository: FromDishka[RestaurantRepository],
        token_service: FromDishka[TokenService],
        image_service: FromDishka[ImageService],
    ) -> BranchOfficeService:
        return BranchOfficeService(
            branch_office_repository,
            restaurant_repository,
            token_service,
            image_service,
        )

    @provide(scope=Scope.REQUEST)
    def get_menu_service(
        self,
        menu_repository: FromDishka[MenuRepository],
        restaurant_repository: FromDishka[RestaurantRepository],
        token_service: FromDishka[TokenService],
        image_service: FromDishka[ImageService],
    ) -> MenuService:
        return MenuService(
            menu_repository,
            image_service,
            restaurant_repository,
            token_service,
        )

    @provide(scope=Scope.REQUEST)
    def get_order_service(
        self,
        order_repository: FromDishka[OrderRepository],
        token_service: FromDishka[TokenService],
    ) -> OrderService:
        return OrderService(order_repository, token_service)


container = make_async_container(AppProvider())
