from abc import ABC, abstractmethod
from typing import List
from .serializable import Serializable
from .factory import Factory
   
class Message(Serializable):
    @property
    def role(self):
        return self._role
    @property
    def content(self):
        return self._content

    def __init__(self, content, role='user'):
        self._role = role
        self._content = content

    def to_dict(self):
        return {
            'role': self.role,
            'content': self.content
        }

    @staticmethod
    def from_dict(data):
        assert len(data) == 2
        return Message(role=data['role'], content=data['content'])

    def show(self):
        print(f"Message role:{self.role} content:")
        print(self.content)


class Response(Serializable):
    @property
    def message(self):
        return self._message
    @property
    def input_token_count(self):
        return self._input_token_count
    @property
    def output_token_count(self):
        return self._output_token_count
    @property
    def is_success(self):
        return self._is_success
    @property
    def is_failure(self):
        return self._is_success != True
    @property
    def status_code(self):
        return self._status_code
    @property
    def error(self):
        return self._error

    def show_header(self):
        if not self.is_success:
            print(f"Response failure; status:{self.status_code} error:{self.error}")
        else:
            print(f"Response successful; tokens: i:{self.input_token_count} o:{self.output_token_count}")

    def show(self):
        self.show_header()
        if self.is_success:
            self.message.show()

    def to_dict(self):
        return {
            'message': self.message.to_json() if self.message is not None else None,
            'input_token_count': self.input_token_count,
            'output_token_count': self.output_token_count,
            'is_success': self.is_success,
            'status_code': self.status_code,
            'error': str(self.error)
        }

    @staticmethod
    def from_dict(data):
        return Response(message = Message.from_json(data['message']),
                        is_success = data['is_success'],
                        status_code = data['status_code'],
                        error = data['error'],
                        input_token_count = data['input_token_count'],
                        output_token_count = data['output_token_count'])

    @staticmethod
    def error_response(status_code, error):
        return Response(status_code = status_code, error = error, is_success=False)

    def __init__(self,
                 message = None,
                 is_success:bool=True,
                 status_code=200,
                 error=None,
                 input_token_count=None,
                 output_token_count=None):
        self._message = message
        self._input_token_count = input_token_count
        self._output_token_count = output_token_count
        self._status_code = status_code
        self._error = error
        self._is_success = is_success
        if is_success:
            assert isinstance(message, Message)
            assert isinstance(input_token_count, int)
            assert isinstance(output_token_count, int)


class LLMChatCompletion(ABC):
    @property
    @abstractmethod
    def context_size(self):
        raise NotImplemented()

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        # this returns an LLM object
        raise NotImplemented()

    @abstractmethod
    def query(self, messages:List[Message], json_response=False, temperature=1.0):
        # this returns a Response
        raise NotImplemented()

import json
import time
from .cache import Cache

class LLMChatCompletionCache:
    def __init__(self, model: LLMChatCompletion, db_path : str):
        self.cache = Cache(db_path)
        self.model = model
        self.model_name = f"cache:{self.model.model_name}"
        self.min_seconds_per_request = None

    def set_rate_limit(self, max_requests_per_second: int):
        assert max_requests_per_second > 0
        self.min_seconds_per_request = 60.0 / max_requests_per_second

    @property
    def context_size(self):
        return self.model.context_size

    def _generate_key(self, messages, json_response, temperature):
        key = {
            'model_name': self.model.model_name,
            'json_response': json_response,
            'temperature': f'{temperature:.3f}',
            'messages': [x.to_json() for x in messages]
        }
        return json.dumps(key)

    def purge_query(self, messages:List[Message], json_response=False, temperature=1.0):
        key = self._generate_key(messages, json_response, temperature)
        self.cache.purge(key)

    def purge(self, response):
        if not hasattr(response,'cache_key'): return
        if response.cache_key == None: return
        self.cache.purge(response.cache_key)

    def query(self, messages:List[Message], json_response=False, temperature=1.0):
        key = self._generate_key(messages, json_response, temperature)
        data = self.cache.get(key)
        if data is not None:
            resp = Response.from_json(data)
            resp.cache_key = key
        else:
            t0 = time.time()
            resp = self.model.query(messages=messages, json_response=json_response, temperature=temperature)
            if resp.is_success:
                data = resp.to_json()
                self.cache.put(key, data)
                resp.cache_key = key
            else:
                resp.cache_key = None
            t1 = time.time()
            if self.min_seconds_per_request is not None:
                dt = self.min_seconds_per_request - (t1-t0)
                if dt > 0:
                    time.sleep(dt)

        return resp

class LLMChatCompletionFactory(Factory):
    _class = LLMChatCompletion

