from __future__ import annotations
import json
from openai import OpenAI
from app.config import OPENAI_API_KEY, CHAT_MODEL
from app.schemas import ArchiveMatch

_client = OpenAI(api_key=OPENAI_API_KEY)

_SYSTEM = """You are evaluating whether a 1973-era archive fragment emotionally resonates
with what a user could not say.

You will receive:
- USER_TEXT: the raw unspoken thing
- INTERPRETED THEME: a structured analysis of the emotional axes already computed
- ARCHIVE_FRAGMENT: a passage from a 1973-era unsent letter

Your job is to score the emotional resonance on three axes:

1. VALENCE — Does the archive fragment share emotional direction with the user?
   (tender longing vs. bitter resignation = MISMATCH)

2. TIME ORIENTATION — Does the archive fragment share the temporal nature of the unsaid thing?
   (past irreversible ≠ present still possible)

3. RELATIONAL DIRECTION — Is the archive fragment addressed to a similar relational target?
   (romantic partner ≠ parent ≠ self)

Use the INTERPRETED THEME axes to anchor your judgment — do not re-derive them.

Return JSON only:
{
  "score": <integer 1-10>,
  "reasoning": "<one sentence>"
}

Scoring:
- 9-10: Strong resonance across all three axes
- 7-8: Resonance on at least 2 axes; one minor divergence acceptable
- 5-6: Surface overlap but emotional axes diverge
- 1-4: No resonance

Be strict. 7 = "good enough to pair." Below 7 = retry."""


def evaluate_match(user_text: str, match: ArchiveMatch, theme: dict) -> dict:
    """Returns {"score": int, "reasoning": str}."""
    theme_block = (
        f"- Valence: {theme.get('valence', 'unknown')}\n"
        f"- Time orientation: {theme.get('time_orientation', 'unknown')}\n"
        f"- Relational direction: {theme.get('relational_direction', 'unknown')}\n"
        f"- Theme description: {theme.get('search_query', user_text)}"
    )

    user_message = (
        f'USER_TEXT:\n"""\n{user_text}\n"""\n\n'
        f'INTERPRETED THEME:\n{theme_block}\n\n'
        f'ARCHIVE_FRAGMENT:\n"""\n{match.text}\n'
        f'Context: {match.context}, {match.year}\n"""\n\n'
        "Score the emotional resonance. Return JSON only."
    )

    response = _client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
        max_tokens=150,
    )

    try:
        result = json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, IndexError):
        return {"score": 5, "reasoning": "parse error"}

    score = result.get("score", 5)
    if not isinstance(score, (int, float)) or not (1 <= int(score) <= 10):
        score = 5

    return {"score": int(score), "reasoning": result.get("reasoning", "")}


def select_best_match(
    user_text: str,
    theme: dict,
    candidates: list[ArchiveMatch],
    threshold: int,
) -> tuple[ArchiveMatch, list[dict], int]:
    """
    Evaluates candidates[0] with theme context.
    If score < threshold, evaluates candidates[1] and picks the higher scorer.
    Hard cap: 1 retry.
    Returns (selected_match, eval_history, final_score).
    """
    first = candidates[0]
    first_eval = evaluate_match(user_text, first, theme)
    history = [{"id": first.id, **first_eval}]

    if first_eval["score"] >= threshold or len(candidates) < 2:
        return first, history, first_eval["score"]

    second = candidates[1]
    second_eval = evaluate_match(user_text, second, theme)
    history.append({"id": second.id, **second_eval})

    if second_eval["score"] > first_eval["score"]:
        return second, history, second_eval["score"]

    return first, history, first_eval["score"]
