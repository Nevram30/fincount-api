"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL - Change this based on your database
# SQLite (for development/testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///./fincount.db"

# PostgreSQL (for production)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/fincount"

# MySQL (for production)
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/fincount"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session
    Use this in your route functions like: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
