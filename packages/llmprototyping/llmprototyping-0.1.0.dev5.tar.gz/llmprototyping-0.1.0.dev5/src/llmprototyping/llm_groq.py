from typing import List
import inspect
import groq
from .llm_interface import LLMChatCompletion, LLMChatCompletionFactory, Message, Response
from .error import LLMPException

class LLMGroqChatCompletion(LLMChatCompletion):
    def __init__(self, api_key, model_name, context_size):
        self.model_name = model_name
        self._client = groq.Groq(api_key=api_key)
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
        except groq.APIConnectionError as e:
            response = Response.error_response(status_code = "connection error", error = f"backend unreachable ({e.__cause__})")
        except groq.RateLimitError as e:
            response = Response(status_code = "rate limit error", error = "rate limit hit")
        except groq.BadRequestError as e:
            response = Response.error_response(status_code = e.status_code, error = e.body)
        except groq.APIStatusError as e:
            response = Response.error_response(status_code = e.status_code, error = e.body)
        except Exception as e:
            print(type(e))
            print(dir(e))
            response = Response.error_response(status_code = "exception", error = e)

        return response

    @classmethod
    def from_dict(cls, data):
        return cls(model_name=cls.cls_model_name, context_size=cls.cls_context_size, api_key=data['api_key'])

class Groq_Llama3_70b_8192(LLMGroqChatCompletion):
    cls_model_name = 'llama3-70b-8192'
    cls_context_size = 8192

class Groq_Llama3_8b_8192(LLMGroqChatCompletion):
    cls_model_name = 'llama3-8b-8192'
    cls_context_size = 8192

class Groq_Mixtral_8x7b_32768(LLMGroqChatCompletion):
    cls_model_name = 'mixtral-8x7b-32768'
    cls_context_size = 32768

class Groq_Gemma_7b_It(LLMGroqChatCompletion):
    cls_model_name = 'gemma-7b-it'
    cls_context_size = 8192

def init():
    for obj in globals().values():            
        if inspect.isclass(obj) and issubclass(obj, LLMGroqChatCompletion) and hasattr(obj,'cls_model_name'):
            LLMChatCompletionFactory.register(name=f'groq/{obj.cls_model_name}', class_obj=obj)
