"""
Constants for the ticket management module.
"""

# API Documentation
API_TITLE = "Ticket Management API"
API_DESCRIPTION = "REST API for support ticket management"
API_VERSION = "1.0.0"

# Path parameter descriptions
TICKET_ID_PATH_DESC = "Unique ticket ID"

# Field descriptions
TICKET_ID_DESC = "Unique ticket identifier (auto-incremented)"
TICKET_TITLE_DESC = "Ticket title"
TICKET_DESCRIPTION_DESC = "Detailed ticket description"
TICKET_STATUS_DESC = "Ticket status (open, stalled, closed)"
TICKET_CREATED_AT_DESC = "Ticket creation date and time (UTC)"

# Validation messages
TICKET_NOT_FOUND = "Ticket not found"
DATABASE_OPERATION_FAILED = "Database operation failed"

# Example values
EXAMPLE_TICKET_ID = 1
EXAMPLE_TITLE = "Application bug"
EXAMPLE_DESCRIPTION = "Application crashes on startup"
EXAMPLE_STATUS_OPEN = "open"
EXAMPLE_STATUS_STALLED = "stalled"
EXAMPLE_STATUS_CLOSED = "closed"
EXAMPLE_CREATED_AT = "2025-01-15T10:30:00.000Z"

# Pagination defaults
DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100
MAX_LIMIT = 1000
