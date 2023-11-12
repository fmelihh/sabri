import os
import datetime
from jose import jwt, JWTError
from schemas.token import TokenPayloadSchema, TokenSchema


def create_access_token(payload: TokenPayloadSchema) -> TokenSchema:
    to_encode = payload.model_dump()
    expire_min = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    expire = datetime.datetime.now() + datetime.timedelta(minutes=expire_min)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.environ["SECRET_KEY"], algorithm=os.environ["ALGORITHM"]
    )
    return TokenSchema(access_token=encoded_jwt, expires_at=expire)


def decode_access_token(token: str) -> TokenPayloadSchema | None:
    try:
        if "Bearer" in token:
            token = token.strip("Bearer").strip()
        payload = jwt.decode(
            token, os.environ["SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]]
        )
        return TokenPayloadSchema(**payload)
    except JWTError:
        return None
