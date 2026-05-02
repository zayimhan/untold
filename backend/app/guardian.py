from __future__ import annotations
from openai import AsyncOpenAI
from app.config import OPENAI_API_KEY, CHAT_MODEL

_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

_SYSTEM = """You are a content safety filter for a creative writing app.
Does the following text contain profanity, hate speech, slurs, explicit sexual
content, graphic violence, or seriously offensive language in ANY language
(including Turkish, English, or others)?
Reply with exactly one word: BLOCKED or OK."""


async def is_inappropriate(text: str) -> bool:
    """Returns True if the input should be blocked."""
    response = await _client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user",   "content": text},
        ],
        max_tokens=5,
        temperature=0,
    )
    result = response.choices[0].message.content.strip().upper()
    return result == "BLOCKED"
