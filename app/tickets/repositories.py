"""
Repository layer for ticket module.
Handles database operations for tickets.
"""

from typing import List, Optional
from uuid import UUID

from loguru import logger
from sqlalchemy.orm import Session

from app.tickets.exceptions import (
    TicketCreationFailedException,
    TicketDeletionFailedException,
    TicketNotFoundException,
    TicketUpdateFailedException,
)
from app.tickets.models import Ticket, TicketStatus
from app.tickets.schemas import TicketCreate, TicketUpdate


class TicketRepository:
    """Repository for ticket database operations."""

    def __init__(self, db: Session):
        """Initialize the repository with database session."""
        self.db = db

    def create_ticket(self, ticket: TicketCreate) -> Ticket:
        """
        Create a new ticket in the database.

        Args:
            ticket: The ticket data to create

        Returns:
            The created ticket

        Raises:
            TicketCreationFailedException: If the creation fails
        """
        try:
            logger.info(f"Creating new ticket with title: {ticket.title}")
            db_ticket = Ticket(
                title=ticket.title,
                description=ticket.description,
                status=TicketStatus.OPEN.value,
            )
            self.db.add(db_ticket)
            self.db.commit()
            self.db.refresh(db_ticket)
            logger.info(f"Ticket created with ID: {db_ticket.id}")
            return db_ticket
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating ticket: {e}")
            raise TicketCreationFailedException(str(e)) from e

    def get_ticket(self, ticket_id: UUID) -> Optional[Ticket]:
        """
        Get a ticket by its ID.

        Args:
            ticket_id: The ID of the ticket to retrieve

        Returns:
            The ticket if found, None otherwise
        """
        try:
            logger.debug(f"Retrieving ticket with ID: {ticket_id}")
            ticket = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
            if ticket:
                logger.debug(f"Found ticket with ID: {ticket_id}")
            else:
                logger.debug(f"Ticket with ID {ticket_id} not found")
            return ticket
        except Exception as e:
            logger.error(f"Error retrieving ticket {ticket_id}: {e}")
            raise

    def get_tickets(self, skip: int = 0, limit: int = 100) -> List[Ticket]:
        """
        Get all tickets with pagination.

        Args:
            skip: Number of tickets to skip
            limit: Maximum number of tickets to return

        Returns:
            List of tickets
        """
        try:
            logger.debug(f"Retrieving tickets with skip={skip}, limit={limit}")
            tickets = self.db.query(Ticket).offset(skip).limit(limit).all()
            logger.debug(f"Retrieved {len(tickets)} tickets")
            return tickets
        except Exception as e:
            logger.error(f"Error retrieving tickets: {e}")
            raise

    def update_ticket(self, ticket_id: UUID, ticket_update: TicketUpdate) -> Ticket:
        """
        Update an existing ticket.

        Args:
            ticket_id: The ID of the ticket to update
            ticket_update: The updated ticket data

        Returns:
            The updated ticket

        Raises:
            TicketNotFoundException: If the ticket is not found
            TicketUpdateFailedException: If the update fails
        """
        try:
            logger.info(f"Updating ticket with ID: {ticket_id}")
            db_ticket = self.get_ticket(ticket_id)
            if db_ticket is None:
                raise TicketNotFoundException(ticket_id)

            db_ticket.title = ticket_update.title
            db_ticket.description = ticket_update.description
            # Status is not updated here - use dedicated endpoints like close_ticket()

            self.db.commit()
            self.db.refresh(db_ticket)
            logger.info(f"Ticket {ticket_id} updated successfully")
            return db_ticket
        except TicketNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating ticket {ticket_id}: {e}")
            raise TicketUpdateFailedException(ticket_id, str(e)) from e

    def close_ticket(self, ticket_id: UUID) -> Ticket:
        """
        Close a ticket by setting its status to CLOSED.

        Args:
            ticket_id: The ID of the ticket to close

        Returns:
            The closed ticket

        Raises:
            TicketNotFoundException: If the ticket is not found
            TicketUpdateFailedException: If the update fails
        """
        try:
            logger.info(f"Closing ticket with ID: {ticket_id}")
            db_ticket = self.get_ticket(ticket_id)
            if db_ticket is None:
                raise TicketNotFoundException(ticket_id)

            db_ticket.status = TicketStatus.CLOSED.value
            self.db.commit()
            self.db.refresh(db_ticket)
            logger.info(f"Ticket {ticket_id} closed successfully")
            return db_ticket
        except TicketNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error closing ticket {ticket_id}: {e}")
            raise TicketUpdateFailedException(ticket_id, str(e)) from e

    def delete_ticket(self, ticket_id: UUID) -> None:
        """
        Delete a ticket from the database.

        Args:
            ticket_id: The ID of the ticket to delete

        Raises:
            TicketNotFoundException: If the ticket is not found
            TicketDeletionFailedException: If the deletion fails
        """
        try:
            logger.info(f"Deleting ticket with ID: {ticket_id}")
            db_ticket = self.get_ticket(ticket_id)
            if db_ticket is None:
                raise TicketNotFoundException(ticket_id)

            self.db.delete(db_ticket)
            self.db.commit()
            logger.info(f"Ticket {ticket_id} deleted successfully")
        except TicketNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting ticket {ticket_id}: {e}")
            raise TicketDeletionFailedException(ticket_id, str(e)) from e
