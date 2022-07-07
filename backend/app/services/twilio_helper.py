from twilio.rest import Client

# credit https://www.twilio.com/docs/sms/send-messages

#environment variables
# from app.core import config
from starlette.config import Config

config = Config(".env")

# client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)

client = Client(config("ACCOUNT_SID", cast=str), config("AUTH_TOKEN", cast=str))

def create_message(coin_name: str, coin_code:str, alert_price: int):
    price_string = str(alert_price)
    message = "Hi, your watched coin {} ({}) is now ${} AUD. Log in now to view!".format(coin_name, coin_code, price_string)
    return message

#sms disabled by default due to paylimit
def send_message(phoneNumber: str,  coin_name: str, coin_code: str, alert_price: int, sms_enabled:bool = False):
    if(sms_enabled):
        message = client.messages.create(
            to=phoneNumber, 
            from_="+16162292836",
            body=create_message(coin_name, coin_code, alert_price)
            )
        print(message.sid)
    else: print(create_message(coin_name, coin_code, alert_price))
