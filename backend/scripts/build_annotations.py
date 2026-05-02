"""
One-time script: generate a 1973-archivist-style annotation for each archive entry,
matching the style produced at runtime by theme_interpreter for user inputs.

The generated annotations are embedded by build_embeddings.py instead of raw text.
This puts queries and archive entries in the same stylistic embedding space (HyDE fix).
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parents[1] / ".env")

DATA_DIR = Path(__file__).parents[1] / "data"
ARCHIVE_JSON = DATA_DIR / "seed_archive.json"
OUTPUT_JSON = DATA_DIR / "archive_annotations.json"
CHAT_MODEL = "gpt-4o-mini"

SYSTEM = """You are a 1973-era archivist annotating an unsent letter or reflection.
You will receive the letter's text and its context.

Write a 2-3 sentence annotation describing:
- WHAT was unsaid (the emotional content)
- TO WHOM (the relational target)
- WHY it could not be said (the obstacle)
- WHETHER the chance still exists (temporal status)

The annotation must be in the SAME register a librarian would use to describe the
emotional content of an unsent letter for a finding aid. Terse, humanistic, not clinical.

Do NOT quote the letter. Do NOT use the letter's specific words.
Write only the annotation. No prefix, no commentary.

Example annotation: "A son who held his admiration for his father in silence until
the chance was gone. The words of pride were never spoken. The door closed permanently."
"""


def annotate(client: OpenAI, entry: dict) -> str:
    user_msg = (
        f'Letter:\n"""\n{entry["text"]}\n"""\n\n'
        f'Context: {entry["context"]}, {entry["year"]}\n'
        f'Source type: {entry["source_type"]}'
    )
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.4,
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit("OPENAI_API_KEY not set.")
    client = OpenAI(api_key=api_key)

    entries = json.loads(ARCHIVE_JSON.read_text(encoding="utf-8"))
    print(f"Annotating {len(entries)} entries…")

    annotations: dict[str, str] = {}
    for i, entry in enumerate(entries, 1):
        ann = annotate(client, entry)
        annotations[entry["id"]] = ann
        print(f"  [{i}/{len(entries)}] {entry['id']}: {ann[:80]}…")

    OUTPUT_JSON.write_text(
        json.dumps(annotations, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nSaved {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
