"""Main FastAPI application for ticket management."""

from fastapi import FastAPI

from app.core.constants import (
    DOCS_URL,
    DOCUMENTATION_KEY,
    MESSAGE_KEY,
    REDOC_URL,
    VERSION_KEY,
    WELCOME_MESSAGE,
)
from app.core.database import engine
from app.tickets.constants import API_DESCRIPTION, API_TITLE, API_VERSION
from app.tickets.models import Base
from app.tickets.router import router as ticket_router

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
)

# Include routers
app.include_router(ticket_router)


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup (for development only)."""
    # Note: In production, use Alembic migrations instead
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint returning API information."""
    return {
        MESSAGE_KEY: WELCOME_MESSAGE,
        DOCUMENTATION_KEY: DOCS_URL,
        VERSION_KEY: API_VERSION,
    }
