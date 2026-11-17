# AI Deliverable Metadata Block

AI authorship and analysis: 100%; human refactoring: 0% at creation. Audit date: November 17, 2026 IST. Student review pending. Prompt and output log: `.ai_logs/prompt-history.md`.

# PA2 deliverables audit

Source: `support/CS763_ProjectDescription.pdf`, pages 3–5, and the professor's notice requiring fresh assignment source and allowing separate assignment folders. This is a review of files and existing evidence, not a new runtime test run.

**Overall: implementation and local evidence are present; final student/provenance/release steps remain.**

| Required item | Status | Evidence / remaining action |
| --- | --- | --- |
| Fresh Domain 1 implementation from master blueprint | Present | `functional-codebase/`; PA1 source retained separately; project/artifact CRUD, searches, manuscript binaries/hash/ZIP |
| Production and test code; passing happy paths | Verified locally | 11 local and 11 PostgreSQL API tests in JUnit XML; evidence checker passes; source hashes unchanged |
| Functional-only baseline generation prompt | Qualified | `.ai_logs/functional-brief.md` is explicitly an internal construction brief in an existing security-aware chat, not an independently submitted functional-only student prompt. Do not represent a clean isolated experiment. If the instructor requires stricter generation provenance, obtain acceptance or perform a fresh correctly logged run. |
| Architectural header on every code asset, including human verification trail | Partial | Stack/AI attribution present; human-review statements still say pending. Student must record actual review, not merely automated test results. |
| Semgrep and SonarQube execution/raw logs | Verified locally | Actual JSON/log exports; both SAST tools returned zero findings. No remote CI run is claimed. |
| True-positive / false-positive ledger | Present | `sast-triage-report.md` records zero scanner alerts to classify and distinguishes manual findings and source-review negatives. No artificial false positives were invented. |
| Minimum 3 distinct cross-layer weaknesses, precise CWE and root causes | Present with validation limit | V1 CWE-306: unauthenticated mutation; V2 CWE-770: absent application resource limits; V3 CWE-362: concurrent revision loss. V2 combines source review and bounded 4 MiB acceptance; it does not demonstrate actual exhaustion. V1/V3 have real HTTP impact evidence. |
| Security requirements | Present | SR1–SR10 in `security-analysis.md` |
| Abuse cases and attack trees for at least 3 cases | Present | AC1–AC3 and three Mermaid trees |
| Attack-surface map and risk priorities | Present | Route/verb, persistence, tooling and evidence inventory |
| Comprehensive DFD and STRIDE for every component | Present | 10 component rows, all six STRIDE categories, trust boundaries/data flows |
| Proposed mitigations | Present | Requirement acceptance checks, per-finding fixes and T1–T12 treatment register |
| AI metadata blocks/contribution percentages | Present; review pending | Both graded reports start with metadata; active selector confirmed as 6.1 / Medium |
| Prompt appendix/export or permitted manual fallback | Manual fallback present | Dated `.ai_logs/prompt-history.md`; native export not supplied. Preserve its disclosed limitations; add a scrubbed task-scoped export if available. |
| Graded conceptual journal (14%) | Incomplete | `.ai_logs/conceptual_journal.md` is a worksheet with pending student reflections, not a completed journal |
| AI/HUMAN/HYBRID commit trace | Incomplete | PA2 directory and workflow are untracked; no PA2 commit yet |
| PA2 release/git tag including previous assignments | Missing | Local tags and public GitHub releases showed only PA1 at audit time |
| Blackboard short summary with actual release URL | Missing | Draft in `SUBMISSION.md`; actual release URL must replace placeholder |

## Release identity

- Recommended GitHub release title: **`project-assignment-2`**.
- Recommended Git tag: **`assignment-2-v1.0.0`**.
- Reason: matches observed PA1 title `project-assignment-1` and tag `assignment-1-v1.0.0`. The rubric does not prescribe an exact literal title.
- The PA2 workflow already accepts `assignment-2-*` tags. Tag the final reviewed commit containing PA1 and PA2, not the PA1 commit.
- Public release check on November 17 found only https://github.com/Glitch18/artifact-indexer/releases/tag/assignment-1-v1.0.0 . GitHub CLI was not authenticated, so no private/draft-release or remote-run claim is made.

## Submission order

1. Complete personal code review and journal; resolve any stricter functional-prompt provenance requirement.
2. Commit PA2 and its workflow with accurate contribution tags; retain prior assignments.
3. Run the real GitHub Actions workflow and retain its actual evidence/run URL. Reconcile any differences from local results.
4. Create `assignment-2-v1.0.0` and the `project-assignment-2` release targeting the final reviewed version.
5. Submit the actual release URL and short summary through Blackboard.

No release or remote mutation was performed during this audit.
