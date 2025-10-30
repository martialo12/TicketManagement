"""Database models for the ticket management system."""

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, String, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type when available, otherwise CHAR(36) for SQLite.
    Stores as stringified hex values and returns as UUID objects.
    """

    impl = String(36)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return value
        elif isinstance(value, uuid.UUID):
            return str(value)
        else:
            return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "postgresql":
            return value
        else:
            return uuid.UUID(value)


class TicketStatus(str, Enum):
    """Ticket status enumeration."""

    OPEN = "open"
    STALLED = "stalled"
    CLOSED = "closed"


class Ticket(Base):
    """Ticket model for database."""

    __tablename__ = "tickets"

    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default=TicketStatus.OPEN.value)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
