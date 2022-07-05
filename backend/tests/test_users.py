# core to testing
import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database


# db repositories
from app.db.repositories.users import UsersRepository

# models
from app.models.user import UserCreate, User, UserPublic

# Import authentication service
from app.services.authentication import AuthService

# decorates all tests with this mark ( @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio

# testing follows pretty common pattern:

# testroutes exist
# testroutes inputs fail correctly
# test actions with various client authorisations
# e.g. logged in, not logged in, allowed,not allowed -> get/create/delete/etc

class TestUserRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        # repeat for all other endpoints
        res = await client.post(app.url_path_for("users:create-user"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

        res = await client.post(app.url_path_for("users:get-user"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

        res = await client.post(app.url_path_for("users:login-email"))
        assert res.status_code != status.HTTP_404_NOT_FOUND


    async def test_invalid_input_fails(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("users:create-user"), json={})
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUserRegistration:
    async def test_valid_input_creates_user(
        self,
        app: FastAPI,  # see conftest
        client: AsyncClient,  # see conftest
        db: Database,  # see conftest
    ) -> None:
        # we want to access the database without routing
        user_repo = UsersRepository(db)

        # we will remove this out into conftest
        local_test_user = UserCreate(
            email="test@test.com",
            phone_number="1234512345"
        )

        # this query is not exposed publicly as a route
        user_in_db = await user_repo.get_user_by_email(email=local_test_user.email)

        # make sure they don't exist
        assert user_in_db is None

        # send post request to create and ensure is successful
        # create the json payload for the endpoint
        payload = {"new_user": local_test_user.dict()}

        # request the endpoint and get a response
        res = await client.post(app.url_path_for("users:create-user"), json=payload)

        # assert response is as expected
        assert res.status_code == status.HTTP_201_CREATED

        # ensure now exists in db
        user_in_db = await user_repo.get_user_by_email(email=local_test_user.email)
        assert user_in_db is not None
        assert user_in_db.email == local_test_user.email

        # assert returned json response is equal to user in database
        # tests if we modify it before we send it we don't modify anything incorrectly.

        # create two dicts of the values in the two models and compare dicts
        returned_user = UserPublic(**res.json()).dict(
            exclude={"profile", "access_token"}
            # profile and accesstoken not known prior to creation
        )
        assert returned_user == user_in_db.dict()
        # a UserPublic is the same as a UserInDB but with less values

    async def test_invalid_input_fails(
        self,
        app: FastAPI,  # see conftest
        client: AsyncClient,  # see conftest
        test_user: User,  # see conftest, this is a persisting test user
    ):

        assert test_user.email == "conf@test.com"
        assert test_user.phone_number == "1234567890"
        # test creating with existing email throws a 400

        payload = {
            "new_user": {"email": test_user.email}
        }
        res = await client.post(app.url_path_for("users:create-user"), json=payload)

        # we raise HTTPException in repository create:user
        assert res.status_code == status.HTTP_400_BAD_REQUEST
    