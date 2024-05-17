from datetime import datetime
from tzlocal import get_localzone
import debugpy as _debugpy

class DotDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            value = self[attr]
            if isinstance(value, dict):
                return DotDict(value)  # Return a new DotDict for nested dictionaries
            else:
                return value
        else:
            return None  # Return None if the attribute does not exist

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            super().__setattr__(attr, value)  # If attribute exists, use dict's __setattr__
        else:
            parts = attr.split('.')  # Split attribute by dots to handle nested dictionaries
            current_dict = self
            for part in parts[:-1]:
                if part not in current_dict:
                    current_dict[part] = DotDict()  # Create nested DotDict if it doesn't exist
                current_dict = current_dict[part]  # Move to the next level
            current_dict[parts[-1]] = value  # Set value at the final level

def UTCZStr_To_Local(UTCTime: str):
  result = UTCZStrToDateTime(UTCTime).astimezone(get_localzone())
  return result

def UTCZStrToDateTime(UTCTime: str):
  result = datetime.fromisoformat(UTCTime.replace('Z', '+00:00'))
  return result