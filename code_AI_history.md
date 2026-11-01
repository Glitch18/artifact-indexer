# AI Usage Log

Conceptual contribution and prose: 100% AI generated / 0% human refactored at initial creation. Exact prompts: `docs/prompts.md`, P1-P6. This is the task-scoped interaction/change history, maintained alongside the initial prompt test.

# Code and design AI history

## Entry 1 - November 1, 2026 - week-one generation

- Agent: running OpenAI Codex desktop session; observed configuration in `Agent_environment.md`.
- Input prompts: P1-P3; P4 reserves all GitHub work for the student; P5 confirms the active model and reasoning effort.
- Design before source generation: `spec.md` with proposed REST contracts, metadata schemas, entity relationships, fixture boundary, acceptance criteria and phase separation.
- Generated source: `app/__init__.py`, `app/main.py`, `tests/test_readiness.py`, `scripts/smoke.py`; infrastructure/scanning files and dependency manifests; synthetic reference fixtures.
- Generated documentation: README, specification, agent environment, prompt appendix, prompt test log, pipeline evidence log, this history, submission instructions.
- AI contribution to authored code/configuration/docs: 100%; human manual refactoring: 0% during this entry. Dependency lockfiles are tool-generated, not manually authored. Human planning prompts and domain choice are disclosed in the prompt appendix rather than counted as manually written code.
- Verification: exact outcomes and corrections are recorded in `Pipeline_execution_log.md`. The file is updated after verification, without claiming success from an attempted command.
- Native conversation export: not produced by the tool interface. This appendix contains the exact task-relevant student prompts, implementation changes, source output, and evidence references; it does not claim to contain hidden prompts or internal reasoning.

## Entry 2 - November 1, 2026 - verification-driven corrections

- Agent, authorship split and original authorization unchanged. No separate student prompt was fabricated for iterative fixes.
- Ruff formatted generated Python. The Docker requirements export was made independent of the local machine path.
- A real Docker smoke check found that the API's internal-only bridge did not publish a usable localhost port on this engine. Updated Compose with an API-only ingress bridge while retaining the DB-only internal bridge; updated the architecture prose to match. Host HTTP and real PostgreSQL readiness passed afterward.
- Verified actual DB outage behavior, then restarted the DB and confirmed recovery. No unrelated containers/volumes were modified.
- Source headers, Markdown disclosures, fixture JSON, dependency export consistency and scanner-report error handling were checked. A temporary YAML parser checked workflow syntax without adding a runtime dependency.
- Docker, database and scanner images are pinned to observed immutable registry digests rather than guessed versions. Final scanner outcomes are recorded in `Pipeline_execution_log.md`.
- Real Semgrep and Trivy scans were executed. The final scanner-script rerun used the fixed file without in-flight edits; it and report validation passed. Semgrep reported 2 warnings in the local helper, dependency scans reported 0 findings, and the image scan reported 245 untriaged findings. No clean result or completed GitHub execution is claimed.

## Entry 3 - November 1, 2026 - local commit organization

- Student prompt P6 explicitly requests logical, atomic local commits after the student configured origin. Pushing, Actions runs and releases remain student-owned.
- Organized the initial files into five dependency-ordered commits: specification/fixtures, app/dependencies/tests, Docker/smoke checks, security workflow/scanner scripts, and submission/agent/evidence documentation.
- Updated the submission instructions to use the observed existing origin and avoid an unnecessary second initial commit or remote creation. Updated the pipeline log's local-commit description. No application or scanner behavior changed in this turn.
- Retained the required `AI AGENT BUILD:` commit prefix. No human-authored refactoring is claimed for agent-created files or documentation updates.

## Commit convention

Use `AI AGENT BUILD: <feature>` for agent-generated changes. Use `HUMAN MOD: <feature>` only for actual manual student code changes. Update file contribution weights if the student later edits code; a review without edits does not become human refactoring.
