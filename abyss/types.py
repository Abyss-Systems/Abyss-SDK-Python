from typing import Any, Generic, Literal, TypeVar
from pydantic import BaseModel

Provider = Literal["groq", "openai", "anthropic"]

T = TypeVar("T")

class AbyssConfig(BaseModel):
  provider: Provider
  api_key: str
  model: str | None = None

class AskOptions(BaseModel, Generic[T]):
  prompt: str
  system: str | None = None
  schema: type[T] | None = None
  temperature: float = 0.7
  max_tokens: int = 1024

class AskResult(BaseModel, Generic[T]):
  data: T
  raw: str
  provider: Provider
  model: str

class EmbedOptions(BaseModel):
  input: str | list[str]
  model: str | None = None

class EmbedResult(BaseModel):
  embeddings: list[list[float]]
  model: str
  provider: Provider
