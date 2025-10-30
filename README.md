# Ticket Management API

REST API for support ticket management, developed with FastAPI, SQLAlchemy, and Pydantic.

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
- pyenv (optional but recommended for Python version management)

### Installing Dependencies

#### Option 1: With pyenv (Recommended)

```bash
# Clone the repository (if applicable)
git clone <repository-url>
cd TicketManagement

# Check available Python versions
pyenv versions

# Create a virtual environment with Python 3.11+
pyenv virtualenv 3.11.13 ticket-management

# Activate the virtual environment
pyenv activate ticket-management

# Or set the environment locally for the project
pyenv local ticket-management

# Install dependencies
pip install -r requirements.txt

# Update pip (optional)
python -m pip install --upgrade pip
```

#### Option 2: With standard venv

```bash
# Clone the repository (if applicable)
git clone <repository-url>
cd TicketManagement

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Setting up Pre-commit Hooks

Pre-commit hooks help maintain code quality by automatically checking your code before each commit.

```bash
# Install pre-commit hooks (after installing dependencies)
pre-commit install

# (Optional) Run hooks on all files manually
pre-commit run --all-files
```

The pre-commit configuration is in `.pre-commit-config.yaml` and includes:
- File size checks
- YAML/TOML validation
- Ruff linting and formatting

### Installation Verification

```bash
# Check Python version
python --version
# Should display: Python 3.11.13 (or 3.10+)

# Check that packages are installed
pip list

# Check database configuration (optional)
python verify_database.py
```

### 🚀 Quick Start

Once the environment is configured, here's how to get started quickly:

```bash
# 1. Activate the environment (if not already done)
pyenv activate ticket-management
# or
source venv/bin/activate

# 2. Launch the API
uvicorn app.main:app --reload

# 3. Open your browser
# http://localhost:8000/docs
```

## 🏃 Running the API

### Method 1: Directly with Uvicorn

```bash
uvicorn app.main:app --reload
```

### Method 2: With Make

```bash
make run
```

### Method 3: With Docker

```bash
# Build the image
docker build -t ticket-api .

# Run the container
docker run -p 8000:8000 ticket-api
```

The API will be accessible at: **http://localhost:8000**

## 📚 Documentation

Once the API is running, interactive documentation is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Running Tests

### Execute all tests with coverage

```bash
pytest
```

### Execute tests with detailed coverage report

```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### With Make

```bash
make test
```

The HTML coverage report will be generated in the `htmlcov/` folder.

## 🔍 Linting

To check code quality with Ruff:

```bash
# Check code
ruff check .

# Automatically fix errors
ruff check --fix .

# With Make
make lint
```

## 📖 Project Structure

The project architecture follows **SOLID principles** and a **clean layered architecture** (Clean Architecture):

```
TicketManagement/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI entry point
│   ├── router.py         # Route/endpoint definitions
│   ├── dependencies.py   # Dependency injection
│   ├── services.py       # Business logic layer
│   ├── repositories.py   # Data access layer
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas (validation)
│   ├── exceptions.py     # Custom exceptions
│   ├── constants.py      # Application constants
│   └── database.py       # Database configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Test configuration
│   ├── test_api.py       # Endpoint tests
│   ├── test_crud.py      # Repository tests
│   └── test_models.py    # Model tests
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project configuration
├── Dockerfile            # Docker configuration
├── Makefile              # Make commands
├── .gitignore
└── README.md
```

### Layered Architecture

The project is organized into distinct layers for better maintainability and testability:

1. **Router Layer** (`router.py`): Defines HTTP endpoints and request validation
2. **Service Layer** (`services.py`): Contains business logic
3. **Repository Layer** (`repositories.py`): Manages data access and CRUD operations
4. **Models** (`models.py`): Defines database entities
5. **Schemas** (`schemas.py`): Data validation and serialization with Pydantic
6. **Dependencies** (`dependencies.py`): Dependency injection to decouple layers

### SOLID Principles Applied

- **S**ingle Responsibility: Each module has a single responsibility (router, service, repository)
- **O**pen/Closed: Classes are open for extension but closed for modification
- **L**iskov Substitution: Dependencies are injected via interfaces
- **I**nterface Segregation: Clear separation between layers via dependency injection
- **D**ependency Inversion: High-level layers don't depend on low-level layers (dependency injection)

### Best Practices

- ✅ **Structured logging** with Loguru
- ✅ **Error handling** via custom exceptions
- ✅ **Strict validation** of data with Pydantic
- ✅ **Automatic OpenAPI documentation** via FastAPI
- ✅ **Unit tests** with coverage > 80%
- ✅ **Python type hints** for better code safety
- ✅ **Centralized constants** to avoid duplication
- ✅ **Separation of responsibilities** (Router → Service → Repository → Database)

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
  "description": "New description",
  "status": "stalled"
}
```

Possible statuses: `open`, `stalled`, `closed`

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
| id | int | Unique identifier (auto-incremented) |
| title | str | Ticket title |
| description | str | Detailed description |
| status | enum | Status: "open", "stalled", "closed" |
| created_at | datetime | Creation date (UTC) |

## 🔧 Available Make Commands

```bash
make install    # Install dependencies
make run        # Launch the API
make test       # Run tests
make coverage   # Generate coverage report
make lint       # Check code with Ruff
make lint-fix   # Automatically fix errors
make clean      # Clean generated files
make docker     # Build Docker image
make help       # Display help
```

## ⚙️ Configuration

### Database

The API uses an in-memory SQLite database. Data is not persisted after application shutdown.

To use a persistent database, modify the `SQLiteDatabase` initialization in `app/database.py`:

```python
# Example with SQLite on disk
db_instance = SQLiteDatabase("sqlite:///./tickets.db")
```

## 🧪 Test Coverage

The project aims for a minimum **80% coverage**.

To check current coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

## 🔗 Git & GitHub Setup

### Initialize Git Repository

```bash
# Initialize Git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Ticket Management API with Clean Architecture"

# Set main branch
git branch -M main
```

### Push to GitHub

```bash
# Add remote repository
git remote add origin git@github.com:martialo12/TicketManagement.git

# Push to GitHub
git push -u origin main
```

### Setup Pre-commit Hooks (After Git Init)

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files (optional)
pre-commit run --all-files
```

## 🐳 Docker

### Build the image

```bash
docker build -t ticket-api .
```

### Run the container

```bash
docker run -p 8000:8000 ticket-api
```

### With Docker Compose

```bash
docker-compose up
```

## 📝 Notes

- No authentication is required to access the API
- Data is stored in memory and is lost on restart
- The API follows REST standards and returns appropriate HTTP codes
- Data validation is automatic thanks to Pydantic

## 🤝 Contribution

This project is a technical test. For any questions, please contact the developer.

## 📄 License

This project is provided for technical demonstration purposes.
