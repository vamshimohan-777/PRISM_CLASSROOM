from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

RAW_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prism.db")


def normalise_database_url(url: str) -> str:
    """Make a hosting provider's connection string usable by SQLAlchemy 2.

    Render (like Heroku) hands out Postgres URLs beginning with `postgres://`.
    SQLAlchemy 2 removed that alias and raises NoSuchModuleError on it, so a
    blueprint wired straight to `fromDatabase` would fail at boot. Rewrite it to
    the explicit driver form instead.
    """
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


DATABASE_URL = normalise_database_url(RAW_DATABASE_URL)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
