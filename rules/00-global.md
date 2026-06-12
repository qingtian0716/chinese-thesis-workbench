# Global Rules

**Trigger:** Every thesis workflow task.
**Required inputs:** User request and current workspace state.
**Outputs:** Safe execution boundaries and state-update obligations.

## Hard Rules

- School and advisor requirements override default rules.
- Do not write formal thesis body before materials are collected or the user explicitly confirms there are no more materials.
- During intake, classify materials as `required`, `strongly_recommended`, or `optional`, and explain the effect of each missing required or strongly recommended material.
- Use `content-decisions.md` when the user provides feature/module/experiment/appendix candidates, but do not block the main workflow only because no candidate content has been provided yet.
- Record user-approved scope, material-unavailable, limited-continuation, standard-conflict, content-exclusion, outline, word-count, DOCX, appendix, and filename decisions in `user-decisions.md`.
- User-facing workflow files are decision aids only. They must not weaken school/advisor requirements, evidence requirements, citation verification, figure provenance, or DOCX delivery checks.
- Do not write formal thesis body before standards, sample/template analysis, and evidence building are complete.
- When evidence is insufficient, trigger `stop_and_report`; do not guess missing facts.
- When blocked, classify the issue as `hard_blocker`, `limited_continue`, or `user_choice_needed`, then provide user options and a recommended path.
- `thesis-ai-spec.yaml` is the single entry point for thesis facts.
- `figure-registry.yaml` is the single entry point for figures, tables, screenshots, and diagram sources.
- Thesis prose may consume structured facts and evidence only; do not expand directly from README files or old notes.
- Do not write content that `content-decisions.md` marks as rejected, excluded, or waiting for evidence.
- Do not invent features, fields, APIs, test results, experiment data, or references.
- AIGC style governance runs after the evidence chain is complete and may only improve academic expression, evidence density, and vague wording.
- Thesis body must not expose AI workflow language.
- Chapter 4 implementation must bind to real modules, screenshots, core code, SQL, or equivalent evidence.
- System-design theses without an E-R diagram or equivalent data-design evidence cannot be marked complete.
- Generate both the main thesis DOCX and appendix DOCX. For strict school formatting, prefer template-copy filling via `scripts/docx/apply_textual_edits.py --from-template`; otherwise use default or sample-style generation. Do not promise full template reproduction. Preserve diagram source, E-R source, flowchart source, and related assets in the appendix.
- Formula delivery must be explicit: `latex_text` preserves source formula text, while `formula_image` requires matching image assets.
- Output filenames must use the thesis title, not generic names such as `final`, `draft`, `paper-final`, or `doc1`.
- Literature workflow must be: build pool -> verify -> filter -> format -> generate verification checklist.
- **Literature verification gate**: Chapter 1 (research status) and Chapter 2 (related work) sections must not enter formal writing until the literature pool has completed verification (`verify_literature` step). All references cited in these chapters must have `status: verified` in `citation-crossref-register.yaml`.
- **Language style enforcement**: After completing each chapter draft, apply the banned phrase list and sentence patterns from `knowledge/prose-style-guide.md`. Non-compliant paragraphs must be revised before submission to the user. Use `scripts/review/check_prose_quality.py` to verify compliance.
- **Prose quality gates**: Run lightweight prose checks (banned phrases, AI sentence patterns) after each section during `draft_chapters`. Run full prose quality report at `quality_gates` stage.

## Workspace Reuse And Reset Rules

- If `paper-context/workflow/workflow-status.md` exists and `phase` is not `intake_only`, read workflow state before starting new thesis work.
- When the user asks to restart, rewrite, regenerate, or use a new angle, present reset choices before clearing data: `--reset-output`, `--reset-evidence`, or `--full-reset`.
- Never delete `papers/` or `assets/`; these are original user materials.
- Use `scripts/workspace/reset_workspace.py` for generated workspace resets. It archives generated files under `paper-context/archive/<timestamp>/` before clearing them.
- Before ending a workflow phase, update `workflow-status.md` and `user-dashboard.md`; do not claim progress only in chat.
- If `paper-context/evidence/` or `paper-context/literature/` is non-empty before a new writing task, ask whether to reuse it and record the decision.

## Reference Knowledge

- Workflow state: `references/workflow/workflow-state-management.md`
- Reset command: `scripts/workspace/reset_workspace.py`
