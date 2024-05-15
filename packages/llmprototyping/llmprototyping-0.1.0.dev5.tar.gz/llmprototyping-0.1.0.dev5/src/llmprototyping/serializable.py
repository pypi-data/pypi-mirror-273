import json
from abc import ABC, abstractmethod

class Serializable(ABC):
    @abstractmethod
    def to_dict(self):
        raise NotImplemented()
    @staticmethod
    @abstractmethod
    def from_dict(data):
        raise NotImplemented()

    def to_json(self):
        return json.dumps(self.to_dict())
    @classmethod
    def from_json(cls, json_string):
        if json_string is None:
            return None
        data = json.loads(json_string)
        if data is None:
            return None
        return cls.from_dict(data)