from sqlalchemy import ForeignKey, String, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import UUID as SQLAlchemyUUID
from uuid import uuid4, UUID

from typing import List
from domain.common.role_enum import RoleEnum
from infrastructure.db.models.base import Base
from infrastructure.db.models.order import OrderModel


class UserModel(Base):
    __tablename__ = "user_table"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum))
    hashed_password: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)

    __mapper_args__ = {
        "polymorphic_identity": "user_table",
        "polymorphic_on": "type",
    }


class CustomerProfileModel(UserModel):
    __tablename__ = "customer_profile_table"

    id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"), primary_key=True, default=uuid4)
    surname: Mapped[str] = mapped_column(String)
    patronymic: Mapped[str] = mapped_column(String)
    orders: Mapped[List["OrderModel"]] = relationship(back_populates="customer")

    __mapper_args__ = {
        "polymorphic_identity": "customer_profile_table",
    }
    
class RestaurantProfileModel(UserModel):
    __tablename__ = "restaurant_table"

    id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"), primary_key=True, default=uuid4)
    image_url: Mapped[str]
    icon_url: Mapped[str]
    tin: Mapped[int] = mapped_column(Integer, unique=True)
    branch_offices: Mapped[List["BranchOfficeModel"]] = relationship(back_populates="restaurant")  # noqa: F821
    
    menu: Mapped["MenuModel"] = relationship(back_populates="restaurant", uselist=False)  # noqa: F821
    
    __mapper_args__ = {
        "polymorphic_identity": "restaurant_table",
    }