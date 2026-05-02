from __future__ import annotations
import numpy as np
from openai import OpenAI
from app.config import OPENAI_API_KEY, EMBEDDING_MODEL, ARCHIVE_PATH
from app.schemas import ArchiveMatch

_client = OpenAI(api_key=OPENAI_API_KEY)

if not ARCHIVE_PATH.exists():
    raise FileNotFoundError(
        f"Archive embeddings not found at {ARCHIVE_PATH}. "
        "Run backend/scripts/build_embeddings.py first."
    )

_data = np.load(ARCHIVE_PATH, allow_pickle=True)
_vectors: np.ndarray = _data["vectors"]       # shape: (N, 1536)
_metadata: list[dict] = list(_data["metadata"])


def _cosine_similarity(query: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    query_norm = query / np.linalg.norm(query)
    matrix_norm = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix_norm @ query_norm


def find_matches(query: str, top_k: int) -> list[ArchiveMatch]:
    response = _client.embeddings.create(model=EMBEDDING_MODEL, input=query)
    user_vec = np.array(response.data[0].embedding, dtype=np.float32)

    similarities = _cosine_similarity(user_vec, _vectors)
    top_indices = np.argsort(similarities)[::-1][:top_k]

    return [
        ArchiveMatch(
            id=_metadata[i]["id"],
            text=_metadata[i]["text"],
            context=_metadata[i]["context"],
            year=int(_metadata[i]["year"]),
            source_type=_metadata[i]["source_type"],
            similarity=float(similarities[i]),
        )
        for i in top_indices
    ]
