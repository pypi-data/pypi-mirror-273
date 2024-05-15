# llmprototyping

`llmprototyping` is a Python package designed to provide easy and uniform access to various large language model (LLM) and embedding APIs, along with basic functionality for building small-scale artificial intelligence applications.

## Features

- **Uniform API Access**: Simplify your interactions with different LLM and embedding APIs using a single interface.
- **Basic AI Application Tools**: Get started quickly with tools designed to support the development of AI applications.

## License

Apache License Version 2.0

## Compatibility

python 3.9+

## Installation

```bash
pip install llmprototyping
```

## Available models

### chat completion models

- groq/llama3-70b-8192
- groq/llama3-8b-8192
- groq/mixtral-8x7b-32768
- groq/gemma-7b-it
- openai/gpt-4o
- openai/gpt-4-turbo
- openai/gpt-4-turbo-preview
- openai/gpt-3.5-turbo
- anthropic/claude-3-opus-20240229
- anthropic/claude-3-sonnet-20240229
- anthropic/claude-3-haiku-20240307
- ollama/*

### embedding models

- openai/text-embedding-3-small
- openai/text-embedding-3-large
- openai/text-embedding-ada-002
- ollama/*

## Usage

Note: The examples use python-dotenv. This is not required by llmprototyping, so it needs to be installed separatedly. 

### Simple chat completion call

```python
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

import llmprototyping as llmp
factory = llmp.LLMChatCompletionFactory
model = factory.build('groq/llama3-70b-8192', {'api_key': groq_api_key})
user_msg = llmp.Message(content="Please give me a list of ten colours and some place that is related to each one.")
sys_msg = llmp.Message(content="Provide an answer in json", role="system")
resp = model.query([user_msg,sys_msg], json_response=True, temperature=0)
resp.show()
```

<details>
  <summary>Output</summary>

```
Response successful; tokens: i:43 o:145 message:
Message role:assistant content:
{
"colours": [
{"colour": "Red", "place": "Rome"},
{"colour": "Orange", "place": "Netherlands"},
{"colour": "Yellow", "place": "Sunshine Coast"},
{"colour": "Green", "place": "Emerald Isle"},
{"colour": "Blue", "place": "Blue Mountains"},
{"colour": "Indigo", "place": "Indigo Bay"},
{"colour": "Violet", "place": "Violet Hill"},
{"colour": "Pink", "place": "Pink Sands Beach"},
{"colour": "Brown", "place": "Brown County"},
{"colour": "Grey", "place": "Greytown"}
]
}
```
</details>

### List available models

```python
import llmprototyping as llmp

print('chat completion models:')
for model_name in llmp.LLMChatCompletionFactory.available_models:
    print(f"  {model_name}")

print('embedding models:')
for model_name in llmp.EmbeddingComputerFactory.available_models:
    print(f"  {model_name}")
```

### Embeddings example: search

```python
knowledge_list = [
    "Rome was founded in 753 BCE according to tradition, by Romulus and Remus.",
    "The Roman Republic was established in 509 BCE after overthrowing the last Etruscan kings.",
    "Julius Caesar became the perpetual dictator in 44 BCE, shortly before his assassination.",
    "The Roman Empire officially began when Octavian received the title of Augustus in 27 BCE.",
    "At its peak, the Roman Empire extended from Hispania to Mesopotamia.",
    "The capital of the Empire was moved to Constantinople by Constantine I in 330.",
    "The fall of Rome occurred in 476 CE when the last Western Roman emperor, Romulus Augustulus, was deposed.",
    "Roman culture greatly influenced law, politics, language, and architecture in the Western world.",
    "The expansion of Christianity as the official religion was promoted by Constantine after the Battle of the Milvian Bridge in 312.",
    "Roman society was heavily stratified between patricians, plebeians, and slaves."
]

question = "What is the name of the last emperor?"

import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

import llmprototyping as llmp

import shelve
db = shelve.open('test_embeddings.db')

def get_embedding(text, computer):
    if text in db:
        json = db[text]
        return llmp.EmbeddingVector.from_json(json)

    print(f'computing embedding for "{text}"')
    em = computer.get_embedding(text)
    db[text] = em.to_json()

    return em

factory = llmp.EmbeddingComputerFactory
computer = factory.build('openai/text-embedding-3-small', {'api_key': openai_api_key})        

entry_table = dict()

for entry_id, entry_text in enumerate(knowledge_list):
    em = get_embedding(entry_text, computer)
    entry_table[entry_id] = em

em_question = get_embedding(question, computer)

vdb = llmp.FAISSDatabase(embedding_type=computer.model_name, embedding_size=computer.vector_size)
vdb.put_records(entry_table)

print(f"query: {question}")
results = vdb.search(em_question)
for distance, entry_id in results:
    print(f"{distance:.3f} {entry_id} {knowledge_list[entry_id]}")
```

<details>
  <summary>Output</summary>

```
computing embedding for "What is the name of the last emperor?"
query: What is the name of the last emperor?
1.105 6 The fall of Rome occurred in 476 CE when the last Western Roman emperor, Romulus Augustulus, was deposed.
1.337 2 Julius Caesar became the perpetual dictator in 44 BCE, shortly before his assassination.
1.457 3 The Roman Empire officially began when Octavian received the title of Augustus in 27 BCE.
1.522 5 The capital of the Empire was moved to Constantinople by Constantine I in 330.
1.559 1 The Roman Republic was established in 509 BCE after overthrowing the last Etruscan kings.
```

Values for distances may vary depending on the actual embeddings computed.
</details>

### Ollama example: chat

OLLAMA_HOST is the uri of the host, e.g. http://192.168.1.2:11434

It requires a call to ollama_discover to register the models in the server

ollama_pull can be used to pull a model

```python
import os
from dotenv import load_dotenv
load_dotenv()

ollama_host = os.getenv('OLLAMA_HOST')

import llmprototyping as llmp

llmp.ollama_discover(host=ollama_host)
llmp.ollama_pull_model(host=ollama_host, model_name='phi3')

print('chat completion models:')
for model_name in llmp.LLMChatCompletionFactory.available_models:
    print(f"  {model_name}")
print()

factory = llmp.LLMChatCompletionFactory
model = factory.build('ollama/phi3')
user_msg = llmp.Message(content="Please give me a list of ten colours and some place that is related to each one.")
sys_msg = llmp.Message(content="Provide an answer in json", role="system")
resp = model.query([user_msg,sys_msg], json_response=True, temperature=0)

resp.show_header()
print(resp.message.content)
```

<details>
  <summary>Output</summary>

```
chat completion models:
  groq/llama3-70b-8192
  groq/llama3-8b-8192
  groq/mixtral-8x7b-32768
  groq/gemma-7b-it
  openai/gpt-4o
  openai/gpt-4-turbo
  openai/gpt-4-turbo-preview
  openai/gpt-3.5-turbo
  anthropic/claude-3-opus-20240229
  anthropic/claude-3-sonnet-20240229
  anthropic/claude-3-haiku-20240307
  ollama/phi3:latest
  ollama/phi3

Response successful; tokens: i:40 o:189
{
  "Colours": [
    {"Red": "The Eiffel Tower, Paris"},
    {"Blue": "Pacific Ocean near Hawaii"},
    {"Green": "Yellowstone National Park, USA"},
    {"Orange": "Sunset at the Grand Canyon, Arizona"},
    {"White": "Mt. Everest Base Camp, Nepal"},
    {"Black": "The Great Barrier Reef, Australia (night diving)"},
    {"Purple": "Royal Palace of Caserta, Italy"},
    {"Gray": "Snowy landscapes in the Swiss Alps"},
    {"Brown": "Amazon Rainforest, Brazil"},
    {"Yellow": "Kilimanjaro's snow-capped peak, Tanzania"}
  ]
}
```
</details>

### Templates example

Write templates.txt file:
```
# template: question_yesno_json_sys
# role: system

Answer the question with any of these responses: yes, no, unknown, ambiguous.
Respond in json using this schema:
{ "answer": "..." }

# template: question_yesno_user
# role: user

{{question}}

# template: extract_keywords_json_sys
# role: system

Extract keywords from the provided text.
Respond in json using this schema:
{ "keywords": ["keyword1", "keyword2", ...] }
```

Use it in code:

```python
import llmprototyping as llmp

template_repo = llmp.TemplateFileRepository("templates.txt")
msg_sys = template_repo.render_message('question_yesno_json_sys', {})
msg_user = template_repo.render_message('question_yesno_user', {"question": "Is 1+1 = 2?"})

# model is an LLMChatCompletion object, see examples above
resp = model.query([msg_sys,msg_text], json_response=True)
```

