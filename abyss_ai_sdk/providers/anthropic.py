from anthropic import Anthropic, AuthenticationError, RateLimitError
from ..types import AskOptions, AskResult
from ..errors import AbyssAuthError, AbyssRateLimitError, AbyssProviderError
from typing import Callable

def anthropic_ask(api_key: str, model: str, options: AskOptions, parse: Callable) -> AskResult:
    try:
        client = Anthropic(api_key=api_key)

        kwargs = dict(
            model=model,
            max_tokens=options.max_tokens,
            messages=[{"role": "user", "content": options.prompt}],
        )
        if options.system:
            kwargs["system"] = options.system
        if options.temperature is not None:
            kwargs["temperature"] = options.temperature

        res = client.messages.create(**kwargs)
        raw = next((b.text for b in res.content if b.type == "text"), "")

        return AskResult(data=parse(raw), raw=raw, provider="anthropic", model=model)

    except AuthenticationError as e:
        raise AbyssAuthError(str(e), provider="anthropic")
    except RateLimitError as e:
        raise AbyssRateLimitError(str(e), provider="anthropic")
    except Exception as e:
        raise AbyssProviderError(str(e), provider="anthropic")

def anthropic_stream(api_key: str, model: str, options: AskOptions):
    try:
        client = Anthropic(api_key=api_key)

        kwargs = dict(
            model=model,
            max_tokens=options.max_tokens,
            messages=[{"role": "user", "content": options.prompt}],
            stream=True,
        )
        if options.system:
            kwargs["system"] = options.system

        with client.messages.stream(**kwargs) as s:
            for text in s.text_stream:
                yield text

    except AuthenticationError as e:
        raise AbyssAuthError(str(e), provider="anthropic")
    except RateLimitError as e:
        raise AbyssRateLimitError(str(e), provider="anthropic")
    except Exception as e:
        raise AbyssProviderError(str(e), provider="anthropic")
    