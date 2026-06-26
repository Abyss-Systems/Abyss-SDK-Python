class AbyssError(Exception):
  """Base error for abyss-ai-sdk."""
  def __init__(self, message: str, provider: str | None = None):
    self.provider = provider
    super().__init__(f"[{provider}] {message}" if provider else message)

class AbyssAuthError(AbyssError):
  """Invalid or missing API key."""
  pass

class AbyssRateLimitError(AbyssError):
  """Rate limit hit."""
  pass

class AbyssTimeoutError(AbyssError):
  """Request timed out."""
  pass

class AbyssProviderError(AbyssError):
  """Generic provider error."""
  def __init__(self, message: str, provider: str | None = None, status_code: int | None = None):
    self.status_code = status_code
    super().__init__(message, provider)

class AbyssSchemaError(AbyssError):
  """Structured response failed schema validation."""
  pass
