import requests
from requests_oauthlib import OAuth2Session
from oauthlib import oauth2

# cred = json.loads(base64.b64decode(os.environ.get('ICAPICREDS', '')).decode())

# API_User = cred.get('username')
# API_Pass = cred.get('password')

client_id = r'30589b1c-25a2-4d0c-be6f-428edb957ab4'
client_secret = r'geDvcUMRs%2FHWe9Hxaft95A%3D%3D'
username = 'YWQPDJJAHNM2JSUGZQFKQTV4WUCKXFSA52IC3XNZV7IK75Z7BIBQ===='
password = 'MH3UPG2T4CJ3QNQSQ4AI2VD2OFFS6JKX262MSDEAI2HWBDH2NYNQ===='

Well_Known_URL = "https://cxone.niceincontact.com/.well-known/openid-configuration"
BU_URL = 'https://cxone.niceincontact.com/inContactAPI/services/v27.0/business-unit'

tokenInfo = []

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
    oauth = OAuth2Session(client=oauth2.LegacyApplicationClient(client_id=client_id))
    token = oauth.fetch_token(token_url=GetTokenEndpoint(), client_secret=client_secret, username=username, password=password )
    return token
    
def CheckToken():
    global tokenInfo
    if (tokenInfo == []):
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