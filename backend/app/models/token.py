from datetime import datetime, timedelta
from pydantic import EmailStr

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_AUDIENCE
from app.models.core import CoreModel


class JWTMeta(CoreModel):
    """
    mixin for JWT payload, holds JWT meta values (issuer/audience/times)
    """

    iss: str = "assistr.io"  # issuer
    aud: str = JWT_AUDIENCE  # audience
    iat: float = datetime.timestamp(datetime.utcnow())  # issued at
    exp: float = datetime.timestamp(
        datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )  # expires


class JWTCreds(CoreModel):
    """
    user credentials mixin for JWT payload, required to sign tokens for user
    email only
    """

    sub: EmailStr  # subcribed with


class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload before it's encoded - combines meta (issuer/audience/times) and user credentials together
    """

    # no additional attributes
    pass


class AccessToken(CoreModel):
    """
    token and token type.
    This is what we expect to receive with a request and provide on login.
    """

    access_token: str
    token_type: str  # as yet unused