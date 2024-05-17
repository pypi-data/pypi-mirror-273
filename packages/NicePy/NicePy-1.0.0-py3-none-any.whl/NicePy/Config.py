import json

try:
    with open("./nicepy_config.json", 'r') as configFile:
        configParams = json.loads(configFile.read())
        APIVersion = configParams.get('APIVersion', '28.0')
except FileNotFoundError as e:
    raise FileNotFoundError('nicepy_config.json missing from project folder')
except:
    raise ValueError('Malformed contents of nicepy_config.json')