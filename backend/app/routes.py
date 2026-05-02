from __future__ import annotations
import asyncio
import json
import logging
import uuid

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from app.schemas import TransformRequest, TransformResponse, EvaluatorMetadata
from app.matcher import find_matches
from app.theme_interpreter import interpret_theme
from app.evaluator import select_best_match
from app.transformer import generate_lyric, stream_lyric_tokens
from app.audio_selector import select_ambient_track
from app.guardian import is_inappropriate
from app.config import TOP_K, QUALITY_THRESHOLD

router = APIRouter()
log = logging.getLogger("untold.routes")

_BLOCKED_SSE = 'data: {"type": "blocked"}\n\n'


async def _resolve_match(user_text: str, request_id: str):
    log.info("resolve_match.start", extra={"request_id": request_id})
    try:
        theme = await asyncio.to_thread(interpret_theme, user_text)
        log.info(
            "theme.resolved",
            extra={
                "request_id": request_id,
                "valence": theme.get("valence"),
                "relational": theme.get("relational_direction"),
            },
        )

        candidates = await asyncio.to_thread(find_matches, theme["search_query"], TOP_K)
        if not candidates:
            raise HTTPException(status_code=500, detail="No archive candidates found.")
        log.info(
            "candidates.found",
            extra={
                "request_id": request_id,
                "ids": [c.id for c in candidates],
                "top_similarity": candidates[0].similarity,
            },
        )

        selected, history, final_score = await asyncio.to_thread(
            select_best_match, user_text, theme, candidates, QUALITY_THRESHOLD
        )
        log.info(
            "evaluator.selected",
            extra={
                "request_id": request_id,
                "id": selected.id,
                "score": final_score,
                "retried": len(history) > 1,
            },
        )

        eval_metadata = EvaluatorMetadata(
            final_score=final_score,
            retried=len(history) > 1,
            history=history,
        )
        return selected, eval_metadata
    except HTTPException:
        raise
    except Exception:
        log.exception("resolve_match.failed", extra={"request_id": request_id})
        raise HTTPException(status_code=500, detail="The pipeline could not complete.")


@router.post("/api/transform", response_model=TransformResponse)
async def transform(request: TransformRequest, http_request: Request) -> TransformResponse:
    request_id = str(uuid.uuid4())[:8]

    if await is_inappropriate(request.user_text):
        log.warning("guardian.blocked", extra={"request_id": request_id})
        raise HTTPException(status_code=422, detail="blocked")

    selected, eval_metadata = await _resolve_match(request.user_text, request_id)
    lyric = await asyncio.to_thread(generate_lyric, request.user_text, [selected])
    ambient_track = select_ambient_track(selected.source_type)
    log.info("transform.complete", extra={"request_id": request_id})
    return TransformResponse(
        lyric=lyric,
        matches=[selected],
        ambient_track=ambient_track,
        evaluator_metadata=eval_metadata,
    )


@router.post("/api/transform/stream")
async def transform_stream(request: TransformRequest) -> StreamingResponse:
    request_id = str(uuid.uuid4())[:8]

    if await is_inappropriate(request.user_text):
        log.warning("guardian.blocked", extra={"request_id": request_id})

        async def blocked_gen():
            yield _BLOCKED_SSE

        return StreamingResponse(
            blocked_gen(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    selected, _ = await _resolve_match(request.user_text, request_id)
    ambient_track = select_ambient_track(selected.source_type)

    async def event_gen():
        yield (
            f"data: {json.dumps({'type': 'matches', 'matches': [selected.model_dump()], 'ambient_track': ambient_track})}\n\n"
        )
        try:
            async for token in stream_lyric_tokens(request.user_text, [selected]):
                yield f"data: {json.dumps({'type': 'token', 'text': token})}\n\n"
            yield 'data: {"type": "done"}\n\n'
        except Exception:
            log.exception("stream.failed", extra={"request_id": request_id})
            yield 'data: {"type": "error"}\n\n'

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
