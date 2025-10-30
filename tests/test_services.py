"""Tests for service layer."""

import pytest

from app.tickets.exceptions import TicketNotFoundException
from app.tickets.models import TicketStatus
from app.tickets.repositories import TicketRepository
from app.tickets.schemas import TicketCreate, TicketUpdate
from app.tickets.services import TicketService


class TestTicketService:
    """Tests for ticket service layer."""

    @pytest.mark.asyncio
    async def test_create_ticket(self, db_session):
        """Test creating a ticket via service."""
        repository = TicketRepository(db_session)
        service = TicketService(repository)

        ticket_data = TicketCreate(title="Service Test", description="Testing service layer")
        ticket = await service.create_ticket(ticket_data)

        assert ticket.id is not None
        assert ticket.title == "Service Test"
        assert ticket.description == "Testing service layer"
        assert ticket.status == TicketStatus.OPEN

    @pytest.mark.asyncio
    async def test_get_ticket(self, db_session):
        """Test getting a ticket via service."""
        repository = TicketRepository(db_session)
        service = TicketService(repository)

        # Create a ticket
        ticket_data = TicketCreate(title="Test", description="Test description")
        created = await service.create_ticket(ticket_data)

        # Retrieve it
        retrieved = await service.get_ticket(created.id)
        assert retrieved.id == created.id
        assert retrieved.title == created.title

    @pytest.mark.asyncio
    async def test_get_nonexistent_ticket(self, db_session):
        """Test getting a nonexistent ticket raises exception."""
        repository = TicketRepository(db_session)
        service = TicketService(repository)

        with pytest.raises(TicketNotFoundException):
            await service.get_ticket(999)

    @pytest.mark.asyncio
    async def test_get_tickets(self, db_session):
        """Test listing tickets via service."""
        repository = TicketRepository(db_session)
        service = TicketService(repository)

        # Create multiple tickets
        for i in range(3):
            ticket_data = TicketCreate(title=f"Ticket {i}", description=f"Description {i}")
            await service.create_ticket(ticket_data)

        tickets = await service.get_tickets()
        assert len(tickets) == 3

    @pytest.mark.asyncio
    async def test_update_ticket(self, db_session):
        """Test updating a ticket via service."""
        repository = TicketRepository(db_session)
        service = TicketService(repository)

        # Create a ticket
        ticket_data = TicketCreate(title="Original", description="Original description")
        created = await service.create_ticket(ticket_data)

        # Update it
        update_data = TicketUpdate(
            title="Updated", description="Updated description", status=TicketStatus.STALLED
        )
        updated = await service.update_ticket(created.id, update_data)

        assert updated.id == created.id
        assert updated.title == "Updated"
        assert updated.description == "Updated description"
        assert updated.status == TicketStatus.STALLED

    @pytest.mark.asyncio
    async def test_close_ticket(self, db_session):
        """Test closing a ticket via service."""
        repository = TicketRepository(db_session)
        service = TicketService(repository)

        # Create a ticket
        ticket_data = TicketCreate(title="To Close", description="This will be closed")
        created = await service.create_ticket(ticket_data)

        # Close it
        closed = await service.close_ticket(created.id)

        assert closed.id == created.id
        assert closed.status == TicketStatus.CLOSED

    @pytest.mark.asyncio
    async def test_delete_ticket(self, db_session):
        """Test deleting a ticket via service."""
        repository = TicketRepository(db_session)
        service = TicketService(repository)

        # Create a ticket
        ticket_data = TicketCreate(title="To Delete", description="This will be deleted")
        created = await service.create_ticket(ticket_data)

        # Delete it
        await service.delete_ticket(created.id)

        # Verify it's gone
        with pytest.raises(TicketNotFoundException):
            await service.get_ticket(created.id)
