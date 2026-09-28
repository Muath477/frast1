from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _sqlite_engine():
    db_file = Path(__file__).resolve().parents[3] / "data" / "rootiq.db"
    db_file.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False},
    )


def _make_engine():
    url = settings.database_url
    if url.startswith("postgresql"):
        try:
            eng = create_engine(
                url,
                pool_pre_ping=True,
                connect_args={"connect_timeout": 2},
            )
            with eng.connect() as conn:
                conn.execute(text("SELECT 1"))
            return eng
        except Exception:
            return _sqlite_engine()
    return create_engine(url, pool_pre_ping=True)


engine = _make_engine()
SessionLocal = sessionmaker(engine, expire_on_commit=False)
