# AI Usage Log

Conceptual contribution and prose: 100% AI generated / 0% human refactored at initial creation. Exact student prompts: `docs/prompts.md`, P1-P6. The student requested manual ownership of GitHub operations and subsequently authorized the agent to create local commits. Commands below are instructions for the student, not remote actions the agent has performed.

# Assignment 1 - manual submission checklist

The local project is in `artifact-indexer/`. Publish **this folder as the repository root** so `.github/workflows/devsecops.yml` is at the GitHub root. Do not publish the parent `cs763/` directory, the course PDF, private chats/configuration, `.venv`, caches or Docker archives.

## 1. Review and confirm

- Read `spec.md` and confirm the proposed Domain 1 requirements. The domain entry is already registered, per the student.
- Active model/effort are confirmed by the student as `gpt-6.1-sol` / `medium` and recorded in `Agent_environment.md`. If you use another agent or change settings later, update that record and the interaction history.
- Review AI disclosures. Retain the exact prompt appendix and source headers. If you edit code yourself, update contribution weights and `code_AI_history.md` honestly.
- Check Blackboard's actual due date and any instructor announcements; the course PDF provides weeks, not calendar deadlines.

## 2. Push the prepared local commits

The student configured origin as `git@github.com:Glitch18/artifact-indexer.git`. The agent prepared five local commits on `main`; no additional initial commit or remote setup is needed. Confirm the GitHub repository is public as required by the assignment, then run:

```bash
cd /Users/atharva/Documents/ms/cs763/artifact-indexer
git status
git log --oneline --reverse
git remote -v
git push -u origin main
```

The existing origin is preserved. If GitHub already has commits, inspect that history before reconciling it; do not force-push blindly. SSH authentication for the push remains the student's responsibility.

## 3. Run and preserve GitHub Actions evidence

The push to `main` triggers **DevSecOps**. In GitHub's Actions tab, open that exact commit's run. It must succeed, including container readiness and both scanners. The full workflow has not been verified on GitHub until you do this.

1. Download `devsecops-evidence-<run_id>-<attempt>` from the successful run. Extract it into the ignored `evidence/github/` directory. If there are repeated runs, retain which attempt supplied the chosen data.
2. Create `evidence/submission/` and copy the run's `source-commit.txt`, `run-started.txt`, `scan-summary.json`, `semgrep.json`, `trivy-dependencies.json`, `trivy-image.json`, scanner `.log` files, `smoke.log`, `tests.log`, `docker-build.log`, and `compose-status.txt` into it. These are generated evidence files, not authored Markdown deliverables. Review all logs for unrelated/private data before publishing.
3. In `Pipeline_execution_log.md`, record the actual workflow URL, run ID/attempt, source commit, result, scanner counts and evidence paths. Distinguish scanned commit from the subsequent documentation/evidence commit.
4. Update `code_AI_history.md` for human documentation changes; do not label an agent-generated commit as manually refactored code.
5. Commit these evidence/docs changes and push them. The source workflow will run again; confirm success. The evidence commit's predecessor is the recorded scanned source commit; if code/configuration changed too, collect new evidence for that code instead.

Local Docker/scanner evidence is useful but does not replace the specifically required GitHub Actions execution log. No pipeline URL or success is pre-filled.

## 4. Create the submission release

Only after the files and verified pipeline evidence are committed:

```bash
git add Agent_environment.md Pipeline_execution_log.md code_AI_history.md evidence/submission
git status
# Commit any remaining reviewed changes if necessary; avoid empty commits.
git tag -a assignment-1-v1.0.0 -m "CS763 Project Assignment 1"
git push origin assignment-1-v1.0.0
```

The tag push also triggers CI. Verify that run succeeds. In GitHub Releases, create a release from `assignment-1-v1.0.0`, titled `Project Assignment 1 - Service Definition and DevSecOps Pipeline`. Include the successful Actions run link and optionally attach the raw evidence archive. Do not move the submitted tag silently; create a new version if fixes are needed.

## 5. Blackboard submission draft

Replace placeholders with verified links; do not submit placeholders:

> Domain 1: Project Artifact & Repository Indexer. The Assignment 1 release contains the proposed REST/API and database specification, documented Codex agent environment and prompt test, a multi-stage Docker/FastAPI skeleton with isolated PostgreSQL, and a GitHub Actions DevSecOps pipeline with Semgrep and Trivy telemetry. The pipeline execution evidence is included with the release. Functional domain implementation will follow the professor's standardized blueprint in Assignment 2.
>
> Release URL: [paste actual GitHub release URL]
>
> Verified pipeline run: [paste actual successful Actions run URL]

Submit the short summary and **release URL**, not only the repository homepage, on Blackboard.
