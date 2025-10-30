"""Tests for repository operations."""

import pytest

from app.tickets.models import TicketStatus
from app.tickets.repositories import TicketRepository
from app.tickets.schemas import TicketCreate, TicketUpdate


class TestCreateTicket:
    """Tests for creating tickets in the database."""

    def test_create_ticket(self, db_session):
        """Test creating a ticket via repository."""
        repository = TicketRepository(db_session)
        ticket_data = TicketCreate(title="Repository Test", description="Testing repository operations")
        ticket = repository.create_ticket(ticket_data)

        assert ticket.id is not None
        assert ticket.title == "Repository Test"
        assert ticket.description == "Testing repository operations"
        assert ticket.status == TicketStatus.OPEN.value
        assert ticket.created_at is not None


class TestGetTicket:
    """Tests for retrieving tickets from the database."""

    def test_get_existing_ticket(self, db_session):
        """Test getting an existing ticket."""
        repository = TicketRepository(db_session)
        # Create a ticket first
        ticket_data = TicketCreate(title="Test", description="Test description")
        created = repository.create_ticket(ticket_data)

        # Retrieve it
        retrieved = repository.get_ticket(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == created.title

    def test_get_nonexistent_ticket(self, db_session):
        """Test getting a ticket that doesn't exist."""
        repository = TicketRepository(db_session)
        retrieved = repository.get_ticket(999)
        assert retrieved is None


class TestGetTickets:
    """Tests for listing all tickets."""

    def test_get_tickets_empty(self, db_session):
        """Test getting tickets when database is empty."""
        repository = TicketRepository(db_session)
        tickets = repository.get_tickets()
        assert len(tickets) == 0

    def test_get_tickets_multiple(self, db_session):
        """Test getting multiple tickets."""
        repository = TicketRepository(db_session)
        # Create multiple tickets
        for i in range(3):
            ticket_data = TicketCreate(title=f"Ticket {i}", description=f"Description {i}")
            repository.create_ticket(ticket_data)

        tickets = repository.get_tickets()
        assert len(tickets) == 3

    def test_get_tickets_with_pagination(self, db_session):
        """Test pagination parameters."""
        repository = TicketRepository(db_session)
        # Create 5 tickets
        for i in range(5):
            ticket_data = TicketCreate(title=f"Ticket {i}", description=f"Description {i}")
            repository.create_ticket(ticket_data)

        # Test skip
        tickets = repository.get_tickets(skip=2)
        assert len(tickets) == 3

        # Test limit
        tickets = repository.get_tickets(limit=2)
        assert len(tickets) == 2

        # Test both
        tickets = repository.get_tickets(skip=1, limit=2)
        assert len(tickets) == 2


class TestUpdateTicket:
    """Tests for updating tickets."""

    def test_update_ticket_success(self, db_session):
        """Test successfully updating a ticket."""
        repository = TicketRepository(db_session)
        # Create a ticket
        ticket_data = TicketCreate(title="Original", description="Original description")
        created = repository.create_ticket(ticket_data)

        # Update it
        update_data = TicketUpdate(
            title="Updated", description="Updated description", status=TicketStatus.STALLED
        )
        updated = repository.update_ticket(created.id, update_data)

        assert updated is not None
        assert updated.id == created.id
        assert updated.title == "Updated"
        assert updated.description == "Updated description"
        assert updated.status == TicketStatus.STALLED.value

    def test_update_nonexistent_ticket(self, db_session):
        """Test updating a ticket that doesn't exist."""
        repository = TicketRepository(db_session)
        update_data = TicketUpdate(
            title="Updated", description="Updated description", status=TicketStatus.OPEN
        )
        try:
            repository.update_ticket(999, update_data)
            assert False, "Should have raised TicketNotFoundException"
        except Exception:
            pass  # Expected


class TestCloseTicket:
    """Tests for closing tickets."""

    def test_close_ticket_success(self, db_session):
        """Test successfully closing a ticket."""
        repository = TicketRepository(db_session)
        # Create a ticket
        ticket_data = TicketCreate(title="To Close", description="This will be closed")
        created = repository.create_ticket(ticket_data)

        # Close it
        closed = repository.close_ticket(created.id)

        assert closed is not None
        assert closed.id == created.id
        assert closed.status == TicketStatus.CLOSED.value

    def test_close_nonexistent_ticket(self, db_session):
        """Test closing a ticket that doesn't exist."""
        repository = TicketRepository(db_session)
        try:
            repository.close_ticket(999)
            assert False, "Should have raised TicketNotFoundException"
        except Exception:
            pass  # Expected

    def test_close_already_closed_ticket(self, db_session):
        """Test closing an already closed ticket."""
        repository = TicketRepository(db_session)
        # Create and close a ticket
        ticket_data = TicketCreate(title="Test", description="Test")
        created = repository.create_ticket(ticket_data)
        repository.close_ticket(created.id)

        # Close again
        closed = repository.close_ticket(created.id)
        assert closed is not None
        assert closed.status == TicketStatus.CLOSED.value
