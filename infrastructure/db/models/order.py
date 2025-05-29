import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.sql.sqltypes import UUID as SQLAlchemyUUID
from uuid import uuid4, UUID

from infrastructure.db.models.base import Base
from infrastructure.db.models.branch_office import BranchOfficeModel


class OrderModel(Base):
    __tablename__ = "order_table"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    order_number: Mapped[int]
    total_price: Mapped[float]
    is_ready: Mapped[bool]
    is_payed: Mapped[bool]
    created_on: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)

    customer_id: Mapped[UUID] = mapped_column(ForeignKey("customer_profile_table.id"))
    customer: Mapped["CustomerProfileModel"] = relationship(back_populates="orders")  # type: ignore # noqa
    
    branch_office_id: Mapped[UUID] = mapped_column(ForeignKey("branch_office_table.id", ondelete="CASCADE"))
    branch_office: Mapped["BranchOfficeModel"] = relationship(back_populates="orders")
    
    order_items: Mapped[List["OrderItemModel"]] = relationship(back_populates="order", foreign_keys="[OrderItemModel.order_id]")  # type: ignore # noqa