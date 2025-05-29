from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLAlchemyUUID
from sqlalchemy.orm import Mapped, mapped_column

# from infrastructure.db.models.restaurant_order_association import restaurant_order_association_table 
from infrastructure.db.models.base import Base


class CuisineModel(Base):
    __tablename__ = "cuisine_table"

    id: Mapped[UUID] = mapped_column(SQLAlchemyUUID, primary_key=True, default=uuid4)
    name: Mapped[str]
