from typing import Optional

# fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# app
from app.core.config import SECRET_KEY, API_PREFIX

# models
from app.models.user import User

# database
from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository

# auth
from app.services.authentication import AuthService
from app.models.token import AccessToken


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{API_PREFIX}/users/login/token/")
# OAuth2PasswordBearer is a class we import from FastAPI that we can instantiate by passing it the path that our users will send their email and password to so that they can authenticate. This class simply informs FastAPI that the URL provided is the one used to get a token. That information is used in OpenAPI and in FastAPI's interactive docs.


async def get_user_from_token(
    *,
    token: str = Depends(oauth2_scheme),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    auth_service: AuthService = Depends(AuthService)
) -> Optional[User]:
    """
    Takes a supplied token attempts to get the user that matches the 'username' (email) credential within it.
    """

    try:
        user_email = auth_service.get_username_from_token(
            token=token, secret_key=str(SECRET_KEY)
        )
        userindb = await user_repo.get_user_by_email(email=user_email)
    except Exception as e:  # httpexceptions
        raise e

    # access_token = AccessToken(
    #     access_token=token,
    #     token_type="bearer"
    # )

    # return userindb.copy(update={"access_token": access_token})
    return userindb


def get_current_user(
    current_user: User = Depends(get_user_from_token),
) -> Optional[User]:
    """
    A primarily routing dependency to get the current user in access token. Depends on get_user_from_token().
    We need an access_token.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # permissions
    # if not current_user[permissions]

    return current_user
