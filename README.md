# AI Usage Log

Conceptual contribution and prose: 100% AI generated / 0% human refactored at initial creation. Exact student prompts: `docs/prompts.md` (P1-P4). Agent configuration and limitations: `Agent_environment.md`. Code changes and verification history: `code_AI_history.md`. Review and execution are distinct from authorship.

# CS763 - Project Artifact & Repository Indexer

Atharva Nimbalkar | Domain 1 | Assignment 1 / week 1.

This repository contains the proposed service specification and a working infrastructure skeleton. `/healthz` and `/readyz` are implemented; the domain CRUD API in `spec.md` is planned for Assignment 2 and is not implemented here. PostgreSQL is dedicated to this service; all external domain entities use fictional local fixtures.

## Submission files

| File | Purpose |
| --- | --- |
| `spec.md` | Proposed REST contracts, JSON schemas, data model, fixtures and acceptance criteria |
| `Agent_environment.md` | Observed agent/tool/host settings, student-confirmed model/effort and unexposed parameters |
| `Prompt_test_log.md` | Exact initial prompt, actual generated source excerpts and verification references |
| `.github/workflows/devsecops.yml` | Tests, Docker build, Compose smoke checks, Semgrep, Trivy, archived evidence |
| `Dockerfile`, `docker-compose.yml` | Multi-stage Python image and isolated PostgreSQL stack |
| `Pipeline_execution_log.md` | Verified local outcomes and separately identified pending GitHub evidence |
| `code_AI_history.md`, `docs/prompts.md` | AI authorship, exact task prompts and change history |
| `SUBMISSION.md` | Student-owned GitHub/release/Blackboard steps |

## Local setup

Prerequisites: Python 3.13, uv 0.13.5, Docker Engine/Desktop with Compose, Git. Docker must be running. Run commands from this repository root.

```bash
uv sync --frozen
uv run --frozen ruff check app tests scripts
uv run --frozen ruff format --check app tests scripts
uv run --frozen pytest -q
docker compose build
docker compose up -d --wait --wait-timeout 120
uv run --frozen python scripts/smoke.py
```

Open http://localhost:8000/docs for the skeleton's actual OpenAPI interface. `/readyz` checks a real SQL connection, while `/healthz` works independently of the DB. The database has no host-published port. The public throwaway course credential in Compose is only for this isolated local stack; it is not a user secret or a production credential.

If port 8000 is occupied, use `API_PORT=8001 docker compose up -d --wait` and `SMOKE_BASE_URL=http://127.0.0.1:8001 uv run --frozen python scripts/smoke.py`.

```bash
docker compose down
```

This stops the project stack while preserving its project-specific database volume. No unrelated containers or volumes need to be removed.

For API-only development without Docker:

```bash
uv run --frozen uvicorn app.main:app --reload
```

Without `DATABASE_URL`, liveness returns 200 and readiness returns 503 by design. Business tables/migrations/authentication do not yet exist.

## Security telemetry

After building the image, run:

```bash
bash scripts/scan.sh semgrep evidence/local
bash scripts/scan.sh trivy evidence/local
uv run --frozen python scripts/check_reports.py evidence/local
```

Semgrep uses `p/python` and `p/security-audit`; metrics and version checks are disabled. The scanner image is digest-pinned, but upstream rule packs can change: the raw report preserves executed rule details and rule IDs. Trivy inventories locked Python dependencies and the built container; its vulnerability DB changes over time. Reports therefore identify one real run, not a promise that later counts are identical. Tooling downloads are allowed during scans, while domain runtime dependencies remain isolated.

Findings are non-blocking in week 1. Failed scanner commands, empty/invalid reports, failed builds and failed tests block the pipeline. The scripts use `set -euo pipefail`; there is no blanket `continue-on-error`. Scans do not upload code to a hosted Semgrep account, and do not require a Semgrep/Trivy token. Trivy uses a named scanner cache volume. The temporary local image archive is deleted after scanning.

Raw local results live in ignored `evidence/local/`, preventing large reports and archives from polluting the source history. GitHub Actions uploads that directory as a run artifact even on failure. The student must download the successful run's artifact into `evidence/github/`, preserve the chosen reports under the tracked `evidence/submission/` directory, and update the execution log before tagging. See `SUBMISSION.md`.

## Dependency updates

The checked-in `uv.lock` pins Python dependency versions and hashes; the Docker build uses its exported, hash-checked production requirements. To deliberately update dependencies:

```bash
uv lock --upgrade
uv export --frozen --no-dev --no-emit-project --no-header --output-file requirements.txt
```

Then rerun tests, build and scans, and record the change. CI checks that the export agrees with the lockfile.

## Phase boundary

The professor will choose a standardized service blueprint after week 1. Preserve this release as the Phase 1 proposal, then adapt future code to that blueprint. Keep future naive/secure experimental versions distinct and retain prompts and evidence. No frontend, production deployment, live external API integration or advanced auth module is needed for this submission.
