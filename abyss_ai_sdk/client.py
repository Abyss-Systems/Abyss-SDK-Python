import json
from .types import AbyssConfig, AskOptions, AskResult, EmbedOptions, EmbedResult
from .providers.groq import groq_ask, groq_stream
from .providers.openai import openai_ask, openai_stream, openai_embed
from .providers.anthropic import anthropic_ask, anthropic_stream
from .errors import AbyssSchemaError

DEFAULT_MODELS = {
    "groq": "llama-3.1-8b-instant",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-sonnet-4-6",
}

def _build_system(schema_cls, base: str | None) -> str | None:
    parts = []
    if base:
        parts.append(base)
    if schema_cls:
        parts.append("Respond ONLY with a valid JSON object. No markdown, no explanation, just raw JSON.")
        parts.append(f"Schema fields: {list(schema_cls.model_fields.keys())}")
    return "\n\n".join(parts) if parts else None

def _parse_structured(raw: str, schema_cls):
    try:
        cleaned = raw.replace("```json", "").replace("```", "").strip()
        return schema_cls.model_validate_json(cleaned)
    except Exception as e:
        raise AbyssSchemaError(f"Failed to parse structured response: {e}")

def ask(config: AbyssConfig, options: AskOptions) -> AskResult:
    model = config.model or DEFAULT_MODELS[config.provider]
    system = _build_system(options.schema, options.system)
    opts = options.model_copy(update={"system": system})

    def parse(raw: str):
        if options.schema:
            return _parse_structured(raw, options.schema)
        return raw

    match config.provider:
        case "groq":
            return groq_ask(config.api_key, model, opts, parse)
        case "openai":
            return openai_ask(config.api_key, model, opts, parse)
        case "anthropic":
            return anthropic_ask(config.api_key, model, opts, parse)
        case _:
            raise ValueError(f"Unknown provider: {config.provider}")

def stream(config: AbyssConfig, options: AskOptions):
    model = config.model or DEFAULT_MODELS[config.provider]

    match config.provider:
        case "groq":
            yield from groq_stream(config.api_key, model, options)
        case "openai":
            yield from openai_stream(config.api_key, model, options)
        case "anthropic":
            yield from anthropic_stream(config.api_key, model, options)
        case _:
            raise ValueError(f"Unknown provider: {config.provider}")

def embed(config: AbyssConfig, options: EmbedOptions) -> EmbedResult:
    if config.provider != "openai":
        raise ValueError("Embeddings only supported with provider 'openai'.")
    return openai_embed(config.api_key, options)

class AbyssClient:
    def __init__(self, config: AbyssConfig):
        self.config = config

    def ask(self, options: AskOptions) -> AskResult:
        return ask(self.config, options)

    def stream(self, options: AskOptions):
        yield from stream(self.config, options)

    def embed(self, options: EmbedOptions) -> EmbedResult:
        return embed(self.config, options)

def create_client(provider: str, api_key: str, model: str | None = None) -> AbyssClient:
    config = AbyssConfig(provider=provider, api_key=api_key, model=model)
    return AbyssClient(config)
