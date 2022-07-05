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
