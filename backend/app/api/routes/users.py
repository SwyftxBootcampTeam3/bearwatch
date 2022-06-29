from typing import List
from fastapi import APIRouter, Depends, Body, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm  # JWT


# dependencies
from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_user

# models
from app.models.token import AccessToken
from app.models.user import UserCreate, User, UserPublic

# repositories
from app.db.repositories.users import UsersRepository

# services
from app.services import auth_service

router = APIRouter()

# name the route and you can use it across testing and db access
@router.get("/", response_model=List[UserPublic], name="users:list-all-users")
async def get_all_users(
    current_user: User = Depends(get_current_user),
) -> List[UserPublic]:

    users = [
        UserPublic(id="1", email="temp@temp.com", username="username1"),
        UserPublic(id="2", email="this@willbe.com", username="replaced"),
        current_user,
    ]
    return users


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
        access_token=auth_service.create_access_token_for_user(user=created_user),
        token_type="bearer",
        is_org = created_user.is_org,
    )

    # return a public model

    # profile attachment done in repository

    # return a public model
    return created_user.copy(update={"access_token": access_token})


@router.post(
    "/login/token/", response_model=AccessToken, name="users:login-email-password"
)
async def login_user_with_email_and_password(
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),  # db
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
) -> AccessToken:
    """
    Takes supplied form data containing 'username' and 'password' matching the OAuth2 standard, passes this to repo to authenticate exists and valid password.
    Then generates and returns an accesstoken for that user.
    """
    user = await user_repo.authenticate_user(
        email=form_data.username, password=form_data.password
    )

    if not user:
        # those values you provided are not authorised
        # specifically: auth was unsuccessful
        # you should be using the bearer auth scheme - an fyi incase
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # else
    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=user),
        token_type="bearer",
        is_org = user.is_org,
    )

    return access_token


@router.post(
    "/org",
    response_model=UserPublic,
    name="users:create-org",
    status_code=status.HTTP_201_CREATED,
)
async def create_org(
    new_user: UserCreate = Body(..., embed=True),  # we pass in body of json
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserPublic:
    """
    # CREATE AN ORG SHOULD NOT BE THIS EASY
    """

    # register user (send UserCreate to db, receive UserInDB)

    created_user = await user_repo.create_org(new_user=new_user)

    # create JWT and attach to UserPublic model

    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=created_user),
        token_type="bearer",
        is_org = created_user.is_org
    )

    # return a public model

    # profile attachment done in repository

    # return a public model
    return created_user.copy(update={"access_token": access_token})