from twilio.rest import Client

# credit https://www.twilio.com/docs/sms/send-messages

#environment variables
# from app.core import config
from starlette.config import Config
from app.models.alert import Alert
from app.models.asset import Asset
from app.models.user import User

config = Config(".env")

# client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)

client = Client(config("ACCOUNT_SID", cast=str), config("AUTH_TOKEN", cast=str))

def price_alert(user:User, alert:Alert, sms_emabled:bool = False):
    message = "Hi, your watched coin {} ({}) is now ${} AUD. Log in now to view!".format(alert.asset_name, alert.asset_code, str(alert.price))
    send_message(user.phone_number, message, sms_emabled)

def new_asset_alert(user:User, asset:Asset, sms_emabled:bool = False):
    message = "Hi, a new asset {} ({}) was just added to the platform. Log in now to view!".format(asset.name, asset.code)
    send_message(user.phone_number, message, sms_emabled)


def send_message(phone_number:str, message_text:str, sms_enabled:bool):
    if(sms_enabled):
        message = client.messages.create(
            to=phone_number, 
            from_="+16162292836",
            body=message_text
            )
        print(message.sid)
    else: print(message_text)