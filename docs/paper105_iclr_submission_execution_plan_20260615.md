# Paper 105 ICLR Submission-Readiness Execution Plan

Started: 2026-06-15 16:41:19 +0100

## Objective

Re-audit Paper 105, `hierarchical_failure_containment`, under the stricter continuation-pass standard. The goal is not to relabel the work optimistically; it is to determine whether the regenerated evidence supports a real ICLR-main submission claim, and to leave a clean, reproducible repository either way.

## Evidence To Regenerate

- Compile-check `src/run_experiment.py`.
- Run the full benchmark with all tasks, regimes, splits, baselines, seeds, ablations, stress sweeps, and failure cases intact.
- Preserve a root-level rerun log at `logs/105_hierarchical_failure_containment_continuation_rerun_20260615.log`.
- Verify that all result CSVs are finite and have the expected coverage.
- Identify the strongest non-oracle baseline from regenerated combined-cascade results.
- Recompute paired seed comparisons, safety diagnostics, ablation margins, and stress-sweep behavior from CSVs.

## Submission Gates

The paper can remain `STRONG_REVISE` only if the proposed method:

- beats the strongest non-oracle baseline on combined-cascade success by at least `0.030`;
- wins at least `5/7` paired seed comparisons;
- improves containment or cascade diagnostics by at least `0.050`;
- does not buy success by increasing state corruption, cascade rate, damage, or false halts;
- survives all named core ablations;
- states plainly that local synthetic evidence is not ICLR-main-ready without real-robot or independent high-fidelity validation.

If those gates fail, the terminal decision must become `KILL_ARCHIVE`.

## Artifacts To Update

- `README.md`
- `child_status.md`
- `plan.md`
- `docs/submission_readiness_audit_v4_1.md`
- `docs/paper105_terminal_audit_20260615.md`
- `paper/main.tex`
- `C:/Users/wangz/Downloads/105.pdf`

## Externalization And Reporting

- Build the PDF with a clean LaTeX/BibTeX log and copy only the numbered PDF to Downloads.
- Do not copy the PDF to Desktop.
- Commit and push the child repository to its public GitHub repo.
- Update root ledgers: `GLOBAL_POOL_STATUS.md`, `BATCH_STATUS.md`, `SUBMISSION_STATUS.md`, `MASTER_REPORT.md`, and `MASTER_SUBMISSION_REPORT.md`.
