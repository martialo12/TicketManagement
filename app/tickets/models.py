"""Database models for the ticket management system."""

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TicketStatus(str, Enum):
    """Ticket status enumeration."""

    OPEN = "open"
    STALLED = "stalled"
    CLOSED = "closed"


class Ticket(Base):
    """Ticket model for database."""

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default=TicketStatus.OPEN.value)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
