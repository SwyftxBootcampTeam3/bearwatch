from h11 import Data
import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database


# db repositories
from app.db.repositories.assets import AssetsRepository

# models
from app.models.asset import Asset, AssetCreate
# Import authentication service
from app.services.authentication import AuthService

# decorates all tests with this mark ( @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio

class TestAlertRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("assets:get-all-assets"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
