from typing import List
import inspect
import openai
from .llm_interface import LLMChatCompletion, LLMChatCompletionFactory, Message, Response
from .error import LLMPException

class LLMOpenAIChatCompletion(LLMChatCompletion):
    def __init__(self, api_key, model_name, context_size):
        self.model_name = model_name
        self._client = openai.OpenAI(api_key=api_key)
        self._context_size = context_size

    @property
    def context_size(self):
        return self._context_size

    def query(self, messages:List[Message], json_response=False, temperature=1.0):
        if not isinstance(temperature,float) and not isinstance(temperature,int):
            raise LLMPException.param_error("temperature must be a float in range [0.0,2.0]")
        if temperature < 0 or temperature > 2:
            raise LLMPException.param_error("temperature must be a float in range [0.0,2.0]")

        try:
            rformat = {"type": "json_object"} if json_response else None
            r = self._client.chat.completions.create(
                messages = [m.to_dict() for m in messages],
                model = self.model_name,
                response_format = rformat,
                temperature = temperature
            )
            rcontent = r.choices[0].message.content
            rrole = r.choices[0].message.role
            msg = Message(content=rcontent, role=rrole)
            input_tokens = r.usage.prompt_tokens
            output_tokens = r.usage.completion_tokens
            response = Response(message=msg, input_token_count=input_tokens, output_token_count=output_tokens)
        except openai.APITimeoutError as e:
            response = Response.error_response(status_code = "timeout", error = f"timeout")
        except openai.APIConnectionError as e:
            response = Response.error_response(status_code = "connection error", error = f"{e.body}")
        except openai.BadRequestError as e:
            response = Response.error_response(status_code = e.status_code, error = f"{e.body}")
        except openai.AuthenticationError as e:
            response = Response.error_response(status_code = e.status_code, error = f"{e.body}")
        except openai.PermissionDeniedError as e:
            response = Response.error_response(status_code = e.status_code, error = f"{e.body}")
        except openai.RateLimitError as e:
            response = Response.error_response(status_code = e.status_code, error = f"{e.body}")
        except openai.APIError as e:
            response = Response.error_response(status_code = e.status_code, error = f"{e.body}")
        except Exception as e:
            print(type(e))
            print(dir(e))
            response = Response.error_response(status_code = "exception", error = e)

        return response

    @classmethod
    def from_dict(cls, data):
        return cls(model_name=cls.cls_model_name, context_size=cls.cls_context_size, api_key=data['api_key'])

class OpenAI_GPT_4o(LLMOpenAIChatCompletion):
    cls_model_name = 'gpt-4o'
    cls_context_size = 128000

class OpenAI_GPT_4_turbo(LLMOpenAIChatCompletion):
    cls_model_name = 'gpt-4-turbo'
    cls_context_size = 128000

class OpenAI_GPT_4_turbo_preview(LLMOpenAIChatCompletion):
    cls_model_name = 'gpt-4-turbo-preview'
    cls_context_size = 128000

class OpenAI_GPT_3_5_turbo(LLMOpenAIChatCompletion):
    cls_model_name = 'gpt-3.5-turbo'
    cls_context_size = 16385

def init():
    for obj in globals().values():            
        if inspect.isclass(obj) and issubclass(obj, LLMOpenAIChatCompletion) and hasattr(obj,'cls_model_name'):
            LLMChatCompletionFactory.register(name=f'openai/{obj.cls_model_name}', class_obj=obj)

