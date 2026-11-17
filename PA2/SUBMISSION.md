# AI Deliverable Metadata Block

- Authoring tool: OpenAI Codex desktop, local single-agent session, 2026-11-17 (IST).
- AI conceptual/prose contribution: 100% at initial creation; human refactoring: 0% at creation.
- Student verification and final contribution assessment: **pending**; review is not authorship.
- Prompts and output history: [.ai_logs/prompt-history.md](.ai_logs/prompt-history.md); [construction brief](.ai_logs/functional-brief.md).
- Native session export/share link: not supplied. Dated manual history is included; add the native export if available.

# Submission readiness and student actions

## Required personal completion

1. Review `functional-codebase/app/main.py` and the reports. Add **actual** human verification notes to each code header, including date, what you checked and the result; do not mark a review complete simply because tests passed.
2. Complete `.ai_logs/conceptual_journal.md` in your own words. The reflection is 14% of the rubric. Address the concrete observations and questions supplied there; distinguish your conclusions from AI-generated analysis.
3. Model confirmation received: the student reports “6.1 Medium” for this session. Exact hidden model SKU and provider hyperparameters remain unexposed; no further setting confirmation is needed.
4. Add the native session export, if available, under `.ai_logs/`, after removing unrelated private content and secrets. A dated manual fallback log is included. Do not share the entire unrelated discussion/browser history as project evidence.
5. Compare the professor's journal template with the provided journal structure if the template has additional required fields.

## Repository and release

All PA1 files remain in place. PA2 is isolated under `PA2/`. The GitHub workflow is `.github/workflows/pa2.yml` and can be run from Actions or on a matching push. Review it before running. Do not move PA1 files merely to rearrange a completed release.

The prior workspace agreement leaves GitHub operations to you. After completing personal review and local checks, from the repository root:

```bash
git status --short
git add PA2 .github/workflows/pa2.yml
git diff --cached --stat
# Use AI/HUMAN/HYBRID prefixes that accurately describe the respective changes.
git commit -m "AI: build and audit PA2 functional baseline"
git push origin main
```

Check the actual branch before using `main`. Run the PA2 workflow and download its evidence. Confirm it succeeded and that reports match the release source. Preserve the validated evidence in `PA2/evidence/` and record the workflow URL in `PA2/evidence/github-run.txt`. Do not invent a GitHub execution URL. Add reviewed documentation changes with accurate authorship tags before the final tag.

Create the PA2 tag/release only after the above is complete. Use **release title `project-assignment-2`** and **tag `assignment-2-v1.0.0`** to match the existing PA1 naming pattern (`project-assignment-1` / `assignment-1-v1.0.0`). The assignment requires a project-assignment-2 release but does not mandate these exact literal strings. The submitted version must contain both assignments. No commit, push, release, or Blackboard submission is claimed to have been performed by this session.

## Blackboard summary draft

> My Assignment 2 release for Domain 1 (Project Artifact & Repository Indexer) is: **[insert actual release URL]**. The PA2 folder contains the fresh functional service and API tests, raw Semgrep and SonarQube results, validated CWE-mapped triage, the security requirements/abuse cases/attack trees/attack surface/DFD/STRIDE analysis, and AI-use logs. The unmitigated baseline is preserved for PA3. **[After review, add a truthful statement about your code review and conceptual journal.]**

The release URL and personal review placeholders must be completed before submission. Confirm the current due date/late-submission policy in Blackboard.
