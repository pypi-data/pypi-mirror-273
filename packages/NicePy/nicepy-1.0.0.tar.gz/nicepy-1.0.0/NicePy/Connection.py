import os.path as path
import json
import requests
from requests_oauthlib import OAuth2Session
from datetime import datetime, timedelta
from oauthlib import oauth2

try:
    with open("./nicepy_config.json", 'r') as configFile:
        configParams = json.loads(configFile.read())
        client_id = configParams['client_id']
        client_secret = configParams['client_secret']
        username = configParams['username']
        password = configParams['password']        
except FileNotFoundError as e:
    raise FileNotFoundError('nicepy_config.json missing from project folder')
except:
    raise ValueError('Malformed contents of nicepy_config.json')

Well_Known_URL = "https://cxone.niceincontact.com/.well-known/openid-configuration"
BU_URL = 'https://cxone.niceincontact.com/inContactAPI/services/v27.0/business-unit'

tokenInfo = []
token_expires = datetime.now()

def GetTokenEndpoint():
    response = requests.get('https://cxone.niceincontact.com/.well-known/openid-configuration')
    if response.ok:
        return response.json()['token_endpoint']
    else:
        response.raise_for_status()

def GetTenantId():
    response = requests.get(BU_URL, headers=AuthHeader())
    if response.ok:
        return response.json()['businessUnits'][0]['tenantId']
    else: 
        response.raise_for_status()

def GetAPIEndpoint():
    tenantId = GetTenantId()    
    URL = f'https://cxone.niceincontact.com/.well-known/cxone-configuration?tenantId={tenantId}'
    response = requests.get(URL, headers=AuthHeader())
    if response.ok:
        return response.json()['api_endpoint']
    else:
        response.raise_for_status()


def GetAuthToken():
    global token_expires
    oauth = OAuth2Session(client=oauth2.LegacyApplicationClient(client_id=client_id))
    token = oauth.fetch_token(token_url=GetTokenEndpoint(), client_secret=client_secret, username=username, password=password )
    token_expires = datetime.now() + timedelta(seconds=token['expires_in'])
    return token
    
def CheckToken():
    global tokenInfo
    if (tokenInfo == [] or token_expires < datetime.now()):
        tokenInfo = GetAuthToken()
        tokenInfo['api_endpoint'] = GetAPIEndpoint()
        
def GetTokenInfo():
    CheckToken()
    return tokenInfo

def ApiURL():
    CheckToken()
    return tokenInfo['api_endpoint'] + '/incontactApi/'

def Token():
    CheckToken()
    return tokenInfo['access_token']

def AuthHeader():
  return {'Authorization': f'Bearer {Token()}', 'Content-Type': 'application/x-www-form-urlencoded'}

if __name__ == '__main__':
    CheckToken()
    x = 123