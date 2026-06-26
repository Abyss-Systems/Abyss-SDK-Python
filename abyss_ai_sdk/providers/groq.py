from groq import Groq
from ..types import AskOptions, AskResult
from typing import Any, Callable, AsyncIterator

def groq_ask(api_key: str, model: str, options: AskOptions, parse: Callable) -> AskResult:
    client = Groq(api_key=api_key)

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

    return AskResult(data=parse(raw), raw=raw, provider="groq", model=model)

def groq_stream(api_key: str, model: str, options: AskOptions):
    client = Groq(api_key=api_key)

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
