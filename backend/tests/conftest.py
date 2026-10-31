import os

# Must be set before app.database is imported anywhere.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
