"""Database configuration and session management."""

from abc import ABC, abstractmethod
from typing import Generator, Optional

from loguru import logger
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

# Constants
DB_NOT_CONNECTED_ERROR = "Database not connected. Call connect() first."


class Database(ABC):
    """Abstract base class for database connections."""

    @abstractmethod
    def connect(self) -> Engine:
        """Establish database connection and return engine."""
        pass

    @abstractmethod
    def get_session(self) -> Session:
        """Get a database session."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close database connection."""
        pass


class SQLiteDatabase(Database):
    """SQLite database implementation with singleton pattern."""

    _instance: Optional["SQLiteDatabase"] = None
    _engine: Optional[Engine] = None
    _session_factory: Optional[sessionmaker] = None

    def __new__(cls):
        """Ensure only one instance of database connection exists (Singleton)."""
        if cls._instance is None:
            logger.info("Creating new SQLiteDatabase instance")
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, database_url: str = "sqlite:///:memory:"):
        """Initialize SQLite database connection."""
        # Only initialize once
        if self._engine is None:
            self.database_url = database_url
            self.connect()

    def connect(self) -> Engine:
        """Establish SQLite database connection."""
        if self._engine is None:
            logger.info(f"Connecting to SQLite database: {self.database_url}")
            self._engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False},
                pool_pre_ping=True,  # Verify connections before using
            )
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            )
            logger.info("SQLite database connected successfully")
        return self._engine

    def get_session(self) -> Session:
        """Get a new database session."""
        if self._session_factory is None:
            raise RuntimeError(DB_NOT_CONNECTED_ERROR)
        return self._session_factory()

    def close(self) -> None:
        """Close database connection."""
        if self._engine is not None:
            logger.info("Closing SQLite database connection")
            self._engine.dispose()
            self._engine = None
            self._session_factory = None
            logger.info("SQLite database connection closed")

    @property
    def engine(self) -> Engine:
        """Get database engine."""
        if self._engine is None:
            raise RuntimeError(DB_NOT_CONNECTED_ERROR)
        return self._engine


# Global database instance (Singleton)
# This ensures only one connection throughout the application lifetime
db_instance = SQLiteDatabase()

# Legacy compatibility: expose engine for models
engine = db_instance.engine


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session.
    
    This is used by FastAPI's dependency injection system.
    It ensures proper session lifecycle management.
    """
    session = db_instance.get_session()
    try:
        yield session
    finally:
        session.close()


def get_database_instance() -> Database:
    """Get the singleton database instance.
    
    Returns:
        The global database instance
    """
    return db_instance
