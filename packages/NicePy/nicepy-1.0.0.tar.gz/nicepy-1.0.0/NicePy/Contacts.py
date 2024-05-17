from pydub import AudioSegment as _AudioSegment
from joblib import Parallel as _Parallel, delayed as _delayed
import io as _io
import json as _json
import requests as _requests
from . import Connection as _Connection
from datetime import timedelta
from .Funcs import UTCZStr_To_Local as _UTC_To_Local, UTCZStrToDateTime as _UTCStr_To_Datetime, DotDict as _DotDict
from .Config import APIVersion


__AllRecords = []

def __GetCompletedContacts(StartDate,
                           EndDate,
                           Skip=0,
                           Fields='',
                           MAX_RESULTS=1000,
                           MediaTypeId=None,
                           APIVersion=APIVersion):
  global __AllRecords
  global __totalRecords

  headers = _Connection.AuthHeader()
  parameters = {
      'startDate': StartDate,
      'endDate': EndDate,
      'top': MAX_RESULTS,
      'fields': Fields,
      'skip': Skip,
  }

  if MediaTypeId is not None:
    parameters.update({'mediaTypeId': MediaTypeId})

  response = _requests.get(f'{_Connection.ApiURL()}/services/v{APIVersion}/contacts/completed', params=parameters, headers=headers)

  if (response.ok):
    if (len(response._content) > 0):
      data = _json.loads(response._content)
      __AllRecords.extend(data['completedContacts'])

      if (len(data.get('completedContacts', '')) < MAX_RESULTS):
        return None, data['totalRecords']
      else:
        return Skip + MAX_RESULTS, data['totalRecords']
        
  else:
    response.raise_for_status()


def GetContactDetails(ContactID, Fields='', APIVersion : str = APIVersion):
  parameters = {
   'fields': Fields
  }
  response = _requests.get(f'{_Connection.ApiURL()}/services/v{APIVersion}/contacts/{ContactID}', params=parameters, headers=_Connection.AuthHeader())
  if (response.ok):
    if len(response.content) > 0:
      data = _DotDict(_json.loads(response.content))
      if data.get('contactId', {'contactStartDate', None }).get('contactStartDate', None) is not None:
        data['contactId']['contactStartDateLocal'] = _UTC_To_Local(data['contactId']['contactStartDate'])
        data['contactId']['contactStartDate'] = _UTCStr_To_Datetime(data['contactId']['contactStartDate'])
        data['contactId']['contactEndDate'] = data.contactId.contactStartDate + timedelta(seconds=data.contactId.totalDurationSeconds)
        data['contactId']['contactEndDateLocal'] = data.contactId.contactStartDateLocal + timedelta(seconds=data.contactId.totalDurationSeconds)
      return data

  return None


def Fetch_Recording(ContactID, mediaType='voice-only'):
  """
  Returns the raw recording object for ContactID
  """
  recording_url = GetRecordingURL(ContactID, mediaType=mediaType)
  response = _requests.get(recording_url)
  return response.content


def Fetch_Recording_AudioSegment(ContactID):
  """
  Fetches the audio recording for the ContactID as a pydub AudioSegment
  """
  mp4Data = Fetch_Recording(ContactID)
  audio = _AudioSegment.from_file(_io.BytesIO(mp4Data), format="mp4")  
  return audio


def AudioSegment_To(Audio, toType='wav'):
  """
  Requires ffprobe[.exe] to be in the path

    Audio: 
      AudioSegment object
    toType ['wav']: 
      Formats other than WAV or RAW also require ffmpeg in the path
  """
  audioExportData = Audio.export(format=toType).read()
  return audioExportData

def GetRecordingURL(ContactID, mediaType='voice-only'):
  """Retrieve the URL to the recording

  Args:
      ContactID
      mediaType (str, optional): Defaults to 'voice-only'. Other options are 'voice-and-screen', 'email', 'chat', and 'all'

  Returns:
      str: The URL to the recording
  """

  url = f'https://na1.nice-incontact.com/media-playback/v1/contacts?acd-call-id={ContactID}&media-type=all&exclude-waveforms=true&isDownload=false&media-type={mediaType}'
  headers = _Connection.AuthHeader()
  response = _requests.get(url, headers=headers)
  json_data = response.json()
  try:
    data_url = json_data['interactions'][0]['data']['fileToPlayUrl']
  except Exception as e:
    try:
      ExceptionText = json_data['message']
    except Exception as e:
      return None
      
    raise Exception(ExceptionText)
  
  return data_url

def GetContactStates(ContactID, APIVersion : str = APIVersion):
  """
  Returns the state history for ContactID
  """
  url = f'{_Connection.ApiURL()}/services/v{APIVersion}/contacts/{ContactID}/statehistory'
  headers = _Connection.AuthHeader()
  response = _requests.get(url, headers=headers)
  json_data = response.json()
  try:
    retVal = json_data['contactStateHistory']
    return retVal
  except Exception as e:
    print(f'Error! GetContactStates({ContactID})\n{e}')

  return []


def GetCompletedContacts(StartDate : str, EndDate : str, MaxIteration : int = 1000, Fields : str = '', MediaTypeId : int =None, APIVersion : str = APIVersion):
  """Retrieve completed contacts
  
  Args
    StartDate, EndDate: 
      Date Time value with UTC offset. eg "2024-01-30T00:00:00-05:00"

    MaxIteration [1000]: 
      Defines the maximum number of records to fetch at a time. If it times out, go lower

    Fields: 
      comma separated list of field names to include in results

    MediaTypeId: 
      Filter by media type. 
        1: E-Mail
        3: Chat
        4: Phone Call
        5: Voice Mail
        6: Work Time
        7: SMS
        8: Social
        9: Digital
  """
  Skip = 0
  
  while Skip != None:
    Skip, Total = __GetCompletedContacts(StartDate, EndDate, Skip=Skip, MAX_RESULTS=MaxIteration, Fields=Fields, MediaTypeId=MediaTypeId, APIVersion=APIVersion)
      
  return __AllRecords

def IsFinalContact(contactId):
  states = GetContactStates(contactId)
  
  # states = data.get('contactStateHistory', {} )
  releases = list(filter(lambda x: (x.get('contactStateName', '') == 'Released'), states))
  if (len(releases) > 0):
    return { 'isFinal': 1, 'startDate': releases[0]['startDate']}
  else:
    return { 'isFinal': 0 }

def GetMultiContactStateHistory(ContactList, verbose : int = 0, threadCount : int = 8):
  retVal = _Parallel(n_jobs=threadCount, backend='threading', verbose=verbose)(_delayed(GetContactStates)(contact_id) for contact_id in ContactList)
  return retVal
  
def GetMultiContactDetails(ContactList, verbose: int = 0, threadCount : int = 8):
  retVal = _Parallel(n_jobs=threadCount, backend='threading', verbose=verbose)(_delayed(GetContactDetails)(contact_id) for contact_id in ContactList)
  return retVal