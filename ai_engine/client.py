"""
LLM client configuration for OpenRouter via LangChain.
"""
import logging

from django.conf import settings
from langchain_openai import ChatOpenAI

logger = logging.getLogger('ai_engine')


def get_llm(
    temperature: float | None = None,
    max_tokens: int | None = None,
    model: str | None = None,
) -> ChatOpenAI:
    """
    Returns a configured ChatOpenAI instance pointing at OpenRouter.

    Args:
        temperature: Sampling temperature (0.0 - 1.0). Defaults to settings.AI_TEMPERATURE.
        max_tokens: Maximum tokens in response. Defaults to settings.AI_MAX_TOKENS.
        model: Model identifier. Defaults to settings.AI_MODEL.

    Returns:
        A ChatOpenAI instance configured for OpenRouter.
    """
    _model = model or getattr(settings, 'AI_MODEL', 'google/gemini-2.0-flash-001')
    _temperature = temperature if temperature is not None else getattr(settings, 'AI_TEMPERATURE', 0.7)
    _max_tokens = max_tokens or getattr(settings, 'AI_MAX_TOKENS', 4096)
    _api_key = getattr(settings, 'OPENROUTER_API_KEY', '')
    _base_url = getattr(settings, 'OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')

    if not _api_key:
        logger.warning("OPENROUTER_API_KEY is not set. AI features will not work.")

    llm = ChatOpenAI(
        model=_model,
        temperature=_temperature,
        max_tokens=_max_tokens,
        api_key=_api_key,
        base_url=_base_url,
        default_headers={
            "HTTP-Referer": "https://travel-advisor-agent.local",
            "X-Title": "Travel Advisor Agent",
        },
    )

    logger.info(f"LLM client initialized: model={_model}, temp={_temperature}")
    return llm
