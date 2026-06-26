from openai import OpenAI
from ..types import AskOptions, AskResult, EmbedOptions, EmbedResult
from typing import Callable

def openai_ask(api_key: str, model: str, options: AskOptions, parse: Callable) -> AskResult:
    client = OpenAI(api_key=api_key)

    messages = []
    if options.system:
        messages.append({"role": "system", "content": options.system})
    messages.append({"role": "user", "content": options.prompt})

    res = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=options.temperature,
        max_tokens=options.max_tokens,
    )

    raw = res.choices[0].message.content or ""
    return AskResult(data=parse(raw), raw=raw, provider="openai", model=model)

def openai_stream(api_key: str, model: str, options: AskOptions):
    client = OpenAI(api_key=api_key)

    messages = []
    if options.system:
        messages.append({"role": "system", "content": options.system})
    messages.append({"role": "user", "content": options.prompt})

    res = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=options.temperature,
        max_tokens=options.max_tokens,
        stream=True,
    )

    for chunk in res:
        text = chunk.choices[0].delta.content
        if text:
            yield text

def openai_embed(api_key: str, options: EmbedOptions) -> EmbedResult:
    client = OpenAI(api_key=api_key)
    model = options.model or "text-embedding-3-small"

    input_list = options.input if isinstance(options.input, list) else [options.input]

    res = client.embeddings.create(model=model, input=input_list)

    return EmbedResult(
        embeddings=[d.embedding for d in res.data],
        model=model,
        provider="openai",
    )