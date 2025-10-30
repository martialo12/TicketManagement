"""
Custom exceptions for the ticket module.
"""

from uuid import UUID

from fastapi import HTTPException, status

from app.tickets.constants import DATABASE_OPERATION_FAILED


class TicketNotFoundException(HTTPException):
    """Exception raised when a ticket is not found."""

    def __init__(self, ticket_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket with ID {ticket_id} not found",
        )


class TicketCreationFailedException(HTTPException):
    """Exception raised when ticket creation fails."""

    def __init__(self, reason: str = DATABASE_OPERATION_FAILED):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create ticket: {reason}",
        )


class TicketUpdateFailedException(HTTPException):
    """Exception raised when ticket update fails."""

    def __init__(self, ticket_id: UUID, reason: str = DATABASE_OPERATION_FAILED):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update ticket {ticket_id}: {reason}",
        )


class TicketDeletionFailedException(HTTPException):
    """Exception raised when ticket deletion fails."""

    def __init__(self, ticket_id: UUID, reason: str = DATABASE_OPERATION_FAILED):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete ticket {ticket_id}: {reason}",
        )
