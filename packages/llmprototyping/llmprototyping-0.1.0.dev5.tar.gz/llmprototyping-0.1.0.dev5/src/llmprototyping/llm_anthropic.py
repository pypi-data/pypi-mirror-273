from typing import List
import inspect
import anthropic
from .llm_interface import LLMChatCompletion, LLMChatCompletionFactory, Message, Response
from .error import LLMPException

class LLMAnthropicMessages(LLMChatCompletion):
    def __init__(self, api_key, model_name, context_size):
        self.model_name = model_name
        self._client = anthropic.Anthropic(api_key=api_key)
        self._context_size = context_size

    @property
    def context_size(self):
        return self._context_size

    def query(self, messages:List[Message], json_response=False, temperature=0.5):
        if not isinstance(temperature,float) and not isinstance(temperature,int):
            raise LLMPException.param_error("temperature must be a float in range [0.0,1.0]")
        if temperature < 0 or temperature > 1:
            raise LLMPException.param_error("temperature must be a float in range [0.0,1.0]")
        if json_response == True:
            raise LLMPException.param_error("json_response not supported")

        valid_roles = ['user','assistant']
        for msg in messages:
            if msg.role not in valid_roles:
                raise LLMPException.param_error(f"invalid role ${msg.role}; expected any of: ${valid_roles}")

        try:
            r = self._client.messages.create(
                max_tokens = 1024,
                messages = [m.to_dict() for m in messages],
                model = self.model_name,
                temperature = temperature
            )
            rcontent = r.content
            rrole = 'assistant'
            msg = Message(content=rcontent, role=rrole)
            input_tokens = r.usage.output_tokens
            output_tokens = r.usage.output_tokens
            response = Response(message=msg, input_token_count=input_tokens, output_token_count=output_tokens)
        except anthropic.BadRequestError as e:
            response = Response.error_response(status_code = e.status_code, error = str(e.response.text))
        except anthropic.AuthenticationError as e:
            response = Response.error_response(status_code = e.status_code, error = str(e.response.text))
        except anthropic.PermissionDeniedError as e:
            response = Response.error_response(status_code = e.status_code, error = str(e.response.text))
        except anthropic.NotFoundError as e:
            response = Response.error_response(status_code = e.status_code, error = str(e.response.text))
        except anthropic.APIStatusError as e:
            response = Response.error_response(status_code = e.status_code, error = str(e.response.text))
        except anthropic.RateLimitError as e:
            response = Response.error_response(status_code = e.status_code, error = str(e.response.text))
        except anthropic.UnprocessableEntityError as e:
            response = Response.error_response(status_code = e.status_code, error = str(e.response.text))
        except anthropic.InternalServerError as e:
            response = Response.error_response(status_code = e.status_code, error = str(e.response.text))
        except anthropic.APIConnectionError as e:
            response = Response.error_response(status_code = "connection error", error = str(e.response.text))
        except Exception as e:
            print(type(e))
            print(dir(e))
            response = Response.error_response(status_code = "exception", error = e)

        return response

    @classmethod
    def from_dict(cls, data):
        return cls(model_name=cls.cls_model_name, context_size=cls.cls_context_size, api_key=data['api_key'])

class Anthropic_Claude_3_Opus_20240229(LLMAnthropicMessages):
    cls_model_name = 'claude-3-opus-20240229'
    cls_context_size = 200000

class Anthropic_Claude_3_Sonnet_20240229(LLMAnthropicMessages):
    cls_model_name = 'claude-3-sonnet-20240229'
    cls_context_size = 200000

class Anthropic_Claude_3_Haiku_20240307(LLMAnthropicMessages):
    cls_model_name = 'claude-3-haiku-20240307'
    cls_context_size = 200000


def init():
    for obj in globals().values():            
        if inspect.isclass(obj) and issubclass(obj, LLMAnthropicMessages) and hasattr(obj,'cls_model_name'):
            LLMChatCompletionFactory.register(name=f'anthropic/{obj.cls_model_name}', class_obj=obj)

