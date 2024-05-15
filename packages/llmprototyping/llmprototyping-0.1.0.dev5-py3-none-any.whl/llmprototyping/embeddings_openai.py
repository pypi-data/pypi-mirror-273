from openai import OpenAI
import inspect
from .embeddings_interface import EmbeddingComputer, EmbeddingComputerFactory, EmbeddingVector

try:
    import tiktoken
    def _num_tokens_from_string(string: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
except ImportError:
    def _num_tokens_from_string(string: str, encoding_name: str) -> int:
        raise NotImplemented()

class OpenAIEmbeddingComputer(EmbeddingComputer):
    @property
    def model_name(self):
        return self._model_name

    @property
    def comparison_method(self):
        return self._comparison_method

    @property
    def max_digest_size(self):
        return self._max_digest_size

    def compute_tokens(self, text):
        return _num_tokens_from_string(text, "cl100k_base")

    @property
    def vector_size(self):
        return self._vector_size

    @classmethod
    def from_dict(cls, data):
        return OpenAIEmbeddingComputer(api_key=data['api_key'],
                                       model_name=cls.cls_model_name,
                                       max_digest_size=cls.cls_max_digest_size,
                                       vector_size=cls.cls_vector_size,
                                       comparison_method=cls.cls_comparison_method)

    @staticmethod
    def get_computer_name(model_name):
        return f"openai/{model_name}"

    def get_embedding(self, text):
        text = text.replace("\n", " ").strip()
        v = self._client.embeddings.create(input=text, model=self.model_name).data[0].embedding
        if len(v) != self.vector_size:
            raise Exception(f"vector size mismatch; expected:{self.vector_size} got:{len(v)}")
        return EmbeddingVector(v, self.get_computer_name(self.model_name))

    def __init__(self, api_key, model_name, max_digest_size, vector_size, comparison_method):
        self._model_name = model_name
        self._client = OpenAI(api_key=api_key)
        self._max_digest_size = max_digest_size
        self._vector_size = vector_size
        self._comparison_method = comparison_method

class OpenAI_Text_Embedding_3_Small(OpenAIEmbeddingComputer):
    cls_model_name = 'text-embedding-3-small'
    cls_max_digest_size = 8191
    cls_vector_size = 1536
    cls_comparison_method = "cosine_similarity"

class OpenAI_Text_Embedding_3_Large(OpenAIEmbeddingComputer):
    cls_model_name = 'text-embedding-3-large'
    cls_max_digest_size = 8191
    cls_vector_size = 3072
    cls_comparison_method = "cosine_similarity"

class OpenAI_Text_Embedding_Ada_002(OpenAIEmbeddingComputer):
    cls_model_name = 'text-embedding-ada-002'
    cls_max_digest_size = 8191
    cls_vector_size = 1536
    cls_comparison_method = "cosine_similarity"

def init():
    for obj in globals().values():            
        if inspect.isclass(obj) and issubclass(obj, OpenAIEmbeddingComputer) and hasattr(obj,'cls_model_name'):
            name = OpenAIEmbeddingComputer.get_computer_name(obj.cls_model_name)
            EmbeddingComputerFactory.register(name=name, class_obj=obj)
