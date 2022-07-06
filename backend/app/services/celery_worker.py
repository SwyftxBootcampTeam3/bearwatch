import time
from celery import Celery
from starlette.config import Config

config = Config(".env")

celery = Celery(__name__)
celery.conf.broker_url = config("CELERY_BROKER_URL", cast=str)
celery.conf.result_backend = config("CELERY_RESULT_BACKEND", cast=str)

@celery.task(name="create_task")
def create_task(a,b,c):
    time.sleep(a)
    return b + c


# CronJob 1 - Fetch all updated asset prices
@celery.task(name="fetch-updated-assets")
def fetch_updated_assets():
    # Fetch from swftx api
    # Iterate over all json objects and for each
    # insert_into_db


def insert_into_db(name, code, last_price):
    # Write query to insert new prices into assets


# CronJob 2 - Fetch all triggered alerts
@celery.task(name="get-triggered-alerts")
def get_triggered_alerts():
    # Fetch from DB (write query)
    # Iterate over and send alerts using lanas stuff