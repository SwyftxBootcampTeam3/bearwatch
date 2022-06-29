from typing import Optional, List
from databases import Database

# app
from pydantic import EmailStr
from fastapi import HTTPException, status

# repositories
from app.db.repositories.base import BaseRepository

# from app.db.repositoris.profiles import ProfilesRepository

# models
from app.models.alert import Alert, AlertCreate, AlertUpdate

CREATE_ALERT_QUERY = """
    INSERT INTO alerts (user_id,asset_id,price,alert_type)
    VALUES (:user_id,:asset_id,:price,:alert_type)
    RETURNING id,user_id,asset_id,price,alert_type,soft_delete, created_at, updated_at;
"""

GET_ALERT_BY_ID_QUERY = """
    SELECT id,user_id,asset_id,price,alert_type,soft_delete, created_at, updated_at;
    FROM alerts
    WHERE id = :id;
"""

GET_ALL_ALERTS_QUERY = """
    SELECT id,user_id,asset_id,price,alert_type,soft_delete, created_at, updated_at;
    FROM alerts
"""

UPDATE_ALERT_PRICE_QUERY = """
    UPDATE alerts
    SET last_price = :new_price
    WHERE id = :id;
"""


class AlertsRepository(BaseRepository):
    """
    All database actions associated with Alerts
    """

    # when we init we want to ensure that the auth service is available to the repository --> we're going to be doing auth things
    def __init__(self, db: Database) -> None:
        """
        Standard repository intialise
        """
        super().__init__(db)


    async def get_alert_by_id(self, *, id: str) -> Alert:
        """
        Queries the database for the first matching user with this email.
        """

        # pass values to query
        alert = await self.db.fetch_one(
            query=GET_ALERT_BY_ID_QUERY, values={"id": id}
        )

        # if user, return UserInDB else None
        if alert:
            alert = Alert(**alert)

            # perform any other modifications on returning inDB model here TODO
            # e.g. masking password/hash/private details
        return alert

    async def get_all_alerts(self) -> List[Alert]:
        """
        Queries the database for the first matching user with this email & phone
        """

        # pass values to query
        alerts = await self.db.fetch_one(
            query=GET_ALL_ALERTS_QUERY
        )

        return map(lambda a : Alert(**a), alerts)

    async def create_alert(self, *, new_alert: AlertCreate) -> Alert:
        """
        Creates an alert.
        """

        # create alert in database
        created_alert = await self.db.fetch_one(
            query=CREATE_ALERT_QUERY, values={"user_id":new_alert.user_id,"asset_id":new_alert.asset_id,
            "price":new_alert.price,"alert_type":new_alert.alert_type}
        )

        return created_alert

    async def update_alert(self, *, updated_alert: AlertUpdate) -> None:
        """
        Creates an alert.
        """

        # create alert in database
        await self.db.fetch_one(
            query=UPDATE_ALERT_PRICE_QUERY, values={"price":updated_alert.price}
        )