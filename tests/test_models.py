"""Tests for database models."""

from datetime import datetime

from app.tickets.models import Ticket, TicketStatus


class TestTicketModel:
    """Tests for Ticket model."""

    def test_ticket_creation(self, db_session):
        """Test creating a ticket model instance."""
        ticket = Ticket(
            title="Test Ticket", description="Test Description", status=TicketStatus.OPEN.value
        )
        db_session.add(ticket)
        db_session.commit()
        db_session.refresh(ticket)

        assert ticket.id is not None
        assert ticket.title == "Test Ticket"
        assert ticket.description == "Test Description"
        assert ticket.status == TicketStatus.OPEN.value
        assert isinstance(ticket.created_at, datetime)

    def test_ticket_default_status(self, db_session):
        """Test that default status is OPEN."""
        ticket = Ticket(title="Test", description="Test")
        db_session.add(ticket)
        db_session.commit()
        db_session.refresh(ticket)

        assert ticket.status == TicketStatus.OPEN.value

    def test_ticket_status_change(self, db_session):
        """Test changing ticket status."""
        ticket = Ticket(title="Test", description="Test", status=TicketStatus.OPEN.value)
        db_session.add(ticket)
        db_session.commit()

        ticket.status = TicketStatus.CLOSED.value
        db_session.commit()
        db_session.refresh(ticket)

        assert ticket.status == TicketStatus.CLOSED.value


class TestTicketStatus:
    """Tests for TicketStatus enum."""

    def test_status_values(self):
        """Test that status enum has correct values."""
        assert TicketStatus.OPEN.value == "open"
        assert TicketStatus.STALLED.value == "stalled"
        assert TicketStatus.CLOSED.value == "closed"

    def test_status_is_string_enum(self):
        """Test that TicketStatus is a string enum."""
        status = TicketStatus.OPEN
        assert isinstance(status.value, str)
