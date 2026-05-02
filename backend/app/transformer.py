from __future__ import annotations
from openai import OpenAI, AsyncOpenAI
from app.config import OPENAI_API_KEY, CHAT_MODEL, LYRIC_MODEL
from app.schemas import ArchiveMatch
from app.prompts import SYSTEM_PROMPT

_client = OpenAI(api_key=OPENAI_API_KEY)
_async_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


def _build_messages(user_text: str, matches: list[ArchiveMatch]) -> list[dict]:
    top_match = matches[0]
    user_message = (
        f'Unspoken text:\n"""\n{user_text}\n"""\n\n'
        f'1973 resonance (atmosphere only — do not quote):\n"""\n'
        f'{top_match.text}\nContext: {top_match.context}, {top_match.year}\n"""'
        '\n\nWrite the lyric.'
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_message},
    ]


def generate_lyric(user_text: str, matches: list[ArchiveMatch]) -> str:
    messages = _build_messages(user_text, matches)
    response = _client.chat.completions.create(
        model=LYRIC_MODEL,
        messages=messages,
    )
    return response.choices[0].message.content.strip()


async def stream_lyric_tokens(user_text: str, matches: list[ArchiveMatch]):
    messages = _build_messages(user_text, matches)
    stream = await _async_client.chat.completions.create(
        model=LYRIC_MODEL,
        messages=messages,
        stream=True,
    )
    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
