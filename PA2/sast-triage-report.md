# AI Deliverable Metadata Block

- Tool: OpenAI Codex desktop, local single-agent session; date: 2026-11-17 IST.
- AI conceptual/prose contribution: 100%; human refactoring at creation: 0%.
- Student source review, interpretation and final contribution assessment: **pending**.
- Prompt appendix: [.ai_logs/prompt-history.md](.ai_logs/prompt-history.md), [functional brief](.ai_logs/functional-brief.md).
- This is an AI-authored audit validated by recorded local checks, not a claim of completed human review.

# SAST triage and manually validated weaknesses

## Scope, source and procedure

Target: `functional-codebase/app` and `functional-codebase/tests`; dedicated localhost PA2 containers for runtime validation. The baseline was preserved during audit. `evidence/source-sha256.json` identifies the exact source files; `evidence/image-inspect.json` identifies the built image. All report locations refer to `functional-codebase/app/main.py` unless stated otherwise. No customer/peer production system was used.

Procedure: run Semgrep and SonarQube; retain raw reports; inspect actual sources and sanitization/data-flow boundaries; classify scanner alerts without equating quality warnings to vulnerabilities; manually test cross-layer design gaps; map confirmed defects to an appropriate CWE with root-cause evidence. A finding not emitted by a scanner is labeled manual. Source coverage and rule/profile limits matter even when the quality gate passes.

## Raw scanner ledger

| Tool | Executed scope / configuration | Actual result | Disposition |
| --- | --- | --- | --- |
| Semgrep | Digest-pinned local container; `p/python`, `p/security-audit`; metrics/version checks disabled | 200 rules; zero findings; zero report errors | No reported true/false positives; no alerts were invented for the ledger |
| SonarQube | Community Build **26.11.0.134175**, SonarScanner CLI **8.4.0.16527**; `Sonar way core` Python profile; sources `app`, tests `tests`; Python 3.13 | Completed analysis; quality gate PASSED; 202 non-comment source lines; **0 issues / 0 hotspots** | No reported true/false positives; core-profile coverage is not a complete application security assessment |

Evidence: `semgrep.json`, `semgrep.log`, `sonar-scanner.log`, `sonar-issues.json`, `sonar-hotspots.json`, `sonar-measures.json`, `sonar-analyses.json`, `sonar-run.json`. Sonar's scanner image was amd64 on an arm64 Docker host; its platform warning is retained. The scan completed successfully under that environment. Three completed Sonar analyses exist because report-export API troubleshooting caused repeated analyses; no baseline source change occurred between them. The final API export is complete for the returned counts.

**False-positive count: 0 reported alerts to classify.** Do not describe the following rejected hypotheses as scanner-generated false positives. They are source-review negatives:

| Hypothesis examined | Why not confirmed |
| --- | --- |
| SQL injection through keyword f-string | The f-string supplies a bound value to SQLAlchemy `ilike`; it is not interpolated into executable SQL. `%`/`_` can broaden matching, but no SQL syntax execution was demonstrated. |
| Filesystem traversal through upload filename | Stored path uses a server-generated artifact UUID. The original filename is metadata; download/ZIP names use `Path(...).name`. No user-selected server path was demonstrated. |
| Cross-project artifact access by swapping nested IDs | `get_artifact` checks project ID and artifact type; mismatched nesting returns 404. Caller authorization is still absent (V1). |
| Hardcoded local Compose credential is a leaked production secret | It is explicitly a public, dedicated course fixture credential with no host-published database port. Production secret management remains a proposed requirement. |

## Dependency / base-image telemetry (separate from SAST)

Trivy reported **0 Python dependency findings** and **271 image package/advisory instances spanning 139 unique vulnerability IDs**: 2 critical, 50 high, 120 medium, 93 low, and 6 unknown. These are package inventory matches from the pinned PA1-derived Debian/Python image; they are not 271 independently demonstrated application exploits and are not counted toward V1–V3.

The two critical-rated records concern `libsqlite3-0` / CVE-2025-7458 (status `affected`) and `zlib1g` / CVE-2023-45853 (status `will_not_fix`); neither record lists a fixed package version in this run. Exploit reachability and Debian vendor applicability have not been validated. Preserve the raw `trivy-image.json` and investigate package/advisory context before choosing a PA3 base-image refresh or claiming a specific runtime impact. The baseline image is not represented as suitable for deployment. Trivy findings are non-blocking experimental telemetry; scanner execution/export failures still fail CI.

## Confirmed manual findings across three layers

### V1 — Unauthenticated modification of authoritative project data

- **Primary CWE:** [CWE-306 — Missing Authentication for Critical Functionality](https://cwe.mitre.org/data/definitions/306.html).
- **Layer:** request identity/access control → project/member service → persisted data.
- **Location:** project POST at lines 120–126; PUT at 152–160; DELETE at 162–170. Artifact and manuscript handlers share the missing principal boundary. `get_artifact` at 87–92 checks nesting, not actor permissions.
- **Root cause:** mutating route dependencies provide only a database session. There is no authenticated principal, token verifier, or role/membership authorization decision before state changes. A submitted member list is not proof of caller identity.
- **Validation:** `scripts/validate_findings.py` created a fictional Alice-associated project, then a fresh client with no Authorization header read it (200) and replaced its title (200). `evidence/manual-validation.json` V1 records the persisted changed title and fixture membership. The fixture was removed afterward.
- **Impact:** any reachable caller can tamper with project content and membership or invoke destructive routes. Read confidentiality depends on the future public/private policy. Authentication and missing authorization are related here and are not double-counted as two independent findings.
- **Proposed fix:** central verified JWT identity plus object/role-level authorization on every mutation and protected read; derive subject from verified claims; audit decisions. Use the professor's local mock issuer in PA3 for positive/negative tests.
- **Suggested verification:** unauthenticated writes return 401; Bob cannot mutate Alice's project (403/404); authorized membership updates work; forged role fields do not grant privileges.
- **Priority:** high in a reachable multi-user service; current localhost binding limits exposure.

### V2 — Resource allocation lacks application-level upload and archive limits

- **Primary CWE:** [CWE-770 — Allocation of Resources Without Limits or Throttling](https://cwe.mitre.org/data/definitions/770.html), more precise than parent/general resource-consumption CWE-400.
- **Layer:** multipart input → process memory → filesystem / archive generation.
- **Location:** `upload` lines 223–235, particularly unbounded `await file.read()` at 226; `download_zip` lines 178–187 constructs the full archive in `BytesIO`. Search also retrieves unpaginated results at 139.
- **Root cause:** the service has no file-byte limit, aggregate storage quota, archive-size limit or request throttling. Spooling by the multipart parser does not prevent the handler from reading the entire spooled file into memory again. A streaming HTTP response does not undo construction of the ZIP in memory first.
- **Validation:** the bounded test sent 4,194,304 bytes and received 200 with matching stored size and hash. Source review confirms no application-level bounds. Raw V2 evidence retains the initial broad `CWE-400` label; this report refines the mapping to CWE-770 after reviewing MITRE. The validation script uses CWE-770 for subsequent runs.
- **Impact and limit:** large/repeated uploads or concurrent ZIP requests could consume process memory, disk or CPU. **The test did not crash the service, prove an infinite capacity, or measure a denial-of-service threshold.** Framework/OS limits are environmental constraints, not a documented service resource policy.
- **Proposed fix:** specify per-file/project/account limits; reject oversized bodies early; count bytes while streaming to staged storage; bound concurrency and archive totals; stream archives without retaining the entire output; paginate queries and monitor quotas.
- **Suggested verification:** configured limit+1 byte fails without an excess stored file; quota and archive limits are enforced; partial uploads clean up; concurrent bounded requests stay within measured budgets.
- **Priority:** medium/high depending on deployment and quotas; keep validation bounded and local.

### V3 — Concurrent project writes lose revision updates

- **Primary CWE:** [CWE-362 — Concurrent Execution Using Shared Resource with Improper Synchronization](https://cwe.mitre.org/data/definitions/362.html).
- **Layer:** concurrent HTTP handlers → ORM state → shared PostgreSQL row / revision history.
- **Location:** `update_project` lines 152–160: load at 154, increment of local state at 157, commit at 159. `revision` is an ordinary integer column, not an optimistic version column.
- **Root cause:** two transactions can read the same old revision, compute the same new value, and both commit. The write does not include a client expected-version predicate, atomic revision expression or explicit row-lock strategy. Each full replacement can erase a previously accepted edit.
- **Validation:** twelve simultaneous HTTP PUT requests all returned 200. Starting revision was 2; after 12 successful updates it should have been 14 if each increment were preserved, but the actual revision was 5. Raw responses and counters are in `manual-validation.json` V3. This tests the real PostgreSQL API, not a mock database. Scheduling affects future reproduction values.
- **Mapping rationale:** the observed defect is an unsynchronized shared database read-modify-write operation. CWE-362's class-level mapping is used with this specific evidence; no more specific permission-check TOCTOU scenario is claimed.
- **Impact:** silent loss of edits and inaccurate revision history undermine integrity and make changes harder to reconstruct. It does not establish code execution or privilege escalation by itself.
- **Proposed fix:** conditional UPDATE by expected revision with conflict response, or a deliberate serialized row-lock strategy. An atomic counter alone fixes the count but does not warn clients about overwritten edits.
- **Suggested verification:** two updates based on the same expected revision produce one accepted write and one 409/412 conflict; the accepted revision and audit event are consistent.
- **Priority:** medium integrity risk.

## Other threats not counted as confirmed vulnerabilities

The security analysis discusses generic metadata acceptance, file/database commit inconsistency, missing attributable audit logs, key/secret handling and supply-chain risks. These remain design gaps or proposed threats unless separately validated. No invented SAST alert, CVE identifier, exploit payload, or CVSS score has been used to reach the required count.

## Baseline preservation and remediation plan

Do not patch the PA2 experimental baseline in place. Prioritize V1, then resource controls and conflict handling in PA3; preserve source hashes, raw evidence and the release tag for comparison. The source has passed happy-path tests while remaining insecure under the proposed multi-user policy. That distinction is the central result of this audit.
