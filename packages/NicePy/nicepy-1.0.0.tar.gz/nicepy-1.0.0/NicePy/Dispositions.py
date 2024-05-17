import requests as _requests
from . import Connection as _Connection
from .Config import APIVersion

def GetDispositions(APIVersion : str = APIVersion):  
  response = _requests.get(f'{_Connection.ApiURL()}services/v{APIVersion}/dispositions', headers=_Connection.AuthHeader())
  returnData = {}

  if (response.ok & (response.status_code != 204)):
    if (len(response._content) > 0):
      returnData = response.json()['dispositions']
      
  return returnData