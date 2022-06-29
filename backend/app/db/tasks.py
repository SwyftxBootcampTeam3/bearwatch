import os
from fastapi import FastAPI
from databases import Database
from app.core.config import DATABASE_URL, DB_MIN_CONNECTIONS, DB_MAX_CONNECTIONS
import logging

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    """
    connects to db using datbases package
    During testing os.env(TESTING) is set to 1 so that we use a mocked database rather than the actual database.
    This function is never called directly it is used by a handler for the application.
    """
    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else DATABASE_URL
    database = Database(
        DB_URL, min_size=DB_MIN_CONNECTIONS, max_size=DB_MAX_CONNECTIONS
    )
    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    """
    Accesses the applications current state, gets the db and attempts to disconnect.
    This function is never called directly it is used by a handler for the application.
    """
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")