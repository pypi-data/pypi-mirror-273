from .llm_interface import Message, Response, LLMChatCompletionFactory, LLMChatCompletionCache
from .embeddings_interface import EmbeddingVector, EmbeddingComputerFactory
from .vectordb import FAISSDatabase
from .templates import Template, TemplateFileRepository
from .error import LLMPException

try:
    from .llm_groq import init as groq_llm_init
    groq_llm_init()
except ImportError:
    pass

try:
    from .llm_openai import init as openai_llm_init
    openai_llm_init()
except ImportError:
    pass

try:
    from .embeddings_openai import init as openai_emb_init
    openai_emb_init()
except ImportError:
    pass

try:
    from .llm_em_ollama import init as ollama_llm_init
    from .llm_em_ollama import pull_model as ollama_pull_model
    ollama_llm_init()
    from .llm_em_ollama import discover as ollama_discover
except ImportError:
    pass

try:
    from .llm_anthropic import init as anthropic_llm_init
    anthropic_llm_init()
except ImportError:
    pass