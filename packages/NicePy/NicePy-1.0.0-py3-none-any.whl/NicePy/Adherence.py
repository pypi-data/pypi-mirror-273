import requests as _requests
from . import Connection as _Connection
from datetime import datetime as _datetime
from dateutil import tz as _tz

def _StampToDateTime(d: dict, key: str) -> None:
  if d[key].count(':') == 1:
    d[key] = d[key].replace('Z', ':00Z')
    
  if '.' in d[key]:
      d[key] = d[key][:d[key].index('.')] + d[key][-1]
  d[key] = _datetime.strptime(d[key], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=_tz.tzutc()).astimezone(_tz.tzlocal())


def GetAdherenceData():
  response = _requests.get(f'https://na1.nice-incontact.com/rta/?since=', headers=_Connection.AuthHeader())

  if (response.ok & (response.status_code != 204)):
    if (len(response._content) > 0):
      data = response.json()['snapshot']
      returnData = []
      for key,item in data.items():
        if item['acdEventId'] == 'LoggedOut' and item['inAdherence']==False:

          _StampToDateTime(item,'eventStartDateTime')
          item['eventStartDateTimeStr'] = item['eventStartDateTime'].strftime('%Y-%m-%d %#I:%M %p')

          _StampToDateTime(item,'expectedActivityEndTime')
          item['expectedActivityEndTimeStr'] = item['eventStartDateTime'].strftime('%Y-%m-%d %#I:%M %p')

          _StampToDateTime(item,'expectedActivityStartTime')
          item['expectedActivityStartTimeStr'] = item['expectedActivityStartTime'].strftime('%Y-%m-%d %#I:%M %p')

          _StampToDateTime(item,'expectedActivityEndTimeOffsetDateTime')
          item['expectedActivityEndTimeOffsetDateTimeStr'] = item['expectedActivityEndTimeOffsetDateTime'].strftime('%Y-%m-%d %#I:%M %p')

          _StampToDateTime(item,'expectedActivityStartTimeOffsetDateTime')
          item['expectedActivityStartTimeOffsetDateTimeStr'] = item['expectedActivityStartTimeOffsetDateTime'].strftime('%Y-%m-%d %#I:%M %p')

          _StampToDateTime(item,'ooaStartTime')
          item['ooaStartTimeStr'] = item['ooaStartTime'].strftime('%Y-%m-%d %#I:%M %p')

          _StampToDateTime(item,'lastUpdateTime')
          item['lastUpdateTimeStr'] = item['lastUpdateTime'].strftime('%Y-%m-%d %#I:%M %p')

          item['ooaDelta'] = (_datetime.now().astimezone(_tz.tzlocal()) - item['ooaStartTime'])
          item['ooaDuration'] = f"{item['ooaDelta'].seconds//3600}:{(item['ooaDelta'].seconds//60)%60:02d}"
          item['key']=key

          returnData.append(item)

      return returnData

