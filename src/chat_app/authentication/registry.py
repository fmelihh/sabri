from fastapi.exceptions import HTTPException

from ..database.user import get_user
from .token import create_access_token
from ..utils.hash import verify_password
from ..schemas.token import TokenPayloadSchema, TokenSchema


async def retrieve_jwt_access_token(email: str, password: str) -> TokenSchema:
    user = await get_user(email)
    if (not user) or (not verify_password(password, user.password)):
        raise HTTPException(
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
            detail="incorrect username or password",
        )
    token_payload = TokenPayloadSchema(sub=user.email)
    token_schema = create_access_token(payload=token_payload)
    return token_schema
