from logging import error
import re
import time

# models
from backend.app.models.asset import Asset, AssetCreate

# repositories
from backend.app.db.repositories.assets import AssetsRepository

from backend.app.api.dependencies.database import get_repository

from backend.app.services.utils import get_server_auth_token

import requests
from celery import Celery
from starlette.config import Config

config = Config(".env")

celery = Celery(__name__)
celery.conf.broker_url = config("CELERY_BROKER_URL", cast=str)
celery.conf.result_backend = config("CELERY_RESULT_BACKEND", cast=str)

apiKey = "MLVMH30Y-QZcXoRpUArvBAK4NvMP5m5-UxmV3JMiQ4eTm"

# Use localhost for local development
route = "http://localhost:9191"

@celery.task(name="create_task")
def create_task(a,b,c):
    time.sleep(a)
    return b + c

# CronJob 1 - Fetch all updated asset prices
@celery.task(name="update_assets")
def update_assets():
    token = get_server_auth_token()
    headers = {
        'Authorization': 'Bearer ' + token
    }

    assets_repo = get_repository(AssetsRepository)

    # Using markets basic table as Swyftx stores more coin prices than actual coins
    req_swyftx = requests.get('https://api.swyftx.com.au/markets/info/basic/').json()

    # Get prices in AUD
    # req_prices = requests.get('https://api.swyftx.com.au/live-rates/1/')

    req_server = requests.get(route + '/api/assets', headers=headers)

    num_swyftx, num_server = len(req_swyftx.json()), len(req_server.json())

    for i in range(num_server - 1):
        coin_data = req_swyftx[i]

        # calculate coin price by averaging buy and sell price
        coin_price = (float(coin_data['buy']) + float(coin_data['sell']))/2

        assets_repo.update_asset_price(code=coin_data['code'], price=coin_price)

    # Add new assets if there are any
    if (num_server < num_swyftx):
        for i in range(num_server, num_swyftx):
            # Get the name, code and id for the new coin
            coin_data = req_swyftx[i]

            # calculate coin price by averaging buy and sell price
            coin_price = (float(coin_data['buy']) + float(coin_data['sell']))/2

            new_asset = AssetCreate(name=coin_data['name'], code=coin_data['code'], price=coin_price)

            # Add new asset to the AssetRepository
            assets_repo.create_asset(new_asset)
    



# CronJob 2 - Fetch all triggered alerts
@celery.task(name="get-triggered-alerts")
def get_triggered_alerts():
    # Fetch from DB (write query)
    # Iterate over and send alerts using lanas stuff
    pass
