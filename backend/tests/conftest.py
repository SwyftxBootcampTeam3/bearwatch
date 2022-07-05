# here we can create and configure things that are common to tests

# we make fixtures for testing and then use them in our user/post/etc tests

# e.g.:

# we create common test_users with X privileges in the testing database
# we create a client using a test_user to make requests

import warnings
import os

from sqlalchemy import true

from app.core.config import JWT_TOKEN_PREFIX

from typing import List, Callable

# testing
import pytest

# Request + response
from httpx import AsyncClient  # emulates a client
from fastapi import FastAPI
from asgi_lifespan import LifespanManager

# Database
from databases import Database
import alembic
from alembic.config import Config

# Repositories
from app.db.repositories.users import UsersRepository
from app.db.repositories.alerts import AlertsRepository
from app.db.repositories.assets import AssetsRepository

# Models
from app.models.user import UserCreate, UserUpdate, User
from app.models.alert import AlertCreate, AlertUpdate, Alert
from app.models.asset import AssetCreate, Asset

# Services (auth)
from app.services.authentication import AuthService


# CORE: all tests need this
@pytest.fixture(scope="session")  # exists for duration of testing session
def apply_migrations():
    """
    Applies alembic migrations to the testing database prior to testing. Then downgrades applied migrations at end of testing session.
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"  # see app/core/config
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# CORE
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    """
    Creates and returns an app for use in tests.
    """
    from app.api.server import get_application

    return get_application()


# CORE
@pytest.fixture
def db(app: FastAPI) -> Database:
    """
    Uses the app's state to return the database. (testing db not live)
    """
    return app.state._db


# CORE
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    """
    Emulates a client (browser/mobileapp/etc) and sends to the application
    """
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testing",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


# USERS - creates a test_user that exists throughout life of testing
@pytest.fixture
async def test_user(db: Database) -> User:
    test_user = UserCreate(
        email="conf@test.com",
        phone_number = "1234567890",
    )

    user_repo = UsersRepository(db)

    # database persists for duration of the testing session
    existing_user = await user_repo.get_user_by_email(email=test_user.email)
    if existing_user:
        return existing_user
    # else

    return await user_repo.create_user(new_user=test_user)


# CORE - create an authorised client for test_user
@pytest.fixture
async def test_user_auth_client(
    client: AsyncClient, test_user: User
) -> AsyncClient:
    """
    Emulates a client with an authenticated user matching test_user. Used to test protected routes.
    """
    # create_access_token has default vars from app.config for all but user
    access_token = AuthService.create_access_token_for_user(user=test_user)

    # add additional auth headers to our client fixture
    client.headers = {
        **client.headers,
        "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
    }

    return client


# CORE - create an authorised client for ANY user
@pytest.fixture
def create_auth_client(client: AsyncClient) -> Callable:
    """
    Takes client (fixture defined already, not necessary to provide).
    Returns a callable function that takes UserInDB.
    Returns a client having Authorization headers with that user's token.
    e.g. authorized_client_with_this_user = create_auth_client(user=this_user)
    functionally we are injecting client into the function for when the user is provided.
    """

    def _create_authorised_client(*, user: User) -> AsyncClient:
        """
        see user_auth_client
        """
        # create_access_token has default vars from app.config for all but user
        access_token = AuthService.create_access_token_for_user(user=user)

        # add additional auth headers to our client fixture
        client.headers = {
            **client.headers,
            "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
        }

        return client

    return _create_authorised_client


# HELPER - create a user helper
async def helper_create_user(
    *, db: Database, new_user: UserCreate
) -> User:
    """
    Helper function that takes a UserCreate as input and creates that user/org
    """
    user_repo = UsersRepository(db)
    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user

    return await user_repo.create_user(new_user=new_user)


# USERS - creates test_user1 + 2 + 3
@pytest.fixture
async def test_user1(db: Database) -> User:
    new_user = UserCreate(email="testuser1@conf.test", phone_number="1111122222")
    return await helper_create_user(db=db, new_user=new_user)


@pytest.fixture
async def test_user2(db: Database) -> User:
    new_user = UserCreate(email="testuser2@conf.test", phone_number="1234512345")
    return await helper_create_user(db=db, new_user=new_user)


@pytest.fixture
async def test_user3(db: Database) -> User:
    new_user = UserCreate(email="testuser3@conf.test", phone_number="2345623456")
    return await helper_create_user(db=db, new_user=new_user)


# LIST of USERS / ORGS for easy access
@pytest.fixture
async def test_user_list(
    test_user1: User, test_user2: User, test_user3: User
) -> List[User]:
    return [test_user1, test_user2, test_user3]

# ALERTS - creates a test_alert belonging to test_user1
@pytest.fixture
async def org1_test_post(db: Database, test_user1: test_user1) -> Alert:
    """
    Alerts owned created by test_user1
    """
    # get repo's from db
    alerts_repo = AlertsRepository(db)

    # make a post with test_user1
    local_new_post = AlertCreate(
        asset_id=1,
        price=2.00,
        alert_type="true",
        user_id=1
    )

    # create post in repo
    created_post = await alerts_repo.create_alert(
        new_alert=local_new_post, current_user=test_user1
    )

    return created_post
