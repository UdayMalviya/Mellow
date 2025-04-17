from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configurations.config import settings    #config import settings




# Read from environment (Infisical or .env already loaded elsewhere)
DATABASE_URL = settings.database_url

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables.")

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # helps with stale connections
    pool_size=20,
    max_overflow=0
)

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
