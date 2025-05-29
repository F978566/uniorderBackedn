from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.sql.sqltypes import UUID as SQLAlchemyUUID
from uuid import uuid4, UUID

from infrastructure.db.models.base import Base


class OrderItemModel(Base):
    __tablename__ = "order_item_table"
    
    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    quantity: Mapped[int]
    
    menu_item_id: Mapped[UUID] = mapped_column(ForeignKey("menu_item_table.id"))
    menu_item: Mapped["MenuItemModel"] = relationship(back_populates="order_items", foreign_keys="[OrderItemModel.menu_item_id]")  # type: ignore # noqa: F821

    order_id: Mapped[UUID] = mapped_column(ForeignKey("order_table.id", ondelete="CASCADE"))
    order: Mapped["OrderModel"] = relationship(back_populates="order_items", foreign_keys="[OrderItemModel.order_id]")  # type: ignore # noqa: F821
