---
name: chinese-thesis-workbench
description: Standardize, draft, revise, check, and package Chinese undergraduate thesis or graduation-design papers from school templates, task books, proposals, sample papers, source code, screenshots, databases, APIs, tests, literature PDFs, Word comments, and existing drafts. Use when the user asks to write, generate, refactor, polish, reduce AIGC style, verify, format, or deliver a Chinese thesis with evidence traceability, figure registries, workflow logs, chapter word control, screenshots, references, DOCX output, and appendix DOCX.
---

# Chinese Thesis Workbench

## Operating Model

Use standards and evidence as the control layer, then use the Chinese thesis drafting pipeline as the output layer. Treat school templates, advisor requirements, task books, sample papers, source code, databases, APIs, tests, literature PDFs, screenshots, Word comments, and existing drafts as materials that must be resolved into structured state before formal prose is written.

The workbench has three sides:

- Governance side: `paper-context/` stores workflow state, standards, evidence, literature, AIGC reports, and Word comment revisions.
- Delivery side: `paper-output/` stores thesis Markdown, DOCX, appendix DOCX, figures, screenshots, image maps, and reference verification artifacts.
- User-facing decision side: `paper-context/workflow/user-dashboard.md`, `content-decisions.md`, `blocker-report.md`, and `user-decisions.md` summarize progress, decisions, blockers, and approved scope.

Before executing any workflow phase, read `rules/00-global.md` and the phase-specific rule file from the Resource Map.

## Required Workflow

Run the workflow in this order unless the user is only asking for a narrow inspection or revision:

1. `intake_materials`: collect materials and record priority, gaps, missing impact, continuation limits, and user next steps.
2. `init_workspace`: initialize `thesis-ai-standard/`, `paper-context/`, and workflow logs.
3. `resolve_standards`: fill `thesis-ai-standard/templates/standard-profile.yaml`.
4. `analyze_sample_and_template`: normalize school template and sample-paper observations before drafting.
5. `build_evidence`: extract project facts into `paper-context/evidence/`.
6. `verify_literature`: verify references and update citation cross-reference state before writing literature-heavy chapters.
7. `stop_and_report`: stop or limit affected scope whenever evidence, standards, figures, citations, or DOCX delivery cannot be verified.
8. `build_thesis_spec`: fill `thesis-ai-standard/templates/thesis-ai-spec.yaml`.
9. `build_figure_registry`: fill `thesis-ai-standard/templates/figure-registry.yaml`.
10. `confirm_outline`: confirm chapter structure, word counts, observations, and content decisions.
11. `assign_section_budgets`: write per-section word budgets to `paper-context/workflow/section-word-budget.md`.
12. `draft_chapters`: draft from confirmed evidence and budgets, checking prose quality after sections.
13. `produce_assets`: generate or collect figures, diagrams, screenshots, tables, and appendix sources.
14. `produce_docx`: generate or edit main DOCX and appendix DOCX into `paper-output/`.
15. `quality_gates`: run standards, evidence, reference, figure, DOCX, prose, and AIGC checks.
16. `delivery_report`: report outputs, limitations, remaining human decisions, and verification evidence.

`stop_and_report` is a global blocking mechanism, not just one step. Read `rules/08-blockers.md` whenever continuing may require guessing.

## Phase + Status State Model

Use this two-layer state model in `paper-context/workflow/workflow-status.md`, and mirror the user-facing summary in `paper-context/workflow/user-dashboard.md`:

| Field | Allowed values |
| --- | --- |
| `phase` | `intake_only`, `workspace_ready`, `standards_resolved`, `sample_analysis_done`, `evidence_built`, `spec_confirmed`, `outline_confirmed`, `writing_allowed`, `delivery_done` |
| `status` | `pending`, `in_progress`, `blocked`, `needs_review`, `done`, `deprecated` |

When status becomes `blocked`, write `blocked_reason`, `missing_materials`, `next_action`, and `can_continue_with_limitations` in the status file. Do not hide blockers in chat only.

After any meaningful phase, blocker, material, outline, or delivery-scope change, update `user-dashboard.md`.

## Decision Tree

1. If there is no workspace, run `scripts/workspace/init_thesis_workspace.py`.
2. If an existing workspace has evidence or literature, ask whether to reuse it before resetting or rebuilding.
3. If school/advisor/template rules are missing or conflicting, resolve standards first.
4. If sample/template analysis is missing, analyze it before `thesis-ai-spec.yaml`.
5. If source evidence or literature is missing, build evidence and reference pools before writing.
6. If `thesis-ai-spec.yaml` is not confirmed, do not write formal thesis body.
7. If `figure-registry.yaml` is not ready, do not claim figures/tables/screenshots are complete.
8. If asked to revise Word comments, extract comments and route back to `writing_allowed`.
9. If asked for final delivery, run quality gates and produce both main and appendix DOCX.

## Resource Map

| Need | Resource |
| --- | --- |
| Global hard rules and reset behavior | `rules/00-global.md` |
| Intake and material collection | `rules/01-intake.md` |
| Standards and template resolution | `rules/02-standards.md` |
| Evidence extraction | `rules/03-evidence.md` |
| Literature workflow | `rules/04-literature.md` |
| Writing pipeline and chapter control | `rules/05-writing.md` |
| Quality gates and review | `rules/06-review.md` |
| DOCX delivery | `rules/07-delivery.md` |
| Blockers and sparse material | `rules/08-blockers.md` |
| Chapter patterns and prose knowledge | `knowledge/chapter-patterns.md`, `knowledge/prose-style-guide.md` |
| Academic phrases and vocabulary | `knowledge/chinese-academic-phrases.md`, `knowledge/domain-vocab.yaml` |
| AIGC governance | `knowledge/aigc-governance.md`, `scripts/review/analyze_aigc_style.py` |
| Literature search module | `modules/literature-search/module.md`, `modules/literature-search/keyword-strategy.md`, `modules/literature-search/database-guide.md` |
| Word comment revision module | `modules/word-comments/module.md`, `scripts/docx/` |
| Figures and screenshots | `scripts/figures/`, `scripts/screenshots/`, `thesis-ai-standard/templates/figure-registry.yaml` |
| Workflow state and rapid workflow | `references/workflow/workflow-state-management.md`, `references/workflow/rapid-thesis-workflow.md` |
| Merge provenance | `references/merge-map.md` |

## Delivery Contract

Deliver thesis artifacts under `paper-output/`:

- `<论文标题>.md`
- `<论文标题>.docx`
- `<论文标题>-附件.docx`
- `<论文标题>-image-map.json`
- `<论文标题>-文献核验清单.json`
- `<论文标题>-prose-report.md`
- `figures/`
- `screenshots/`

Report what was verified, what could not be verified, and what still needs human confirmation. If verification cannot run, state the command and the reason.
