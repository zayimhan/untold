from __future__ import annotations
import json
from openai import OpenAI
from app.config import OPENAI_API_KEY, CHAT_MODEL

_client = OpenAI(api_key=OPENAI_API_KEY)

_SYSTEM = """You analyze what a person could not say and extract its emotional essence
for archival matching against 1973-era unsent letters.

Return a JSON object with exactly these fields:

{
  "search_query": "<2-3 sentences written as a 1973 archivist's annotation: what was NOT said, to whom, why it mattered, and whether the chance still exists. Terse and humanistic, not clinical. This becomes the text that is embedded for semantic search.>",
  "valence": "<one of: tender_longing | bitter_regret | quiet_grief | unspoken_love | deferred_forgiveness | suppressed_anger | unacknowledged_pride | unspoken_farewell>",
  "time_orientation": "<one of: past_irreversible | past_regrettable | present_possible | future_feared>",
  "relational_direction": "<one of: romantic_partner | parent | child | friend | sibling | self | stranger | colleague>"
}

The search_query is the most important field. It should read like something that could appear
in a 1973 letter collection annotation — the kind of sentence a librarian would write
to describe the emotional content of an unsent letter.

Example input: "i never told my dad i was proud of him before he died"
Example output:
{
  "search_query": "A son who held his admiration for his father in silence until the chance was gone. The words of pride and love were never spoken. The door closed permanently.",
  "valence": "unacknowledged_pride",
  "time_orientation": "past_irreversible",
  "relational_direction": "parent"
}"""


def interpret_theme(user_text: str) -> dict:
    """
    Returns:
    {
        "search_query": str,
        "valence": str,
        "time_orientation": str,
        "relational_direction": str,
    }
    Falls back to raw user_text on parse failure.
    """
    response = _client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": f'Unspoken text:\n"""\n{user_text}\n"""'},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
        max_tokens=350,
    )

    try:
        result = json.loads(response.choices[0].message.content)
        return {
            "search_query": result.get("search_query") or user_text,
            "valence": result.get("valence", "unknown"),
            "time_orientation": result.get("time_orientation", "unknown"),
            "relational_direction": result.get("relational_direction", "unknown"),
        }
    except (json.JSONDecodeError, IndexError, KeyError):
        return {
            "search_query": user_text,
            "valence": "unknown",
            "time_orientation": "unknown",
            "relational_direction": "unknown",
        }
