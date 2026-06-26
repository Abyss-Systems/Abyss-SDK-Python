from groq import Groq, AuthenticationError, RateLimitError
from ..types import AskOptions, AskResult
from ..errors import AbyssAuthError, AbyssRateLimitError, AbyssProviderError
from typing import Callable

def groq_ask(api_key: str, model: str, options: AskOptions, parse: Callable) -> AskResult:
    try:
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

    except AuthenticationError as e:
        raise AbyssAuthError(str(e), provider="groq")
    except RateLimitError as e:
        raise AbyssRateLimitError(str(e), provider="groq")
    except Exception as e:
        raise AbyssProviderError(str(e), provider="groq")

def groq_stream(api_key: str, model: str, options: AskOptions):
    try:
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

    except AuthenticationError as e:
        raise AbyssAuthError(str(e), provider="groq")
    except RateLimitError as e:
        raise AbyssRateLimitError(str(e), provider="groq")
    except Exception as e:
        raise AbyssProviderError(str(e), provider="groq")
    