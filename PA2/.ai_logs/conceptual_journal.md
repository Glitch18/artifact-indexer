# AI Deliverable Metadata Block

- Authoring tool: OpenAI Codex desktop, local single-agent session, 2026-11-17 (IST).
- AI conceptual/prose contribution: 100% at initial creation; human refactoring: 0% at creation.
- Student verification and final contribution assessment: **pending**; review is not authorship.
- Prompts and output history: [.ai_logs/prompt-history.md](.ai_logs/prompt-history.md); [construction brief](.ai_logs/functional-brief.md).
- Native session export/share link: not supplied. Dated manual history is included; add the native export if available.

# Conceptual journal — student completion required

This is an AI-authored review worksheet, not a fabricated first-person student journal. Replace the pending sections with your actual dated reasoning and preserve authorship history.

## Entry 1 — scope and experimental design (2026-11-17)

Observed agent actions: read the current assignment and Domain 1 blueprint; preserved PA1; generated a fresh PA2 service; retained an internal functional construction brief; disclosed inherited security context rather than claiming an isolated experiment.

**Your reflection :** A fresh functional baseline matters because PA2 should examine a newly generated implementation of the functional specification, rather than inherit PA1’s code and security decisions. Preserving that baseline also gives us a stable reference for evaluating PA3’s mitigations. However, fresh code does not mean a fresh experimental context. The disclosed prior security discussion could have influenced the AI’s implementation choices even without copying source code or deliberately planting vulnerabilities. I would therefore treat this as a documented case study, rather than a controlled comparison that isolates the effect of security prompting.

I accept reasonable contract conventions such as plural artifact routes, independent project and artifact UUIDs, AND-combined search filters, and creating manuscript metadata before uploading its binary. Using artifact UUIDs in ZIP paths also makes sense because it avoids collisions between identical filenames. These choices make the service’s behavior explicit without substantially changing its purpose.

I would ask the professor whether artifact or file changes should increment the parent project’s revision, whether PUT requires complete replacement of all relevant fields, and what validation is required for each artifact type’s metadata. I would also clarify whether timestamp filters must parse and normalize dates rather than depend on consistently formatted UTC strings, and whether fictional local affiliation references satisfy the expected integration scope. Finally, I would confirm that authentication is deferred to PA3. Documenting an assumption makes it reviewable, but does not establish that it satisfies the specification; similarly, missing validation remains an audit finding even when its current behavior is documented.

## Entry 2 — review the code rather than trust the output

Observed automated checks: local API suite and real PostgreSQL API tests; see evidence for exact outcomes. The suite covers happy paths; it is not proof of security.

**Your reflection:** On 17 November 2026, I reviewed create_app.<locals>.update_project and create_app.<locals>.upload in [PA2/functional-codebase/app/main.py (line 153)](/Users/atharva/Documents/ms/cs763/artifact-indexer/PA2/functional-codebase/app/main.py:153).

For project updates, update_project loads the project through get_project, replaces the fields from the validated request, increments the revision, updates the timestamp, and commits the transaction. I questioned whether project.revision += 1 reliably preserved revision history under concurrent requests. The AI’s audit explanation was correct: a transaction alone does not prevent two requests from reading the same revision and writing the same incremented value. I checked the ordinary integer revision column, the absence of a version condition or explicit row lock, and the recorded PostgreSQL validation. Twelve successful updates advanced the revision from 2 to 5 instead of 14, supporting the lost-update finding.

For manuscript uploads, upload checks that the artifact belongs to the specified project and is a manuscript, reads the entire file, writes it under the artifact’s UUID, records its original filename, SHA-256 hash, size, and timestamp, then commits. I accept the server-generated storage filename because it keeps the supplied filename out of the storage path. However, the whole-file read has no application-level size bound, and the filesystem write and database commit are separate operations. The AI’s resource-risk assessment is supported by this implementation, although the successful 4 MiB test does not demonstrate exhaustion. This review helped me distinguish functional correctness from concurrency, resource, and failure-handling guarantees.

## Entry 3 — scanner limitations and validation

Observed audit: Semgrep initially reported zero alerts, while manual HTTP checks found unauthenticated changes, unrestricted whole-file buffering, and lost revision updates. Read the final Sonar ledger before writing your conclusions.

**Your reflection:** A clean automated scan did not establish safety because it only showed that the configured rules found no reportable issues in the scanned code. Semgrep returned zero findings, and SonarQube reported zero issues or hotspots, but neither result demonstrated that the service enforced its intended security policy. The manual checks exposed gaps involving caller identity, resource limits, and concurrent updates. This showed me why scanner results need to be combined with source review and tests of how the service can be misused.

I consider unauthenticated modification the most important finding for the intended multi-user service. The recorded test showed that a client sending no Authorization header could replace the title of an Alice-associated project, and the changed title persisted. Project membership data therefore did not establish who was making the request or whether they had permission. This directly threatens the integrity of the project records. The current localhost binding limits exposure, but authentication and permission checks would be essential before broader deployment.

The bounded resource test is not sufficient to claim host exhaustion. It demonstrated that the service accepted and stored a 4 MiB upload with a matching size and hash. Source review also identified whole-file buffering and missing application-level upload and archive limits. Together, these support a resource-consumption concern, but they do not establish a crash, memory exhaustion, unlimited capacity, or a denial-of-service threshold. Measuring those effects would require separate, controlled testing with resource monitoring and explicit limits.

## Entry 4 — proposed hardening and future measurement

**Your reflection:** I would prioritize spoofing, tampering, and denial of service, because they directly affect who can use the service, whether project records remain trustworthy, and whether the service stays available.
For spoofing, the trust boundary is between an untrusted HTTP caller and the API’s authenticated identity. PA3 should verify JWT signatures using trusted configured keys and validate the allowed algorithm, issuer, audience, and expiry. I would test that a valid token succeeds while missing, expired, incorrectly signed, and otherwise invalid tokens fail. Authentication must establish identity before the service makes permission decisions.

For tampering, the boundary is between a caller’s requested changes and the authoritative project records in PostgreSQL. A valid identity should not automatically grant permission to modify every project. I would test that Bob cannot modify Alice’s project or grant himself access through submitted membership fields. I would also verify revision conflict handling: two writes based on the same revision should produce one accepted update and one conflict response, rather than silently overwrite an edit.
For denial of service, the boundary is where untrusted uploads and archive requests consume server memory, disk, and CPU. I would introduce upload limits, storage quotas, bounded concurrency, and streaming processing. Verification would include requests just below and above configured limits, cleanup after rejected uploads, and controlled concurrent requests with resource monitoring.

I would implement and test these changes in a separate PA3 branch or directory, preserving PA2’s source hashes, evidence, and release reference for comparison. The professor’s mock token issuer supplies test keys, JWKS, and valid and invalid tokens; it stands in for an external identity provider. My responsibility is to validate tokens and authorize requests in the service, rather than build login flows or an identity provider. Its token-decoding command alone does not verify signatures.

## Prompt / verification trail

Add each substantive new prompt and a concise output/evaluation summary with a date. Record any mistaken AI claim or hallucinated setting you actually encounter; do not invent one for the rubric. Keep secrets, private keys and live tokens out of this journal.
