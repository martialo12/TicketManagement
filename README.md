# Ticket Management API

REST API for support ticket management, developed with FastAPI, SQLAlchemy, and Pydantic.

🔗 **GitHub Repository**: https://github.com/martialo12/TicketManagement

## 📋 Description

This API allows you to manage support tickets with the following features:
- Create a new ticket
- List all tickets
- Retrieve a specific ticket
- Update a ticket
- Close a ticket

## 🚀 Technologies

- **Python 3.10+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database management
- **Pydantic** - Data validation
- **SQLite** - In-memory database
- **Pytest** - Testing framework
- **Ruff** - Modern Python linter

## 📦 Installation

### Prerequisites

- Python 3.10 or higher (3.11.13 recommended)
- pip (Python package manager)
- **pyenv** (recommended for Python version management)

#### Installing pyenv (if not already installed)

See official pyenv installation guide: https://github.com/pyenv/pyenv#installation

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/martialo12/TicketManagement.git
cd TicketManagement

# Create virtual environment with pyenv (recommended)
pyenv virtualenv 3.11.13 ticket-management
pyenv activate ticket-management

# Install dependencies
pip install -r requirements.txt
pre-commit install
```

### 🚀 Quick Start

```bash
# Run the API
uvicorn app.main:app --reload --port 8000

# Open Swagger UI: http://localhost:8000/docs
```

## 🏃 Running the API

### Method 1: Directly with Uvicorn

```bash
uvicorn app.main:app --reload --port 8000
```

### Method 2: With Make

```bash
make run
```

### Method 3: With Docker Compose (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

The API will be accessible at: **http://localhost:8000**

## 📚 Documentation

Once the API is running, interactive documentation is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Run tests
make test

# Or directly
pytest
```

Current coverage: **84%** (target: 80%)

## 📖 Project Structure

The project architecture follows **SOLID principles** and a **clean layered architecture** (Clean Architecture):

```
TicketManagement/
├── app/
│   ├── core/            # Core components (database, constants)
│   ├── tickets/         # Ticket module (models, schemas, routes, services, repos)
│   └── main.py          # FastAPI entry point
├── tests/               # Test suite
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── requirements.txt
```

**Architecture:** Clean layered architecture with SOLID principles
- Router → Service → Repository → Database
- Dependency injection, logging, error handling
- 84% test coverage

## 🎯 API Endpoints

### Create a ticket

```http
POST /tickets
Content-Type: application/json

{
  "title": "Ticket title",
  "description": "Detailed description"
}
```

**Response:** 201 Created

### List all tickets

```http
GET /tickets?skip=0&limit=100
```

Optional parameters:
- `skip`: Number of tickets to skip (pagination, default: 0)
- `limit`: Maximum number of tickets to return (default: 100, max: 1000)

**Response:** 200 OK

### Retrieve a ticket

```http
GET /tickets/{ticket_id}
```

**Response:** 200 OK or 404 Not Found

### Update a ticket

```http
PUT /tickets/{ticket_id}
Content-Type: application/json

{
  "title": "New title",
  "description": "New description"
}
```

**Note:** Status cannot be updated via this endpoint. Use dedicated endpoints like `PATCH /tickets/{id}/close` to change status.

**Response:** 200 OK or 404 Not Found

### Close a ticket

```http
PATCH /tickets/{ticket_id}/close
```

**Response:** 200 OK or 404 Not Found

### Delete a ticket

```http
DELETE /tickets/{ticket_id}
```

**Response:** 204 No Content or 404 Not Found

## 📊 Data Model

### Ticket

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier (UUID v4) |
| title | str | Ticket title |
| description | str | Detailed description |
| status | enum | Status: "open", "stalled", "closed" |
| created_at | datetime | Creation date (UTC) |

**Example ID:** `550e8400-e29b-41d4-a716-446655440000`

## 🔧 Available Make Commands

```bash
make help        # Display available commands
make install     # Install dependencies
make run         # Run the API locally (port 8000)
make test        # Run tests with coverage
make lint        # Check code with Ruff
make format      # Format and fix code with Ruff
make clean       # Clean generated files
make docker-up   # Build and run with Docker Compose
make docker-down # Stop Docker Compose
```


## 🐳 Docker

```bash
# Quick start
docker-compose up --build -d

# Stop
docker-compose down
```

## 📝 Notes

- No authentication is required to access the API
- Data is stored in memory (SQLite) and is lost on restart
- The API follows REST standards and returns appropriate HTTP codes
- Data validation is automatic thanks to Pydantic
- Ticket IDs use UUID v4 for better security and scalability
- Status changes must use dedicated endpoints (e.g., `/close`)

## 🤝 Contribution

This project is a technical test. For any questions, please contact the developer.

## 📄 License

This project is provided for technical demonstration purposes.
