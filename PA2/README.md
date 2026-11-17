# AI Deliverable Metadata Block

- Authoring tool: OpenAI Codex desktop, local single-agent session, 2026-11-17 (IST).
- AI conceptual/prose contribution: 100% at initial creation; human refactoring: 0% at creation.
- Student verification and final contribution assessment: **pending**; review is not authorship.
- Prompts and output history: [.ai_logs/prompt-history.md](.ai_logs/prompt-history.md); [construction brief](.ai_logs/functional-brief.md).
- Native session export/share link: not supplied. Dated manual history is included; add the native export if available.

# Project Assignment 2 — Domain 1

This directory is a fresh implementation of the professor's Domain 1 master specification. The Assignment 1 source remains at the repository root. Only configuration ideas and the existing stack were reused. No PA1 source was copied into `functional-codebase/app`.

## What to submit

| Item | Weight | Location |
| --- | --- | --- |
| Functional source and tests | 20% | `functional-codebase/` |
| SAST triage | 20% | `sast-triage-report.md`, `evidence/` |
| Security analysis | 40% | `security-analysis.md` |
| AI logs and critical reflection | 20% | `.ai_logs/`, metadata blocks and source headers |

The source is intentionally preserved as the generated functional baseline. Audit findings are documented, with fixes proposed for PA3. The baseline is for isolated local course use. Docker exposes the API only on `127.0.0.1:8002`; the database is not host-published.

## Run and verify

From the repository root:

```bash
cd PA2/functional-codebase
uv sync --frozen
uv run --frozen pytest -q --junitxml=../evidence/pytest-local.xml
cd ..
docker compose build
docker compose up -d --wait --wait-timeout 120
cd functional-codebase
PA2_BASE_URL=http://127.0.0.1:8002 uv run --frozen pytest -q --junitxml=../evidence/pytest-postgres.xml
cd ..
functional-codebase/.venv/bin/python scripts/validate_findings.py
bash scripts/scan_semgrep.sh
bash scripts/scan_trivy.sh
python3 scripts/scan_sonar.py
python3 scripts/fingerprint.py
```

Open `http://127.0.0.1:8002/docs` for OpenAPI. Source dependencies are locked in `uv.lock`; the Docker build installs the hash-checked `requirements.txt` export. Unit/in-process tests use isolated SQLite fixtures. The same API suite against port 8002 exercises PostgreSQL in Compose.

`validate_findings.py` modifies and removes only its own fictional fixture. Its concurrency result can vary; a failed reproduction must be investigated, not reported as success. The bounded upload is 4 MiB; it does not attempt to exhaust the host.

Scanners run locally; no hosted SonarCloud or Semgrep code-upload service is used. `scan_sonar.py` starts a dedicated throwaway evaluation server if absent, creates/revokes an ephemeral scan token, and exports analysis results. The local server uses H2 for evaluation only. The script uses only its own container/network names. Stop it and the application after review:

```bash
docker compose down
docker stop cs763-pa2-sonar
docker rm cs763-pa2-sonar
docker network rm cs763-pa2-scanners
```

Named PA2 application volumes are retained. Avoid adding `-v` unless you intend to delete your local PA2 data.

## Contract clarifications

- Artifact types are plural path literals: `manuscripts`, `videos`, `repositories`. UUIDs identify projects and artifacts independently.
- PUT replaces project fields or artifact metadata; project revision starts at 1 and increments on PUT. Artifact/file changes have their own timestamps and do not increment the project revision in this baseline.
- Project members are `{id, role}` dictionaries; academic units are `{type, id}` dictionaries with types `lab`, `department`, and `course`. At least one member and unit is required. The fixtures in `functional-codebase/fixtures/reference-data.json` are fictional external references; there are no cross-service calls.
- Search predicates combine with AND; keyword searches title/description case-insensitively. Time bounds are inclusive ISO timestamp string comparisons against `created_at`; clients use normalized UTC ISO strings. `artifact_type` filters for at least one artifact of that type. No date parsing guarantee beyond that convention is claimed.
- Manuscript metadata fields: title, abstract, authors, keywords, year, publisher. Repository fields: repo_url, target_branch, primary_tech_stack, total_commit_count, latest_commit_timestamp. Video fields: video_url, thumbnail_url, duration (seconds), description. Metadata dictionaries are stored as supplied; per-type semantic schemas are a documented audit gap.
- Create manuscript metadata before uploading its binary multipart `file`. Stored filenames are server-generated artifact UUIDs. A binary can be replaced, downloaded, or removed while metadata remains. SHA-256 identifies the uploaded bytes; it is not a signature or authorship proof.
- ZIP download is the fixed `/artifacts/manuscripts/download` route. Entries are `<artifact UUID>/<basename>` to distinguish duplicate filenames. Empty projects produce an empty ZIP. URLs are stored, not fetched.
- The framework's OpenAPI/docs and `/healthz` endpoints are also exposed entry points. No authentication module or identity-provider implementation is included in PA2.

## Professor's mock issuer notice

The supplied v1.0.0 README identifies the tool as a **PA3 test aid**. It was made with Claude Code assistance; the professor states he reviewed/tested it. We read its README and retained the reference in `support/`. We did not execute, incorporate, or claim to verify its code in PA2. For PA3, use its signing keys/JWKS and negative tokens instead of building an identity provider; keep it localhost-only, keep keys and generated tokens out of Git, review its code, and run its tests first. Its `decode` command does not verify signatures. No generated key or token is included here.

## Remaining student-owned work

See `SUBMISSION.md` for personal review, conceptual reflection, provenance checks, and GitHub/Blackboard release steps. This package is not represented as submitted or fully human-verified.
