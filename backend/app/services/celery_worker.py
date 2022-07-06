from logging import error
import re
import time
from backend.app.services.utils import get_server_auth_token
import utils
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

@celery.task(name="get_asset_prices")
def get_asset_prices():
    # Get rates in terms of AUD
    req_swyftx = requests.get('https://api.swyftx.com.au/live-rates/1/')
