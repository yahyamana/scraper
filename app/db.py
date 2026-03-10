from __future__ import annotations

from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

DB_PATH = Path("data") / "finder.db"
DB_PATH.parent.mkdir(exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
