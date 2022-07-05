from twilio.rest import Client

# credit https://docs.sendgrid.com/for-developers/sending-email/quickstart-python

#TODO add to environment variables / kubernetes secrets
accountSid = "AC3e213fe045faa378d90724ef0f500a42"
authToken = "c349b07c121c6c564e03e9b49e3fb3d9"
client = Client(accountSid, authToken)

smsEnabled = False #enable this when wanting to send messaged - be aware of pay limit!

def createMessage(coinType: str, alertPrice: str):
    message = "Hi, your watched coin {} is now {}. Log in now to view!".format(coinType, alertPrice)
    return message
    
def sendMessage(phoneNumber: str,  coinType: str, alertPrice: str):
    if(smsEnabled):
        message = client.messages.create(
            to=phoneNumber, 
            from_="+16162292836",
            body=createMessage(coinType, alertPrice)
            )
        print(message.sid)
    else: print(createMessage(coinType, alertPrice))

#test
#function to call to send a message 
sendMessage("+61439020560", "BearCoin", "$1000.00")


