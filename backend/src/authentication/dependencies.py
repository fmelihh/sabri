from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from database.user import get_user
from .token import decode_access_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def oauth_v2_dependency(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token=token)
    if payload is None:
        raise credentials_exception

    user = await get_user(email=payload.sub)
    if user is None:
        raise credentials_exception

    if user.is_banned is True:
        raise HTTPException(status_code=400, detail="inactive user")

    return user
