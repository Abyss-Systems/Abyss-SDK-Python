# abyss-ai-sdk (Python)

Multi-provider AI utility with structured responses and streaming. Supports Groq, OpenAI, and Anthropic with a unified API.

## Install

```bash
pip install abyss-ai-sdk
```

## Usage

### `create_client()` - recommended

```python
from abyss_ai_sdk import create_client, AskOptions
from pydantic import BaseModel

ai = create_client(provider="groq/openai/anthropic", api_key="your_api_key")

# Plain text
res = ai.ask(AskOptions(prompt="Say hello in one sentence."))
print(res.data)

# Structured
class Sentiment(BaseModel):
  sentiment: str
  confidence: float
  summary: str

res = ai.ask(AskOptions(
  prompt="Analyse: 'I love this product!'",
  schema=Sentiment,
))
print(res.data.sentiment)
print(res.data.confidence)

# Streaming
for chunk in ai.stream(AskOptions(prompt="Tell me a story.")):
  print(chunk, end="", flush=True)
```

### Embeddings (OpenAI only)

```python
from abyss_ai_sdk import create_client, EmbedOptions

ai = create_client(provider="openai", api_key="your_openai_key")

res = ai.embed(EmbedOptions(input=["cat", "dog"]))
print(len(res.embeddings[0]))  # 1536
```

### One-off calls

```python
from abyss_ai_sdk import ask, stream, AskOptions
from abyss_ai_sdk import AbyssConfig

config = AbyssConfig(provider="groq", api_key="your_groq_key")

res = ask(config, AskOptions(prompt="What is 2 + 2?"))
print(res.data)
```

## Providers

## Providers

| Provider | Default Model |
|---|---|
| `groq` | `llama-3.1-8b-instant` |
| `openai` | `gpt-4o-mini` |
| `anthropic` | `claude-sonnet-4-6` |

Override the model:

```python
ai = create_client(provider="groq/openai/anthropic", api_key="api_key", model="model_of_your_choice")
```

## API

### `create_client(provider, api_key, model=None)`

Returns an `AbyssClient` with `.ask()`, `.stream()`, and `.embed()`.

### `AskOptions`

| Field | Type | Description |
|---|---|---|
|`prompt`|`str`|The user message|
|`system`|`str \| None`|System prompt|
|`schema`|`BaseModel \| None`|Pydantic model for structured output|
|`temperature`|`float`|Default 0.7|
|`max_tokens`|`int`|Default 1024|

### `EmbedOptions`

|Field|Type|Description|
|---|---|---|
|`input`|`str \| list[str]`|Text to embed|
|`model`|`str \| None`|Override default model|

## License

MIT