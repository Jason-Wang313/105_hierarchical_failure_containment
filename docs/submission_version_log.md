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
- Reran `src/run_experiment.py` from source with the full benchmark and logged the run at `logs/105_hierarchical_failure_containment_continuation_rerun_20260615.log`.
- Verified expected CSV coverage and finite numeric outputs.
- Reconfirmed the strongest non-oracle baseline as `failure_aware_hierarchical_controller`.
- Added terminal audit docs and rebuilt the numbered Downloads PDF.
- Terminal decision: STRONG_REVISE; ICLR main ready: no.
