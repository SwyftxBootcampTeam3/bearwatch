from typing import List
from asyncpg import ForeignKeyViolationError
from databases import Database

# app
from fastapi import HTTPException, status

# repositories
from app.db.repositories.base import BaseRepository

# from app.db.repositoris.profiles import ProfilesRepository

# models
from app.models.alert import Alert, AlertCreate, AlertUpdate

CREATE_ALERT_QUERY = """
    INSERT INTO alerts (user_id,asset_id,price,alert_type)
    VALUES (:user_id,:asset_id,:price,:alert_type)
    RETURNING id;
"""

GET_ALERT_BY_ID_QUERY = """
    SELECT alerts.id,alerts.user_id,alerts.asset_id,alerts.price,alerts.alert_type,alerts.active,alerts.triggered,alerts.soft_delete, alerts.created_at, alerts.updated_at, assets.name as asset_name, assets.code as asset_code, assets.price as asset_price
    FROM alerts
    INNER JOIN assets ON assets.id=alerts.asset_id
    WHERE alerts.id = :id AND alerts.soft_delete = false;
"""

GET_ALERT_BY_USER_ID_QUERY = """
    SELECT alerts.id,alerts.user_id,alerts.asset_id,alerts.price,alerts.alert_type,alerts.active,alerts.triggered,alerts.soft_delete, alerts.created_at, alerts.updated_at, assets.name as asset_name, assets.code as asset_code, assets.price as asset_price
    FROM alerts
    INNER JOIN assets ON assets.id=alerts.asset_id
    WHERE alerts.user_id = :user_id AND alerts.soft_delete = false;
"""

GET_ALL_ALERTS_QUERY = """
    SELECT alerts.id,alerts.user_id,alerts.asset_id,alerts.price,alerts.alert_type,alerts.active,alerts.triggered,alerts.soft_delete, alerts.created_at, alerts.updated_at, assets.name as asset_name, assets.code as asset_code, assets.price as asset_price
    FROM alerts
    INNER JOIN assets ON assets.id=alerts.asset_id
    WHERE alerts.soft_delete = false;
"""

UPDATE_ALERT_PRICE_QUERY = """
    UPDATE alerts
    SET price = :price, alert_type = :alert_type
    WHERE id = :id AND soft_delete = false;
"""

DELETE_ALERT_QUERY = """
    UPDATE alerts
    SET soft_delete = true
    WHERE id = :id AND soft_delete = false;
"""

SLEEP_ALERT_QUERY = """
    UPDATE alerts
    SET active = false
    WHERE id = :id AND soft_delete = false;
"""

UNSLEEP_ALERT_QUERY = """
    UPDATE alerts
    SET active = true
    WHERE id = :id AND soft_delete = false;
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

    async def get_alert_by_id(self, id: str) -> Alert:
        """
        Queries the database for an alert matching this id
        """

        # pass values to query
        alert = await self.db.fetch_one(
            query=GET_ALERT_BY_ID_QUERY, values={"id": id}
        )

        if alert:
            alert = Alert(**alert)

        return alert

    async def get_alerts_by_user_id(self, user_id: str) -> List[Alert]:
        """
        Queries the database for all alerts for a user
        """
        # pass values to query
        alerts = await self.db.fetch_all(
            query=GET_ALERT_BY_USER_ID_QUERY, values={"user_id": user_id}
        )

        # Map alerts to alert model
        return list(map(lambda a: Alert(**a), alerts))

    async def get_all_alerts(self) -> List[Alert]:
        """
        Queries the database for all non-deleted alerts
        """

        # pass values to query
        alerts = await self.db.fetch_all(
            query=GET_ALL_ALERTS_QUERY
        )

        # Map alerts to alert model
        return list(map(lambda a: Alert(**a), alerts))

    async def create_alert(self, *, new_alert: AlertCreate) -> Alert:
        """
        Creates an alert
        """
        # create alert in database
        try:
            created_alert_id = await self.db.fetch_one(
                query=CREATE_ALERT_QUERY, values={"user_id": new_alert.user_id, "asset_id": new_alert.asset_id,
                                                  "price": new_alert.price, "alert_type": new_alert.alert_type}
            )
        except ForeignKeyViolationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That asset does not exist!",
            )

        if created_alert_id:
            asset_id = int(created_alert_id['id'])

        return await self.get_alert_by_id(asset_id)

    async def update_alert(self, alert_id: int, updated_alert: AlertUpdate) -> None:
        """
        Update an alerts:
        - Price
        """

        # update alert in database
        await self.db.fetch_one(
            query=UPDATE_ALERT_PRICE_QUERY, values={
                "price": updated_alert.price, "alert_type": updated_alert.alert_type, "id": alert_id}
        )

    async def delete_alert_by_id(self, *, alert_id: int) -> None:
        """
        Delete an alert
        """

        # update alert in database
        await self.db.fetch_one(
            query=DELETE_ALERT_QUERY, values={
                "id": alert_id}
        )

    async def sleep_alert_by_id(self, *, alert_id: int) -> None:
        """
        Sleep an alert
        """

        # update alert in database
        await self.db.fetch_one(
            query=SLEEP_ALERT_QUERY, values={
                "id": alert_id}
        )

    async def unsleep_alert_by_id(self, *, alert_id: int) -> None:
        """
        Sleep an alert
        """

        # update alert in database
        await self.db.fetch_one(
            query=UNSLEEP_ALERT_QUERY, values={
                "id": alert_id}
        )