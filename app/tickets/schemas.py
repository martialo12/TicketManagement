"""Pydantic schemas for request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.tickets.constants import (
    EXAMPLE_CREATED_AT,
    EXAMPLE_DESCRIPTION,
    EXAMPLE_STATUS_OPEN,
    EXAMPLE_TICKET_ID,
    EXAMPLE_TITLE,
    TICKET_CREATED_AT_DESC,
    TICKET_DESCRIPTION_DESC,
    TICKET_ID_DESC,
    TICKET_STATUS_DESC,
    TICKET_TITLE_DESC,
)
from app.tickets.models import TicketStatus


class TicketBase(BaseModel):
    """Base schema for ticket data."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description=TICKET_TITLE_DESC,
        example=EXAMPLE_TITLE,
    )
    description: str = Field(
        ..., min_length=1, description=TICKET_DESCRIPTION_DESC, example=EXAMPLE_DESCRIPTION
    )


class TicketCreate(TicketBase):
    """Schema for creating a new ticket."""

    pass


class TicketUpdate(TicketBase):
    """Schema for updating an existing ticket.

    Note: Status cannot be updated via this endpoint.
    Use dedicated endpoints like PATCH /tickets/{id}/close to change status.
    """

    pass


class TicketResponse(TicketBase):
    """Schema for ticket response."""

    id: UUID = Field(..., description=TICKET_ID_DESC, example=EXAMPLE_TICKET_ID)
    status: TicketStatus = Field(..., description=TICKET_STATUS_DESC, example=EXAMPLE_STATUS_OPEN)
    created_at: datetime = Field(
        ..., description=TICKET_CREATED_AT_DESC, example=EXAMPLE_CREATED_AT
    )

    model_config = ConfigDict(from_attributes=True)
