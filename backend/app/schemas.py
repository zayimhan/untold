from __future__ import annotations
from pydantic import BaseModel, Field


class TransformRequest(BaseModel):
    user_text: str = Field(..., min_length=1, max_length=2000)


class ArchiveMatch(BaseModel):
    id: str
    text: str
    context: str
    year: int
    source_type: str
    similarity: float


class EvaluatorEntry(BaseModel):
    id: str
    score: int
    reasoning: str


class EvaluatorMetadata(BaseModel):
    final_score: int
    retried: bool
    history: list[EvaluatorEntry]


class TransformResponse(BaseModel):
    lyric: str
    matches: list[ArchiveMatch]
    ambient_track: str
    evaluator_metadata: EvaluatorMetadata | None = None
