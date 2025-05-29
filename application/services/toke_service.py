import os
from jose import JWTError, jwt
from fastapi import status, HTTPException

import datetime
from domain.entities.tokens import TokenEntity
from domain.entities.user import UserEntity, UserRequestEntity
from domain.common.role_enum import RoleEnum


class TokenService:
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 20
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 120

    def create_access_token(self, user: UserEntity, role: RoleEnum):
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        # expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": role.value,
            "exp": expire,
        }

        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return token

    def decode_token(self, token: str) -> TokenEntity:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("id") is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return TokenEntity(**payload)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def is_expired(self, token: str):
        return (self.decode_token(token).exp < datetime.datetime.now(datetime.timezone.utc)) or True