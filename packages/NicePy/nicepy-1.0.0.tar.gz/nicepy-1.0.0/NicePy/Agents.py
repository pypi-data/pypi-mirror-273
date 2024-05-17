from collections import defaultdict
import requests
from . import Connection
import json 
from datetime import datetime, timedelta
import time
from .Config import APIVersion

def AgentByLogin(agents, login):
  for agent in agents:
    if agent['userName'] == login:
      return agent
  
  return None

def AgentByUUID(agents, uuid):
  for agent in agents:
    if agent['userId'] == uuid:
      return agent
  
  return None 

def GetInactiveAgents():
    data = GetAgents(includeFields="agentId", isActive=False)
    dataList = [obj["agentId"] for obj in data]
    return dataList

def _minSecAgo(utcTimeStamp):
  if utcTimeStamp is None:
     return 'N/A'
  
  utcTime = datetime.strptime(utcTimeStamp, "%Y-%m-%dT%H:%M:%S.%fZ")
  local_offset_seconds = -time.timezone if (time.localtime().tm_isdst == 0) else -time.altzone
  timestamp_local = utcTime + timedelta(seconds=local_offset_seconds)
  time_difference = datetime.now() - timestamp_local
  minutes = time_difference.seconds // 60
  seconds = time_difference.seconds % 60
  return f'{minutes}:{seconds:02}'

def GetAgentStates(APIVersion : str = APIVersion, Fields : str = ''):
    headers = Connection.AuthHeader()

    URL = f"{Connection.ApiURL()}/services/v{APIVersion}/agents/states"
    params = {
        "fields": Fields
    }

    response = requests.get(URL, headers=headers, params=params)

    if response.ok:
        if len(response.content) > 0:
            data = json.loads(response.content)

            agentStates = [
                {**obj, 'timeInState': _minSecAgo(obj['startDate'])}
                for obj in data["agentStates"]
                if obj["agentStateName"] != "LoggedOut"
            ]

            return agentStates
    else:
        return {}


def GetAgentSkillAssignments(APIVersion = APIVersion):
    inactiveAgents = GetInactiveAgents()

    headers = Connection.AuthHeader()
    skip = 0
    nextURL = 'primer'
    skillAssignments = []

    URL = f"{Connection.ApiURL()}/services/v{APIVersion}/agents/skills"
    params = {
        "fields": "isActive,isOutbound,agentId,agentName,teamId,skillId,skillName,campaignName",
        "mediaTypeId": 4,
        "skip": skip
    }

    while nextURL is not None:
      response = requests.get(URL, headers=headers, params=params)
      if response.ok:
        if len(response.content) > 0:
          data = json.loads(response.content)
          skillAssignments.extend(data['agentSkillAssignments'])
          params['skip'] += 10000
          nextURL = data['_links']['next']
        else: 
          nextURL = None
      else:
          nextURL = None

    if len(skillAssignments) > 0:
      data = json.loads(response.content)

      records = [
          obj
          for obj in skillAssignments
          if obj["isActive"] and not obj["isOutbound"]
      ]
      activeRecords = [
          obj for obj in records if obj["agentId"] not in inactiveAgents
      ]

      grouped_data = defaultdict(lambda: {"agentIds": [], "teamIds": []})

      for assignment in activeRecords:
          key = (
              assignment["skillId"],
              assignment["skillName"],
              assignment["campaignName"],
          )
          grouped_data[key]["skillId"] = assignment["skillId"]
          grouped_data[key]["skillName"] = assignment["skillName"]
          grouped_data[key]["campaignName"] = assignment["campaignName"]
          grouped_data[key]["agentIds"].append(assignment["agentId"])
          grouped_data[key]["teamIds"].append(assignment["teamId"])

      # Convert grouped_data to a list of dictionaries
      result_list = list(grouped_data.values())

      return result_list
    else:
        return {}

def GetAgents(includeFields = None, isActive = None):

  params = {}

  if includeFields is not None:
    params.update({ "fields": includeFields})

  if isActive is not None:    
      params.update({"isActive": str(isActive)})

  response = requests.get(f'{Connection.ApiURL()}services/v28.0/agents', headers=Connection.AuthHeader(), params=params)
  returnData = {}

  if (response.ok & (response.status_code != 204)):
    if (len(response._content) > 0):
      returnData = response.json()['agents']
      
  return returnData