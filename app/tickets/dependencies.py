"""
Dependency injection for ticket module.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.tickets.repositories import TicketRepository
from app.tickets.services import TicketService


def get_ticket_repository(db: Session = Depends(get_db)) -> TicketRepository:
    """
    Dependency to get the ticket repository.

    Args:
        db: The database session

    Returns:
        An instance of the TicketRepository
    """
    return TicketRepository(db)


def get_ticket_service(
    repository: TicketRepository = Depends(get_ticket_repository),
) -> TicketService:
    """
    Dependency to get the ticket service.

    Args:
        repository: The ticket repository instance

    Returns:
        An instance of the TicketService
    """
    return TicketService(repository)
