

import json
import time
from pytest import param

import requests
from sqlalchemy import JSON

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

def check_new_asset():
    token = get_server_auth_token()
    headers = {
        'Authorization': 'Bearer ' + token
    }
    req_swyftx = requests.get('https://api.swyftx.com.au/live-rates/1/')
    req_server = requests.get(route + '/api/assets', headers=headers)
    print(len(req_server.json()))
    print(len(req_swyftx.json()))

check_new_asset()