from typing import List
from uuid import uuid4, UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import UUID as SQLAlchemyUUID

from infrastructure.db.models.base import Base
from infrastructure.db.models.menu_item import MenuItemModel


class MenuModel(Base):
    __tablename__ = "menu_table"
    
    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    
    restaurant_id: Mapped[UUID] = mapped_column(ForeignKey("restaurant_table.id", ondelete="CASCADE"))
    restaurant: Mapped["RestaurantProfileModel"] = relationship(back_populates="menu")  # type: ignore # noqa
    
    menu_items: Mapped[List["MenuItemModel"]] = relationship(back_populates="menu")