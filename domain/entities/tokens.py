import datetime
from uuid import UUID
from pydantic import BaseModel

from domain.common.role_enum import RoleEnum


class TokenResponseEntity(BaseModel):
    access_token: str
    
    
class TokenEntity(BaseModel):
    id: UUID
    name: str
    email: str
    role: RoleEnum
    exp: datetime.datetime