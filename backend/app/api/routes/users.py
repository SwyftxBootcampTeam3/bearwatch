from typing import List
from fastapi import APIRouter, Depends, Body, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr  # JWT


# dependencies
from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_user

# models
from app.models.token import AccessToken
from app.models.user import UserCreate, User, UserPublic

# repositories
from app.db.repositories.users import UsersRepository

# services
from app.services.authentication import AuthService

router = APIRouter()

# name the route and you can use it across testing and db access


@router.get("/me", response_model=UserPublic, name="users:get-user")
async def get_user(
    current_user: User = Depends(get_current_user),
) -> UserPublic:

    return current_user


@router.post(
    "/",
    response_model=UserPublic,
    name="users:create-user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    new_user: UserCreate = Body(..., embed=True),  # we pass in body of json
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserPublic:
    """
    Creates a new user and returns a public model including access token (JWT)
    """

    # register user (send UserCreate to db, receive UserInDB)

    created_user = await user_repo.create_user(new_user=new_user)

    # create JWT and attach to UserPublic model

    access_token = AccessToken(
        access_token=AuthService.create_access_token_for_user(
            user=created_user),
        token_type="bearer"
    )

    # return a public model

    # profile attachment done in repository

    # return a public model
    return created_user.copy(update={"access_token": access_token})


@router.post(
    "/login/token/", response_model=AccessToken, name="users:login-email"
)
async def login_user_with_email(
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    email: EmailStr = Body(..., embed=True),
) -> AccessToken:
    """
    Takes supplied email, passes this to repo to authenticate.
    Then generates and returns an accesstoken for that user.
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
        access_token=AuthService.create_access_token_for_user(user=user),
        token_type="bearer"
    )

    return access_token
