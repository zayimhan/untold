import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[1] / ".env")

OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
EMBEDDING_MODEL: str = "text-embedding-3-small"
CHAT_MODEL: str = "gpt-4o-mini"
LYRIC_MODEL: str = "gpt-5.5"
TEMPERATURE: float = 0.82
TOP_K: int = 5
QUALITY_THRESHOLD: int = 7
ARCHIVE_PATH: Path = Path(__file__).parents[1] / "data" / "archive_embeddings.npz"
