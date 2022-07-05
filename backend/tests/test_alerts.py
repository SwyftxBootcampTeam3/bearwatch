from h11 import Data
import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database


# db repositories
from app.db.repositories.alerts import AlertsRepository

# models
from app.models.alert import Alert, AlertCreate, AlertUpdate
# Import authentication service
from app.services.authentication import AuthService

# decorates all tests with this mark ( @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio

class TestAlertRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        # repeat for all other endpoints
        res = await client.post(app.url_path_for("alerts:get-user-alerts"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

        res = await client.post(app.url_path_for("alerts:create-alert"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

        res = await client.post(app.url_path_for("alerts:update-alert"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

        res = await client.post(app.url_path_for("alerts:delete-alert"))
        assert res.status_code != status.HTTP_404_NOT_FOUND

    async def test_require_auth(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("alerts:create-alert"), json={})
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

        res = await client.post(app.url_path_for("alerts:delete-alert"), json={})
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

        res = await client.post(app.url_path_for("alerts:update-alert"), json={})
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

        res = await client.post(app.url_path_for("alerts:get-user-alerts"))
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

class TestAuthentication:
    # TODO: Fix to include authentication
    async def test_invalid_input_fails(self, app: FastAPI, client: AsyncClient, db: Database ) -> None:
        res = await client.post(app.url_path_for("alerts:create-alert"), json={})
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        res = await client.post(app.url_path_for("alerts:delete-alert"), json={})
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        res = await client.post(app.url_path_for("alerts:update-alert"), json={})
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_use_auth_token(self, app: FastAPI, client: AsyncClient) -> None:
        """
        Checks whether an auth token (bearer) is correctly generated and view alerts
        """
        pass

    async def test_incorrect_token(self, app: FastAPI, client: AsyncClient) -> None:
        """
        Ensures that a valid token is used and matches to the correct user. 
        """
        pass

class TestCreateAlert:
    async def test_invalid_alert(self, app: FastAPI, client: AsyncClient, db: Database) -> None:
        """
        "Idiot proof" test - alerts are valid if:
            - alert price is lower than current price for decrease alert
            - alert price is higher than current price for increase alert
            - alert price is a floating point number
        """
        pass

    async def test_duplicate_alert(self, app: FastAPI, client: AsyncClient, db: Database) -> None:
        """
        Ensure that duplicate alerts are not created
        """
        pass

    async def test_retriggered_alert(self, app: FastAPI, client: AsyncClient, db: Database) -> None:
        """
        Checks that triggered alerts can be reset to re-trigger again
        """
        pass
    
class TestUpdateAlert:
    async def test_update_alert(self, app: FastAPI, client: AsyncClient, db: Database) -> None:
        """
        Ensure that updated alert meets the requirements for a valid alert (and updates)
        """
        pass

class TestDeleteAlert:
    async def test_update_alert(self, app: FastAPI, client: AsyncClient, db: Database) -> None:
        """
        Ensure that deleted alerts are placed 'in hibernations' and can be retriggered.
        """
        pass