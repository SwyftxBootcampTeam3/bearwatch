from typing import List
from fastapi import APIRouter, Depends, Body, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr  # JWT


# dependencies
from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_user

# models
from app.models.token import AccessToken
from app.models.user import UserCreate, User

# repositories
from app.db.repositories.users import UsersRepository

# services
from app.services.authentication import AuthService

router = APIRouter()


@router.get("/me", response_model=User, name="users:get-user")
async def get_user(
    current_user: User = Depends(get_current_user),
) -> User:
    '''
    Fetch the user from a given JWT
    '''

    return current_user


@router.post(
    "/",
    response_model=AccessToken,
    name="users:create-user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: UserCreate = Body(..., embed=True),  # we pass in body of json
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    auth_service: AuthService = Depends(AuthService)
) -> AccessToken:
    """
    Creates a new user and returns their JWTs
    """

    # register user (send UserCreate to db, receive UserInDB)
    created_user = await user_repo.create_user(new_user=request)

    # create JWT
    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(
            user=created_user),
        token_type="bearer"
    )
    return access_token


@router.post(
    "/login/", response_model=AccessToken, name="users:login-email"
)
async def login_user_with_email(
    email: EmailStr,
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    auth_service: AuthService = Depends(AuthService)
) -> AccessToken:
    """
    Takes supplied email, passes this to repo to authenticate.
    Then generates and returns an access token for that user.
    """
    user = await user_repo.authenticate_user(
        email=email
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=user),
        token_type="bearer"
    )

    return access_token
