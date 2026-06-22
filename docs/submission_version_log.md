# Submission Version Log

## v1 - Generated Draft

- Original continuation-batch generated paper and toy single-seed experiment.

## v2 - Submission Hardening

- Added hostile reviewer attack log and response docs.
- Added seven-seed synthetic metrics, stronger baselines, ablations, stress tests, and negative cases.
- Terminal decision: WORKSHOP_ONLY.

## v3 - ICLR Main Gate Archive

- Applied stricter ICLR-main-conference standard.
- Marked the existing artifact `KILL_ARCHIVE` because the local evidence was template-like and underpowered.

## v4 - Paper-Specific Evidence Rebuild

- Added `docs/paper105_rebuild_plan.md`.
- Replaced the runner with a hierarchical-failure-containment benchmark.
- Generated fresh metrics, per-task/per-regime tables, pairwise tests, ablations, stress sweeps, failure cases, figures, and LaTeX tables.
- Removed obsolete v3 outputs from the runner.
- Rewrote the paper as a strong-revise evidence report with honest limitations.
- Terminal decision: STRONG_REVISE.

## v4.1 - Continuation Submission Audit

- Added `docs/paper105_iclr_submission_execution_plan_20260615.md`.
- Reran `src/run_experiment.py` from source with the full benchmark.
- Verified expected CSV coverage and finite numeric outputs.
- Reconfirmed the strongest non-oracle baseline as `failure_aware_hierarchical_controller`.
- Added terminal audit docs and rebuilt the numbered Downloads PDF.
- Terminal decision: STRONG_REVISE; ICLR main ready: no.

## v5-expanded - Hostile-Review Rebuild

- Added `docs/paper105_expanded_submission_plan_20260622.md`.
- Replaced the runner with a RAM-light streaming v5 benchmark.
- Expanded evidence to 6 tasks, 8 regimes, 8 splits, 15 methods, 10 seeds, and raw rollout persistence.
- Added v5 ablations, stress sweep, fixed-risk budgets, negative cases, row-count validation, nonnegative regret audit, and figures.
- Added `scripts/generate_manuscript.py` and `scripts/validate_submission_artifacts.py`.
- Generated a 28-page manuscript with bright boxed clickable citations.
- Validated canonical PDF at `C:/Users/wangz/Downloads/105.pdf`.
- Terminal decision: STRONG_REVISE; ICLR main ready: no.
