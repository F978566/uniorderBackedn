from typing import List
from uuid import uuid4, UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import UUID as SQLAlchemyUUID

from infrastructure.db.models.base import Base


class MenuItemModel(Base):
    __tablename__ = "menu_item_table"
    
    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    name: Mapped[str]
    
    menu_id: Mapped[UUID] = mapped_column(ForeignKey("menu_table.id", ondelete="CASCADE"))
    menu: Mapped["MenuModel"] = relationship(back_populates="menu_items")  # type: ignore # noqa
    
    # order_item_id: Mapped[UUID] = mapped_column(ForeignKey("order_item_table.id"))
    order_items: Mapped[List["OrderItemModel"]] = relationship(back_populates="menu_item", foreign_keys="[OrderItemModel.menu_item_id]")  # type: ignore # noqa
    
    image_url: Mapped[str]
    price: Mapped[float]
    currency: Mapped[str]