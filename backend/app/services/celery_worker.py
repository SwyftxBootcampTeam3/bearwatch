from typing import List

# models
from app.models.asset import Asset, AssetCreate

# repositories
from app.db.repositories.assets import AssetsRepository


from app.api import server
from app.services.twilio_helper import new_asset_alert, price_alert

import requests
from celery import Celery
from starlette.config import Config
from app.db.repositories.alerts import AlertsRepository
from app.models.alert import Alert
from app.db.repositories.users import UsersRepository

config = Config(".env")

celery = Celery(__name__)
celery.conf.broker_url = config("CELERY_BROKER_URL", cast=str)
celery.conf.result_backend = config("CELERY_RESULT_BACKEND", cast=str)


# CronJob 1 - Fetch all updated asset prices
@celery.task(name="update_assets")
async def update_assets():
    assets_repo:AssetsRepository = AssetsRepository(server.app.state._db)

    # Using markets basic table as Swyftx stores more coin prices than actual coins
    try:
        new_assets = requests.get('https://api.swyftx.com.au/markets/info/basic/').json()
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
        stored_asset_ids:List[int] = list(map(lambda a: a.external_id, stored_assets))
        for asset in new_assets:
            #Check if the asset doesn't exists in our db
            if asset['id'] not in stored_asset_ids:
                #Add asset
                try:
                    price = (float(asset['buy']) + float(asset['sell']))/2
                    new_asset = AssetCreate(name=asset['name'], code=asset['code'], price=price, external_id=asset['id'])
                    await assets_repo.create_asset(new_asset)
                    await send_new_asset_alert(new_asset)
                except Exception as e:
                    pass          
    
    #Update our asset prices
    for index,asset in enumerate(stored_assets):
        #The order of stored assets and new assets SHOULD align, so we use this primarily, then fall back to a filter if we don't find the expected asset
        try:
            if (new_assets[index]['id'] == asset.external_id):
                new_asset = new_assets[index]
            else:
                new_asset = list(filter(lambda a: a['id'] == asset.external_id,new_assets))[0]
            price = (float(new_asset['buy']) + float(new_asset['sell']))/2
            await assets_repo.update_asset_price(id=asset.id, price=price)
        except Exception as e:
            print(e)
    
# CronJob 2 - Fetch all triggered alerts
@celery.task(name="get-triggered-alerts")
async def get_triggered_alerts():
    # Alerts are triggered through a db function when the underlying asser price updates
    # Fetch triggered alerts and send notification
    alerts_repo:AlertsRepository = AlertsRepository(server.app.state._db)
    user_repo:UsersRepository = UsersRepository(server.app.state._db)

    try:
        triggered_alerts:List[Alert] = await alerts_repo.get_alerts_to_notify()
    except Exception as e:
        # This is something we would log in a real application
        print(e)

    #Send Notification and set not active
    for alert in triggered_alerts:
        try:
            alert_user = await user_repo.get_user_by_id(id=alert.user_id)
            price_alert(alert_user, alert)
            #Set as notified
            await alerts_repo.set_alert_notified_by_id(alert_id=alert.id)
        except Exception as e:
            print(e)

async def send_new_asset_alert(asset:Asset):
    user_repo:UsersRepository = UsersRepository(server.app.state._db)
    all_users = await user_repo.get_all_users()
    for user in all_users:
        new_asset_alert(user, asset)