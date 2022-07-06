from typing import List
from databases import Database

# app
from fastapi import HTTPException, status

# repositories
from app.db.repositories.base import BaseRepository

# models
from app.models.asset import Asset, AssetCreate

GET_ALL_ASSETS_QUERY = """
    SELECT id, name, code, price, external_id, created_at, updated_at
    FROM assets;
"""

GET_ASSET_BY_ID = """
    SELECT id, name, code, price, external_id, created_at, updated_at
    FROM assets
    WHERE id = :id;
"""

GET_ASSET_BY_EXTERNAL_ID = """
    SELECT id, name, code, price, external_id, created_at, updated_at
    FROM assets
    WHERE external_id = :external_id;
"""

CREATE_ASSET_QUERY = """
    INSERT INTO assets (name,code,price,external_id)
    VALUES (:name,:code,:price,:external_id)
    RETURNING id, name, code, price, external_id, created_at, updated_at;
"""

UPDATE_ASSET_PRICE_QUERY = """
    UPDATE assets
    SET price = :price
    WHERE id = :id;
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
        return list(map(lambda a: Asset(**a), assets))

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

    async def get_asset_by_external_id(self, *, external_id: int) -> Asset:
        """
        Queries the database for the first matching asset with this external id (this SHOULD be a unique field)
        """
        # pass values to query
        asset = await self.db.fetch_one(
            query=GET_ASSET_BY_EXTERNAL_ID, values={"external_id": external_id}
        )

        if asset:
            asset = Asset(**asset)

        return asset

    async def create_asset(self, new_asset: AssetCreate) -> Asset:
        """
        Creates a asset.
        """
        # unique constraints exist on external_id
        existing_asset = await self.get_asset_by_external_id(external_id=new_asset.external_id)

        if existing_asset:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That asset already exists",
            )

        # create asset in database
        created_asset = await self.db.fetch_one(
            query=CREATE_ASSET_QUERY, values={
                "name": new_asset.name, "code": new_asset.code, "price": new_asset.price, 'external_id': new_asset.external_id}
        )

        return created_asset

    async def update_asset_price(self, *, id: int, price: float) -> Asset:
        """
        Updates the last price of an asset
        """

        # Update the asset price
        updated_asset = await self.db.fetch_one(
            query=UPDATE_ASSET_PRICE_QUERY, values={
                "id": id, "price": price}
        
        )
        return updated_asset

