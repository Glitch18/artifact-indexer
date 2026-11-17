# AI Deliverable Metadata Block

- Tool: OpenAI Codex desktop, local single-agent session; date: 2026-11-17 IST.
- AI conceptual/prose contribution: 100%; human refactoring at creation: 0%.
- Student source review, interpretation and final contribution assessment: **pending**.
- Prompt appendix: [../.ai_logs/prompt-history.md](../.ai_logs/prompt-history.md), [functional brief](../.ai_logs/functional-brief.md).
- This is an AI-authored audit validated by recorded local checks, not a claim of completed human review.

# Execution evidence

Local runs are dated November 17, 2026 IST. Tools record UTC timestamps (the manual check began November 16, 2026 at 20:31:48 UTC, corresponding to November 17 at 02:01:48 IST). These are local execution artifacts, not fabricated GitHub Actions results.

- `pytest-local.xml`: 11 passing in-process tests with temporary SQLite data.
- `pytest-postgres.xml`, `tests-postgres.log`: the same 11 tests pass against Docker/FastAPI/PostgreSQL.
- `manual-validation.json`: real HTTP observations for V1–V3, using only fictional local data. Fixture cleanup returned 204. Its original V2 mapping was CWE-400; the final report refines it to CWE-770.
- `semgrep.json`, `semgrep.log`, `semgrep-version.txt`: actual scanner output, not a manually constructed alert set.
- `sonar-*.json`, `sonar-scanner.log`: completed SonarQube analyses and API exports. No security issues or hotspots were returned by the active core profile. Initial export API errors were repaired; analysis success and export success are distinct in the history.
- `compose-up.log`, `compose-status.json`, `compose.log`, `docker-build.log`, `image-inspect.json`: actual dedicated stack and image evidence. The saved build log is a successful cached rebuild of the same source after the initial successful build.
- `source-sha256.json`: hash manifest of baseline source, tests, configuration, dependency locks, fixtures and README. No hidden virtual environment or live data is included.
- `trivy-dependencies.json` and `trivy-image.json`: completed dependency/image scans, with 0 Python dependency alerts and 271 image package/advisory instances (139 unique IDs). See the triage report for severity counts and limits; these are not counted as the three manually validated source weaknesses.

GitHub run URL and release URL are not yet available. Download the real CI artifact after your push and add its actual run reference before tagging. Never replace local provenance with an invented remote execution claim.
