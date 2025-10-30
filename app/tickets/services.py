"""
Service layer for ticket module.
Handles business logic for tickets.
"""

from typing import List
from uuid import UUID

from loguru import logger

from app.tickets.exceptions import TicketNotFoundException
from app.tickets.repositories import TicketRepository
from app.tickets.schemas import TicketCreate, TicketResponse, TicketUpdate


class TicketService:
    """Service for ticket business logic."""

    def __init__(self, repository: TicketRepository):
        """
        Initialize the service with the ticket repository.

        Args:
            repository: The ticket repository instance
        """
        self.repository = repository

    async def create_ticket(self, ticket_data: TicketCreate) -> TicketResponse:
        """
        Create a new ticket.

        Args:
            ticket_data: The ticket data to create

        Returns:
            The created ticket

        Raises:
            TicketCreationFailedException: If the ticket creation fails
        """
        logger.info(f"Service: Creating new ticket with title '{ticket_data.title}'")
        ticket = self.repository.create_ticket(ticket_data)
        logger.info(f"Service: Ticket created successfully with ID {ticket.id}")
        return TicketResponse.model_validate(ticket)

    async def get_ticket(self, ticket_id: UUID) -> TicketResponse:
        """
        Get a ticket by its ID.

        Args:
            ticket_id: The ID of the ticket to retrieve

        Returns:
            The ticket

        Raises:
            TicketNotFoundException: If the ticket is not found
        """
        logger.debug(f"Service: Retrieving ticket with ID {ticket_id}")
        ticket = self.repository.get_ticket(ticket_id)
        if ticket is None:
            raise TicketNotFoundException(ticket_id)
        return TicketResponse.model_validate(ticket)

    async def get_tickets(self, skip: int = 0, limit: int = 100) -> List[TicketResponse]:
        """
        Get all tickets with pagination.

        Args:
            skip: Number of tickets to skip
            limit: Maximum number of tickets to return

        Returns:
            List of tickets
        """
        logger.debug(f"Service: Retrieving tickets with skip={skip}, limit={limit}")
        tickets = self.repository.get_tickets(skip=skip, limit=limit)
        return [TicketResponse.model_validate(ticket) for ticket in tickets]

    async def update_ticket(self, ticket_id: UUID, ticket_data: TicketUpdate) -> TicketResponse:
        """
        Update an existing ticket.

        Args:
            ticket_id: The ID of the ticket to update
            ticket_data: The updated ticket data

        Returns:
            The updated ticket

        Raises:
            TicketNotFoundException: If the ticket is not found
            TicketUpdateFailedException: If the update fails
        """
        logger.info(f"Service: Updating ticket with ID {ticket_id}")
        ticket = self.repository.update_ticket(ticket_id, ticket_data)
        logger.info(f"Service: Ticket {ticket_id} updated successfully")
        return TicketResponse.model_validate(ticket)

    async def close_ticket(self, ticket_id: UUID) -> TicketResponse:
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
        logger.info(f"Service: Closing ticket with ID {ticket_id}")
        ticket = self.repository.close_ticket(ticket_id)
        logger.info(f"Service: Ticket {ticket_id} closed successfully")
        return TicketResponse.model_validate(ticket)

    async def delete_ticket(self, ticket_id: UUID) -> None:
        """
        Delete a ticket.

        Args:
            ticket_id: The ID of the ticket to delete

        Raises:
            TicketNotFoundException: If the ticket is not found
            TicketDeletionFailedException: If the deletion fails
        """
        logger.info(f"Service: Deleting ticket with ID {ticket_id}")
        self.repository.delete_ticket(ticket_id)
        logger.info(f"Service: Ticket {ticket_id} deleted successfully")
