from contextlib import asynccontextmanager
import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router
from app.logging_config import configure_logging

log = logging.getLogger("untold.main")

_raw = os.environ.get("ALLOWED_ORIGINS", "http://localhost:4200")
ALLOWED_ORIGINS = [o.strip() for o in _raw.split(",") if o.strip()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    log.info("untold.startup", extra={"allowed_origins": ALLOWED_ORIGINS})
    yield
    log.info("untold.shutdown")


app = FastAPI(title="Untold — 1973", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(router)
