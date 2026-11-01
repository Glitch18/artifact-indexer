# AI Usage Log

Conceptual contribution and prose: 100% AI generated / 0% human refactored at initial creation. Exact student prompts: `docs/prompts.md`, especially P3. This log records the actual running desktop agent, not an invented standalone CLI test. Verification results are added only after commands complete.

# Initial agent prompt test

Date: November 1, 2026. Agent environment: `Agent_environment.md`.

## Prompt and generation

The student authorized the running Codex agent with P3:

> Okay done, our entry is in the google doc now.
>
> Let's start working on the project so we can finish this week's submission. Let me know if anything is required or if I need to do anything in the end

Inputs: earlier domain/stack discussion (P1-P2), the assignment PDF, the selected Domain 1 and the agreed Python/FastAPI/PostgreSQL/Docker/Actions/Trivy/Semgrep stack. P4 subsequently reserved GitHub operations for the student.

The agent first wrote `spec.md`, then generated a minimal app rather than the full business service. Actual generated source in `app/main.py` includes:

```python
@app.get("/healthz", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()
```

```python
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
```

The complete generated code and tests live in `app/`, `tests/`, and `scripts/`; snippets are not substituted for source. Source headers disclose AI authorship. The agent also generated dependency files, Docker/Compose and the pipeline workflow. See `code_AI_history.md` for revisions and `Pipeline_execution_log.md` for actual command outcomes. Human code refactoring during this initial run: none. Student review is still required before submission.
