from fastapi import Depends, status
from fastapi.security import SecurityScopes
from fastapi.exceptions import HTTPException

from models.user import User
from .oauth import OAuthSchema
from database.user import get_user
from .token import decode_access_token
from schemas.token import TokenPayloadSchema


async def token_dependency(token: str = Depends(OAuthSchema)) -> TokenPayloadSchema:
    payload = decode_access_token(token=token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


async def user_dependency(
    token_payload: TokenPayloadSchema = Depends(token_dependency),
):
    user = await get_user(email=token_payload.sub)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_banned is True:
        raise HTTPException(status_code=400, detail="inactive user")

    return user


async def permission(
    scopes: SecurityScopes, user: User = Depends(user_dependency)
) -> User:
    for scope in scopes.scopes:
        if scope not in user.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions.",
                headers={"WWW-Authenticate": f"Bearer scope= {scopes.scope_str}"},
            )

    return user
