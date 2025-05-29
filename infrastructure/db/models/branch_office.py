from typing import List
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLAlchemyUUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.models.base import Base


class BranchOfficeModel(Base):
    __tablename__ = "branch_office_table"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    address: Mapped[str]
    image_url: Mapped[str]
    longitude: Mapped[float]
    latitude: Mapped[float]
    
    restaurant_id: Mapped[UUID] = mapped_column(ForeignKey("restaurant_table.id", ondelete="CASCADE"))
    restaurant: Mapped["RestaurantProfileModel"] = relationship(back_populates="branch_offices")  # type: ignore # noqa
    
    orders: Mapped[List["OrderModel"]] = relationship(back_populates="branch_office")  # type: ignore # noqa: F821
