"""Embed the archive annotations (not raw text) for symmetric retrieval."""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parents[1] / ".env")

DATA_DIR = Path(__file__).parents[1] / "data"
ARCHIVE_JSON = DATA_DIR / "seed_archive.json"
ANNOTATIONS_JSON = DATA_DIR / "archive_annotations.json"
OUTPUT_NPZ = DATA_DIR / "archive_embeddings.npz"
EMBEDDING_MODEL = "text-embedding-3-small"


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit("OPENAI_API_KEY not set.")
    if not ANNOTATIONS_JSON.exists():
        sys.exit("Run build_annotations.py first.")

    client = OpenAI(api_key=api_key)
    entries = json.loads(ARCHIVE_JSON.read_text(encoding="utf-8"))
    annotations = json.loads(ANNOTATIONS_JSON.read_text(encoding="utf-8"))

    print(f"Embedding {len(entries)} annotated entries…")

    vectors: list[list[float]] = []
    metadata: list[dict] = []

    for i, entry in enumerate(entries, 1):
        annotation = annotations.get(entry["id"])
        if not annotation:
            sys.exit(f"Missing annotation for {entry['id']}")
        # Embed the annotation, not the raw text — symmetric with query embeddings
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=annotation)
        vectors.append(response.data[0].embedding)
        metadata.append({
            "id": entry["id"],
            "text": entry["text"],
            "annotation": annotation,
            "context": entry["context"],
            "year": entry["year"],
            "source_type": entry["source_type"],
            "theme_tags": entry.get("theme_tags", []),
        })
        print(f"  [{i}/{len(entries)}] {entry['id']}")

    np.savez(
        OUTPUT_NPZ,
        vectors=np.array(vectors, dtype=np.float32),
        metadata=np.array(metadata, dtype=object),
    )
    print(f"\nSaved {OUTPUT_NPZ}")


if __name__ == "__main__":
    main()
