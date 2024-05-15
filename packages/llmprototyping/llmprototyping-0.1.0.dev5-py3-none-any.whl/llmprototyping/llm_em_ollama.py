from typing import List
import inspect
import ollama
from .llm_interface import LLMChatCompletion, LLMChatCompletionFactory, Message, Response
from .embeddings_interface import EmbeddingComputer, EmbeddingComputerFactory, EmbeddingVector
from .error import LLMPException

class OLlamaEmbeddingComputer(EmbeddingComputer):
    @property
    def model_name(self):
        return self._model_name

    @property
    def comparison_method(self):
        return self._comparison_method

    @property
    def max_digest_size(self):
        raise NotImplemented()

    def compute_tokens(self, text):
        raise NotImplemented()

    @property
    def vector_size(self):
        return self._vector_size

    @classmethod
    def from_dict(cls, data):
        return OLlamaEmbeddingComputer(host=cls.cls_host,
                                       model_name=cls.cls_model_name,
                                       ollama_model_name=cls.cls_ollama_model_name,
                                       vector_size=cls.cls_vector_size,
                                       comparison_method=cls.cls_comparison_method)

    @staticmethod
    def get_computer_name(model_name):
        return f"ollama/{model_name}"

    def get_embedding(self, text):
        text = text.replace("\n", " ").strip()
        try:
            resp = self._client.embeddings(prompt=text, model=self._ollama_model_name)
        except ollama.ResponseError as e:
            raise LLMPException(e.status_code, e.error, True)
        except Exception as e:
            raise LLMPException("exception", e, False)

        if 'embedding' not in resp:
            raise LLMPException("unexpected response", resp, False)
        v = resp.get('embedding',[])
        if len(v) != self.vector_size:
            raise LLMPException("vector size mismatch", f"vector size mismatch; expected:{self.vector_size} got:{len(v)}", False)
        return EmbeddingVector(v, self.get_computer_name(self.model_name))

    def __init__(self, host, model_name, vector_size, comparison_method, ollama_model_name):
        self._model_name = model_name
        self._client = ollama.Client(host=host)
        self._vector_size = vector_size
        self._comparison_method = comparison_method
        self._ollama_model_name = ollama_model_name

class LLMOLlamaChatCompletion(LLMChatCompletion):
    def __init__(self, host, model_name, model_details, ollama_model_name):
        self.model_name = model_name
        self.model_details = model_details
        self._ollama_model_name = ollama_model_name
        self._client = ollama.Client(host=host)

    @property
    def context_size(self):
        raise NotImplemented()

    def query(self, messages:List[Message], json_response=False, temperature=1.0):
        if not isinstance(temperature,float) and not isinstance(temperature,int):
            raise LLMPException.param_error("temperature must be a float")

        try:
            rformat = 'json' if json_response else ''
            r = self._client.chat(
                messages = [m.to_dict() for m in messages],
                model = self._ollama_model_name,
                options = {'temperature': temperature},
                format = rformat,
            )
            rcontent = r['message']['content']
            rrole = r['message']['role']
            msg = Message(content=rcontent, role=rrole)
            input_tokens = r['prompt_eval_count']
            output_tokens = r['eval_count']
            response = Response(message=msg, input_token_count=input_tokens, output_token_count=output_tokens)
        except ollama.ResponseError as e:
            response = Response.error_response(status_code = e.status_code, error = e.error)
        except Exception as e:
            response = Response.error_response(status_code = "exception", error = e)

        return response

    @classmethod
    def from_dict(cls, data):
        return cls(model_name=cls.cls_model_name, host=cls.cls_host, ollama_model_name=cls.cls_ollama_model_name, model_details = cls.cls_model_details)

_class_counter = 1
def _register(factory, model_name, base_class, attrs):
    global _class_counter
    class_name = f'ollama_model_{_class_counter}'
    _class_counter += 1
    model_class = type(class_name, (base_class,), attrs)
    alias = None
    if model_name.count(':') == 1:
        nm, ver = model_name.split(':')
        if ver == 'latest':
            alias = nm
    factory.register(name=model_name, class_obj=model_class, alias=alias)

def _process_llm(client, host, model_details):
    model_name = f'ollama/{model_details["name"]}'
    if LLMChatCompletionFactory.model_registered(model_name):
        return False

    try:
        client.chat(model=model_details["name"], messages=[])
    except ollama.ResponseError:
        # model not capable of chat
        return True

    attrs = {
        'cls_model_name': model_name,
        'cls_model_details': model_details,
        'cls_host': host,
        'cls_ollama_model_name': model_details["name"]
    }
    _register(LLMChatCompletionFactory, model_name, LLMOLlamaChatCompletion, attrs)
    return False

def _process_em(client, host, model_details):
    model_name = f'ollama/{model_details["name"]}'
    if EmbeddingComputerFactory.model_registered(model_name):
        return

    try:
        resp = client.embeddings(model=model_details["name"], prompt='a')
    except ollama.ResponseError:
        # model not capable of embeddings
        return
    try:
        vector_size = len(resp['embedding'])
    except KeyError:
        return
    if vector_size == 0:
        return

    attrs = {
        'cls_model_name': model_name,
        'cls_model_details': model_details,
        'cls_host': host,
        'cls_vector_size': vector_size,
        'cls_comparison_method': 'unknown',
        'cls_ollama_model_name': model_details["name"]
    }
    _register(EmbeddingComputerFactory, model_name, OLlamaEmbeddingComputer, attrs)

def discover(host):
    global _class_counter

    client = ollama.Client(host=host)
    for model in client.list()['models']:
        if _process_llm(client, host, model):
            _process_em(client, host, model)

def pull_model(host, model_name):
    try:
        client = ollama.Client(host=host)
        resp = client.pull(model_name)
        if resp.get('status') == 'success':
            discover(host)
            return True
    except:
        return False


def init():
    pass
