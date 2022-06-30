from typing import List, Optional
from databases import Database

# app
from pydantic import EmailStr
from fastapi import HTTPException, status

# repositories
from app.db.repositories.base import BaseRepository

# models
from app.models.asset import Asset, AssetCreate

GET_ALL_ASSETS_QUERY = """
    SELECT id, name, code, created_at, updated_at;
    FROM assets
"""

GET_ASSET_BY_ID = """
    SELECT id, name, code, created_at, updated_at;
    FROM assets
    WHERE id = :id;
"""

GET_ASSET_BY_CODE = """
    SELECT id, name, code, created_at, updated_at;
    FROM assets
    WHERE code = :code;
"""

CREATE_ASSET_QUERY = """
    INSERT INTO assets (name,code,last_price)
    VALUES (:name,:code,:last_price)
    RETURNING id, name, code, last_price, created_at, updated_at;
"""


class AssetsRepository(BaseRepository):
    """
    All database actions associated with Assets
    """

    # when we init we want to ensure that the auth service is available to the repository --> we're going to be doing auth things
    def __init__(self, db: Database) -> None:
        """
        Standard repository intialise
        """
        super().__init__(db)

    async def get_all_assets(self) -> List[Asset]:
        """
        Queries the database for all the current assets
        """

        # pass values to query
        assets = await self.db.fetch_all(
            query=GET_ALL_ASSETS_QUERY
        )

        # Map assets to asset model
        return map(lambda a: Asset(**a), assets)

    async def get_asset_by_id(self, *, id: str) -> Asset:
        """
        Queries the database for an asset with the matching id
        """

        # pass values to query
        asset = await self.db.fetch_one(
            query=GET_ASSET_BY_ID, values={"id": id}
        )

        if asset:
            asset = Asset(**asset)

        return asset

    async def get_asset_by_code(self, *, code: str) -> Asset:
        """
        Queries the database for the first matching asset with this code (this SHOULD be a unique field)
        """

        # pass values to query
        asset = await self.db.fetch_one(
            query=GET_ASSET_BY_CODE, values={"code": code}
        )

        if asset:
            asset = Asset(**asset)

        return asset

    async def create_asset(self, *, new_asset: AssetCreate) -> Asset:
        """
        Creates a asset.
        """

        # unique constraints exist on code, ensure no asset exists with this code
        existing_asset = await self.get_asset_by_code(code=new_asset.code)

        if existing_asset:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That asset already exists",
            )

        # create asset in database
        created_asset = await self.db.fetch_one(
            query=CREATE_ASSET_QUERY, values={
                "name": new_asset.name, "code": new_asset.code, "last_price": new_asset.last_price}
        )

        return created_asset
