"""Tests for API endpoints."""

from fastapi import status

from app.tickets.models import TicketStatus


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_read_root(self, client):
        """Test root endpoint returns correct information."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "documentation" in data
        assert "version" in data
        assert data["documentation"] == "/docs"


class TestCreateTicket:
    """Tests for ticket creation endpoint."""

    def test_create_ticket_success(self, client):
        """Test successful ticket creation."""
        ticket_data = {
            "title": "Test Ticket",
            "description": "This is a test ticket description",
        }
        response = client.post("/tickets/", json=ticket_data)
        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()
        assert data["title"] == ticket_data["title"]
        assert data["description"] == ticket_data["description"]
        assert data["status"] == TicketStatus.OPEN.value
        assert "id" in data
        assert "created_at" in data

    def test_create_ticket_missing_title(self, client):
        """Test ticket creation fails without title."""
        ticket_data = {"description": "Description without title"}
        response = client.post("/tickets/", json=ticket_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_ticket_missing_description(self, client):
        """Test ticket creation fails without description."""
        ticket_data = {"title": "Title without description"}
        response = client.post("/tickets/", json=ticket_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_ticket_empty_title(self, client):
        """Test ticket creation fails with empty title."""
        ticket_data = {"title": "", "description": "Valid description"}
        response = client.post("/tickets/", json=ticket_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestListTickets:
    """Tests for listing tickets endpoint."""

    def test_list_tickets_empty(self, client):
        """Test listing tickets when no tickets exist."""
        response = client.get("/tickets/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_tickets_with_data(self, client):
        """Test listing tickets with existing tickets."""
        # Create multiple tickets
        ticket1 = {"title": "Ticket 1", "description": "Description 1"}
        ticket2 = {"title": "Ticket 2", "description": "Description 2"}

        client.post("/tickets/", json=ticket1)
        client.post("/tickets/", json=ticket2)

        response = client.get("/tickets/")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == ticket1["title"]
        assert data[1]["title"] == ticket2["title"]

    def test_list_tickets_with_pagination(self, client):
        """Test listing tickets with pagination parameters."""
        # Create multiple tickets
        for i in range(5):
            ticket = {"title": f"Ticket {i}", "description": f"Description {i}"}
            client.post("/tickets/", json=ticket)

        # Test skip parameter
        response = client.get("/tickets/?skip=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3

        # Test limit parameter
        response = client.get("/tickets/?limit=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

        # Test both parameters
        response = client.get("/tickets/?skip=1&limit=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2


class TestGetTicket:
    """Tests for getting a single ticket endpoint."""

    def test_get_ticket_success(self, client):
        """Test successful retrieval of a ticket."""
        # Create a ticket first
        ticket_data = {"title": "Test Ticket", "description": "Test Description"}
        create_response = client.post("/tickets/", json=ticket_data)
        ticket_id = create_response.json()["id"]

        # Get the ticket
        response = client.get(f"/tickets/{ticket_id}")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["id"] == ticket_id
        assert data["title"] == ticket_data["title"]
        assert data["description"] == ticket_data["description"]

    def test_get_ticket_not_found(self, client):
        """Test getting a non-existent ticket returns 404."""
        response = client.get("/tickets/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "non trouvé" in response.json()["detail"]


class TestUpdateTicket:
    """Tests for updating ticket endpoint."""

    def test_update_ticket_success(self, client):
        """Test successful ticket update."""
        # Create a ticket first
        ticket_data = {"title": "Original Title", "description": "Original Description"}
        create_response = client.post("/tickets/", json=ticket_data)
        ticket_id = create_response.json()["id"]

        # Update the ticket
        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "status": TicketStatus.STALLED.value,
        }
        response = client.put(f"/tickets/{ticket_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["status"] == update_data["status"]

    def test_update_ticket_not_found(self, client):
        """Test updating a non-existent ticket returns 404."""
        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "status": TicketStatus.OPEN.value,
        }
        response = client.put("/tickets/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_ticket_invalid_status(self, client):
        """Test updating with invalid status returns 422."""
        # Create a ticket first
        ticket_data = {"title": "Test Ticket", "description": "Test Description"}
        create_response = client.post("/tickets/", json=ticket_data)
        ticket_id = create_response.json()["id"]

        # Try to update with invalid status
        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "status": "invalid_status",
        }
        response = client.put(f"/tickets/{ticket_id}", json=update_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestCloseTicket:
    """Tests for closing ticket endpoint."""

    def test_close_ticket_success(self, client):
        """Test successfully closing a ticket."""
        # Create a ticket first
        ticket_data = {"title": "Test Ticket", "description": "Test Description"}
        create_response = client.post("/tickets/", json=ticket_data)
        ticket_id = create_response.json()["id"]

        # Close the ticket
        response = client.patch(f"/tickets/{ticket_id}/close")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["status"] == TicketStatus.CLOSED.value
        assert data["title"] == ticket_data["title"]
        assert data["description"] == ticket_data["description"]

    def test_close_ticket_not_found(self, client):
        """Test closing a non-existent ticket returns 404."""
        response = client.patch("/tickets/999/close")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_close_already_closed_ticket(self, client):
        """Test closing an already closed ticket."""
        # Create and close a ticket
        ticket_data = {"title": "Test Ticket", "description": "Test Description"}
        create_response = client.post("/tickets/", json=ticket_data)
        ticket_id = create_response.json()["id"]

        # Close it once
        client.patch(f"/tickets/{ticket_id}/close")

        # Close it again
        response = client.patch(f"/tickets/{ticket_id}/close")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == TicketStatus.CLOSED.value


class TestTicketWorkflow:
    """Integration tests for complete ticket workflows."""

    def test_complete_ticket_lifecycle(self, client):
        """Test a complete ticket lifecycle from creation to closure."""
        # 1. Create a ticket
        ticket_data = {"title": "Bug Report", "description": "Found a critical bug"}
        create_response = client.post("/tickets/", json=ticket_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        ticket_id = create_response.json()["id"]
        assert create_response.json()["status"] == TicketStatus.OPEN.value

        # 2. List all tickets and verify it's there
        list_response = client.get("/tickets/")
        assert len(list_response.json()) == 1

        # 3. Get the specific ticket
        get_response = client.get(f"/tickets/{ticket_id}")
        assert get_response.status_code == status.HTTP_200_OK

        # 4. Update the ticket to stalled
        update_data = {
            "title": "Updated Bug Report",
            "description": "Updated description",
            "status": TicketStatus.STALLED.value,
        }
        update_response = client.put(f"/tickets/{ticket_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["status"] == TicketStatus.STALLED.value

        # 5. Close the ticket
        close_response = client.patch(f"/tickets/{ticket_id}/close")
        assert close_response.status_code == status.HTTP_200_OK
        assert close_response.json()["status"] == TicketStatus.CLOSED.value

        # 6. Verify final state
        final_response = client.get(f"/tickets/{ticket_id}")
        assert final_response.json()["status"] == TicketStatus.CLOSED.value
