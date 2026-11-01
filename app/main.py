# AI Contribution Weight: 100% AI Generated / 0% Human Refactored
"""Minimal agent-generated application, intentionally limited to week-one scope."""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    database_url = os.getenv("DATABASE_URL")
    app.state.engine = (
        create_engine(database_url, pool_pre_ping=True, connect_args={"connect_timeout": 3})
        if database_url
        else None
    )
    try:
        yield
    finally:
        if app.state.engine is not None:
            app.state.engine.dispose()


app = FastAPI(title="Project Artifact & Repository Indexer", version="0.1.0", lifespan=lifespan)


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "artifact-indexer"
    phase: str = "week-1"


class ReadinessResponse(BaseModel):
    status: str = "ready"
    database: str = "reachable"


@app.get("/healthz", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@app.get("/readyz", response_model=ReadinessResponse)
def readiness(request: Request) -> ReadinessResponse:
    engine = request.app.state.engine
    if engine is None:
        raise HTTPException(status_code=503, detail="Database unavailable")
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Database unavailable") from None
    return ReadinessResponse()
