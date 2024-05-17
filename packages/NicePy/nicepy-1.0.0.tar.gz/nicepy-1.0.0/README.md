# NicePy

A python package for the CXOnce NICE/inContact API

This is a work in progress and currently far from complete in terms of endpoints. More will be added over time.

# Installation
You can either install the package

`pip install nicepy`

or if you download the code, from the folder containing the `setup.py`, you can enter

`pip install .`

Functions that involve media may require one or both of `ffprobe` and `ffmpeg` to be in the system path. If you receive a file not found error this is likely the reason.

# Configuration
* In your project folder, create a file `nicepy_config.json` containing the following:

```json
{
  "client_id" : "APP_ID",
  "client_secret" : "APP_SECRET",
  "username" : "USER_ID",
  "password" : "USER_SECRET",
  "APIVersion" : "28.0"
}
```

`client_id` and `client_secret` are the keys provided when registering an API app with NICE. `username` and `password` are the keys generated on a user account within NICE.

`APIVersion` if not set will default to v28.0. All endpoints with versioning (will) allow passing a version in the call.

## Implemented Functions

- Agents
  - GetAgents
  - GetAgentSkillAssignments
  - GetAgentStates
  - GetInactiveAgents
  - AgentByUUID
  - AgentByLogin

- Contacts
  - GetContactDetails
  - GetMultiContactDetails
  - Fetch_Recording
  - Fetch_Recording_AudioSegment (Threaded)
  - AudioSegment_To
  - GetRecordingURL
  - GetContactStates
  - GetMultiContactStateHistory (Threaded)
  - GetCompletedContacts
  - IsFinalContact

- Adherence
  - GetAdherenceData
- Dispositions
  - GetDispositions



## Usage Examples
To come
