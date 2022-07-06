import re
import requests
from app.api.dependencies.database import get_repository

# Rachel's Swyftx API key (read-only)
apiKey = "MLVMH30Y-QZcXoRpUArvBAK4NvMP5m5-UxmV3JMiQ4eTm"

# Use localhost for local development
route = "http://localhost:9191"

def get_auth_token_swyftx(apiKey=apiKey):
    data = { 'apiKey' : apiKey}

    headers = {
        'Content-Type': 'application/json'
    }

    r = requests.post(
        'https://api.swyftx.com.au/auth/refresh/', json=data
    )
    token = r.json()['accessToken']
    return token

def get_server_auth_token():
    
    # Define administrator params:
    creds = {
        'email': 'admin@bearwatch.com',
        'phone_number': '0412345678'
    }

    req = requests.post(route + "/api/users/login/", params=creds)

    # Add admininstrator user if not found
    if (req.status_code == 401):
        add_req = requests.post(route + '/api/users/', json={"new_user": creds})
        new_req = requests.post(route + "/api/users/login/", params=creds)
        return new_req.json()['access_token']
    print(req.json()['access_token'])
    return req.json()['access_token']


def valid_phone_number(phone_string: str):
    regex = r"^[0-9]{9,15}$"
    if not re.search(regex, phone_string, re.I):
        return False
    return True