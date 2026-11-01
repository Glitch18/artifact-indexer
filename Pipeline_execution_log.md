# AI Usage Log

Conceptual contribution and prose: 100% AI generated / 0% human refactored at initial creation. Exact student prompts: `docs/prompts.md`, P1-P5. Values below refer to commands actually executed by the running agent, except the explicitly pending GitHub section. Raw scanner reports are machine generated.

# Pipeline execution evidence - Assignment 1

## Evidence boundary

The student reserved GitHub publishing and Actions runs for manual execution. The local checks below validate this machine's source, Docker build, Compose stack and scan commands. **A successful GitHub Actions execution has not yet been observed.** This submission is not fully ready to submit until the student adds that run and creates the release.

Run date: November 1, 2026. Host: macOS 26.6.2 / arm64; Docker Linux/arm64. GitHub's configured runner is Ubuntu 24.04 / amd64, so its container build is a separate verification. Code and dependency files identify what was tested; the agent organized local commits at the student's explicit request (prompt appendix P6). Pushing and GitHub execution remain student-owned.

## Local results

| Check | Result / evidence |
| --- | --- |
| CPython environment | 3.13.12; dependencies resolved and installed with uv 0.13.5 |
| Ruff lint | Passed; `evidence/local/lint.log` |
| Ruff format | Passed for authored Python files |
| Pytest | 2 passed; `evidence/local/tests.log`, `pytest.xml` |
| Fixture and manifest checks | JSON/TOML parsed; fixture IDs unique per collection |
| Authorship disclosures | Authored Python files have AI contribution headers; authored Markdown starts with AI Usage Log |
| Workflow YAML | Parsed with temporary PyYAML; workflow uses read-only contents permission |
| Scanner failure behavior | Report validator rejects missing reports and synthetic scanner errors; accepts synthetic reports with findings. Synthetic controls are not scanner evidence. |
| Dependency export | Production `requirements.txt` matches a fresh frozen export from `uv.lock` byte for byte |
| Docker/Compose | Multi-stage build passed; API runs as UID/GID 10001:10001; API and DB healthy; `evidence/local/docker-build.log`, `compose-up.log`, `image-inspect.json` |
| HTTP smoke checks | `/healthz` and real-SQL `/readyz` returned 200; OpenAPI exposes only those two paths; `evidence/local/smoke.log` |
| Actual DB outage/recovery | With this project's DB stopped, liveness stayed 200 and readiness returned generic 503. DB restarted and full smoke checks passed again; `evidence/local/outage-check.log`, `outage-control.log`, `smoke.log` |
| Semgrep | 1.182.1; 200 rules executed, 5 targets scanned, 2 WARNING findings, no scanner errors, command exit 0; `evidence/local/semgrep.json`, `semgrep.log`, `semgrep-version.txt` |
| Trivy dependency scan | 0.76.1; 2 targets (`requirements.txt`: 21 packages, `uv.lock`: 22 packages), 0 reported vulnerabilities; successful command and valid JSON; `evidence/local/trivy-dependencies.json`, `.log` |
| Trivy image scan | 0.76.1; Debian 12.15 and Python package targets; 245 raw findings: 2 CRITICAL, 56 HIGH, 95 MEDIUM, 90 LOW, 2 UNKNOWN; successful command and valid JSON; `evidence/local/trivy-image.json`, `.log` |
| Combined report validation | Passed; actual counts saved in `evidence/local/scan-summary.json`. Findings did not fail the command. |

Test warning: the resolved Starlette version emits a deprecation warning about its httpx-based TestClient. Both tests pass; this is not a test failure. Future dependency updates should revisit it.

Semgrep's two findings are `python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected`, both in the local smoke helper's URL calls. They ask for review of dynamic urllib URLs. The helper defaults to localhost and takes its optional base URL from the operator environment; it is not an exposed application route. Preserve these raw findings rather than calling the run clean or silently suppressing them. Formal triage of the later functional baseline belongs to Assignment 2. Semgrep's summary labels findings "blocking", but `semgrep scan` without `--error` returned 0; the week-one workflow intentionally treats findings as telemetry. The default Semgrep ignore rules excluded the test file; the raw `paths.scanned` list is authoritative.

Trivy's raw image findings comprise 237 Debian package findings and 8 Python package findings. The latter name msgpack, setuptools and urllib3; these are not the application packages listed in the production requirements export. These are scanner alerts, not 245 confirmed exploitable application flaws. No suppression, blanket `ignore-unfixed`, or fabricated clean report was applied. The dependency scan warns that license detection cannot locate site-packages in the scanner container; vulnerability inventory still succeeds for both the requirements and uv lockfile targets. The scan intentionally excludes development dependencies by Trivy's default; do not describe it as a dev-tool audit.

Successful final Trivy run timestamps from the JSON: dependency scan `2026-11-01T10:42:30Z`, image scan `2026-11-01T10:42:31Z`. The image scan identified the pinned Python base with Debian 12.15. Exact tool/image identities are in `Dockerfile`, `docker-compose.yml`, `scripts/scan.sh`, and the local version/inspect files. Vulnerability DB/rule changes and the amd64 GitHub runner can produce different later counts.

## Corrections during generation

- Docker socket and package-index access required sandbox escalation; Docker daemon access was verified afterward.
- Python PDF extraction used the bundled `pypdf` after PyMuPDF was unavailable. This affected source reading only, not the application.
- The requirement export was regenerated without a machine-specific command header. Dependencies and hashes remain generated from `uv.lock`.
- Ruff reformatted test/report-validation files before the final format check.
- Scanner reports are checked independently of vulnerability counts, so a scanner crash cannot be mistaken for clean results.
- Initial Docker host-port access failed when the API joined only an internal bridge. Added a separate project-specific ingress bridge for the API; PostgreSQL remains only on the internal network. Actual host HTTP, SQL readiness and DB outage/recovery checks then passed. The initial failed smoke attempt is not counted as a successful verification.
- GitHub automation was prepared but not executed, per the student's explicit instruction.
- While the initial Trivy process was downloading its DB, the scanner script was edited to finalize flags/digests. Editing that running shell file caused a trailing shell parse error after scans; it was not accepted as success. The finalized script passed `bash -n` and was rerun without edits using the downloaded DB cache. Both Trivy commands and combined JSON validation then exited 0; the final logs/reports above are from that successful rerun.

## GitHub Actions - pending student run

- Repository URL: **PENDING**.
- Workflow run URL / run ID / attempt: **PENDING**.
- Source commit scanned: **PENDING**.
- UTC run timestamp: **PENDING**.
- Build / test / smoke / scanner result: **PENDING**.
- Scanner versions and finding counts: **PENDING actual Actions artifact**.
- Checked-in evidence paths: **PENDING `evidence/submission/`**.
- Submission tag / release URL: **PENDING**.

Follow `SUBMISSION.md`. Download the actual run artifact, preserve raw JSON/logs, replace these fields with observed values and distinguish the scanned source commit from later evidence-only commits. Do not copy local results into these fields as if GitHub produced them.
