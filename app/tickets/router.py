"""API router for ticket endpoints."""

from typing import List

from fastapi import APIRouter, Body, Depends, Path, Query, status
from loguru import logger

from app.tickets.constants import TICKET_ID_PATH_DESC
from app.tickets.dependencies import get_ticket_service
from app.tickets.schemas import TicketCreate, TicketResponse, TicketUpdate
from app.tickets.services import TicketService

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new ticket",
    responses={
        201: {
            "description": "Ticket created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Application bug",
                        "description": "Application crashes on startup",
                        "status": "open",
                        "created_at": "2025-01-15T10:30:00.000Z",
                    }
                }
            },
        },
        422: {"description": "Validation error"},
    },
)
async def create_ticket(
    ticket_data: TicketCreate = Body(
        ...,
        description="Ticket data to create",
        example={
            "title": "Application bug",
            "description": "Application crashes on startup",
        },
    ),
    ticket_service: TicketService = Depends(get_ticket_service),
):
    """
    Create a new ticket with the following information:

    - **title**: Ticket title (required, max 200 characters)
    - **description**: Detailed ticket description (required)

    The ticket will be created with the "open" status by default.
    """
    logger.info(f"Creating new ticket: {ticket_data.title}")
    ticket = await ticket_service.create_ticket(ticket_data)
    logger.info(f"Ticket created: {ticket.id}")
    return ticket


@router.get(
    "",
    response_model=List[TicketResponse],
    summary="List all tickets",
)
async def list_tickets(
    skip: int = Query(0, ge=0, description="Number of tickets to skip (pagination)"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of tickets to return"
    ),
    ticket_service: TicketService = Depends(get_ticket_service),
):
    """
    Retrieve the list of all tickets with optional pagination.

    - **skip**: Number of tickets to skip (default: 0)
    - **limit**: Maximum number of tickets to return (default: 100, max: 1000)
    """
    logger.debug(f"Listing tickets with skip={skip}, limit={limit}")
    tickets = await ticket_service.get_tickets(skip=skip, limit=limit)
    return tickets


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
    summary="Retrieve a specific ticket",
    responses={
        200: {"description": "Ticket found"},
        404: {
            "description": "Ticket not found",
            "content": {
                "application/json": {"example": {"detail": "Ticket with ID 999 not found"}}
            },
        },
    },
)
async def get_ticket(
    ticket_id: int = Path(..., description=TICKET_ID_PATH_DESC, gt=0),
    ticket_service: TicketService = Depends(get_ticket_service),
):
    """
    Retrieve a ticket by its ID.

    - **ticket_id**: Ticket ID to retrieve

    Returns a 404 error if the ticket does not exist.
    """
    logger.debug(f"Getting ticket with ID: {ticket_id}")
    ticket = await ticket_service.get_ticket(ticket_id)
    return ticket


@router.put(
    "/{ticket_id}",
    response_model=TicketResponse,
    summary="Update a ticket",
    responses={
        200: {"description": "Ticket updated successfully"},
        404: {
            "description": "Ticket not found",
            "content": {
                "application/json": {"example": {"detail": "Ticket with ID 999 not found"}}
            },
        },
        422: {"description": "Validation error"},
    },
)
async def update_ticket(
    ticket_id: int = Path(..., description=TICKET_ID_PATH_DESC, gt=0),
    ticket_data: TicketUpdate = Body(
        ...,
        description="Updated ticket data",
        example={
            "title": "Bug fixed",
            "description": "The bug has been fixed",
            "status": "closed",
        },
    ),
    ticket_service: TicketService = Depends(get_ticket_service),
):
    """
    Update all information of an existing ticket.

    - **ticket_id**: Ticket ID to update
    - **title**: New ticket title
    - **description**: New ticket description
    - **status**: New ticket status (open, stalled, closed)

    Returns a 404 error if the ticket does not exist.
    """
    logger.info(f"Updating ticket with ID: {ticket_id}")
    ticket = await ticket_service.update_ticket(ticket_id, ticket_data)
    logger.info(f"Ticket {ticket_id} updated successfully")
    return ticket


@router.patch(
    "/{ticket_id}/close",
    response_model=TicketResponse,
    summary="Close a ticket",
    responses={
        200: {"description": "Ticket closed successfully"},
        404: {
            "description": "Ticket not found",
            "content": {
                "application/json": {"example": {"detail": "Ticket with ID 999 not found"}}
            },
        },
    },
)
async def close_ticket(
    ticket_id: int = Path(..., description=TICKET_ID_PATH_DESC, gt=0),
    ticket_service: TicketService = Depends(get_ticket_service),
):
    """
    Close a ticket by changing its status to "closed".

    - **ticket_id**: Ticket ID to close

    Returns a 404 error if the ticket does not exist.
    """
    logger.info(f"Closing ticket with ID: {ticket_id}")
    ticket = await ticket_service.close_ticket(ticket_id)
    logger.info(f"Ticket {ticket_id} closed successfully")
    return ticket


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a ticket",
    responses={
        204: {"description": "Ticket deleted successfully"},
        404: {
            "description": "Ticket not found",
            "content": {
                "application/json": {"example": {"detail": "Ticket with ID 999 not found"}}
            },
        },
    },
)
async def delete_ticket(
    ticket_id: int = Path(..., description=TICKET_ID_PATH_DESC, gt=0),
    ticket_service: TicketService = Depends(get_ticket_service),
):
    """
    Permanently delete a ticket.

    - **ticket_id**: Ticket ID to delete

    Returns a 404 error if the ticket does not exist.
    """
    logger.info(f"Deleting ticket with ID: {ticket_id}")
    await ticket_service.delete_ticket(ticket_id)
    logger.info(f"Ticket {ticket_id} deleted successfully")
    return None
