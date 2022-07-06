from logging import error
import re
import time
from typing import List

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


# CronJob 1 - Fetch all updated asset prices
@celery.task(name="update_assets")
async def update_assets():
    assets_repo:AssetsRepository = get_repository(AssetsRepository)

    # Using markets basic table as Swyftx stores more coin prices than actual coins
    try:
        new_assets = await requests.get('https://api.swyftx.com.au/markets/info/basic/').json()
    except Exception as e:
        # This is something we would log in a real application
        print(e)

    try:
        stored_assets:List[Asset] = await assets_repo.get_all_assets()
    except Exception as e:
        # This is something we would log in a real application
        print(e)
    
    #Check for new assets
    if len(new_assets) != len(stored_assets):
        stored_asset_ids:List[int] = list(map(stored_assets, lambda a: a.external_id))
        for asset in new_asset:
            #Check if the asset doesn't exists in our db
            if asset['id'] not in stored_asset_ids:
                #Add asset
                price = (float(asset['buy']) + float(asset['sell']))/2
                new_asset = AssetCreate(name=asset['name'], code=asset['code'], price=price, external_id=asset['id'])
                try:
                    await assets_repo.create_asset(new_asset)
                    stored_assets.append(new_asset)
                except Exception as e:
                    print(e)            

    #Update our asset prices
    for asset in stored_assets:
        new_asset = list(filter(new_assets, lambda a: a['id'] == asset.external_id))[0]
        price = (float(new_asset['buy']) + float(new_asset['sell']))/2
        await assets_repo.update_asset_price(id=asset.id, price=price)


# CronJob 2 - Fetch all triggered alerts
@celery.task(name="get-triggered-alerts")
def get_triggered_alerts():
    # Fetch from DB (write query)
    # Iterate over and send alerts using lanas stuff
    pass
