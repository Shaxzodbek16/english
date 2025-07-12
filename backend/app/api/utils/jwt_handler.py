from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.models.user import User
from app.core.databases.postgres import get_general_session
from app.core.settings import Settings, get_settings

settings: Settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/")
UTC = ZoneInfo("UTC")


class JWTHandler:
    def __init__(self) -> None:
        self.__settings: Settings = get_settings()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def _sanitize_payload(data: dict) -> dict:
        return {
            key: (value.isoformat() if isinstance(value, datetime) else value)
            for key, value in data.items()
        }

    def _create_token(self, data: dict, expires_delta: timedelta) -> str:
        expire = datetime.now(UTC) + expires_delta
        payload = self._sanitize_payload(data)
        payload["exp"] = int(expire.timestamp())
        return jwt.encode(
            payload, self.__settings.SECRET_KEY, algorithm=self.__settings.ALGORITHM
        )

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        return self._create_token(
            data,
            expires_delta
            or timedelta(minutes=self.__settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    def create_refresh_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        return self._create_token(
            data,
            expires_delta or timedelta(days=self.__settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.__settings.SECRET_KEY,
                algorithms=[self.__settings.ALGORITHM],
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def get_user_from_token(self, token: str, session: AsyncSession) -> User:
        payload = self.decode_token(token)
        phone_number = payload.get("phone_number") or None

        if phone_number:
            result = await session.execute(
                select(User).where(User.phone_number == phone_number)
            )
            user = result.scalar_one_or_none()
            if user:
                return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_general_session),
) -> User:
    with JWTHandler() as jwt_handler:
        return await jwt_handler.get_user_from_token(token, session)
