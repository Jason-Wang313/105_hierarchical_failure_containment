# Submission Readiness Audit v4.1

Paper: 105 `hierarchical_failure_containment`

Audit date: 2026-06-15 16:41:19 +0100

Decision: STRONG_REVISE

ICLR main ready: no

## Regenerated Evidence

- Runner: `src/run_experiment.py`
- Rerun log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/105_hierarchical_failure_containment_continuation_rerun_20260615.log`
- Benchmark coverage: 5 tasks x 7 failure regimes x 5 splits x 9 methods.
- Repeats: 7 seeds, 84 episodes per task/regime/split/method group.
- Strongest non-oracle baseline: `failure_aware_hierarchical_controller`.
- Terminal decision emitted by runner: `STRONG_REVISE`.

## CSV Integrity

- `metrics.csv`: 45 rows, finite numeric fields.
- `per_task_regime_metrics.csv`: 1575 rows, finite numeric fields.
- `seed_task_regime_metrics.csv`: 11025 rows, finite numeric fields.
- `seed_split_metrics.csv`: 315 rows, finite numeric fields.
- `pairwise_stats.csv`: 8 rows, finite numeric fields.
- `ablation_metrics.csv`: 7 rows, finite numeric fields.
- `ablation_seed_metrics.csv`: 49 rows, finite numeric fields.
- `ablation_task_regime_seed_metrics.csv`: 1715 rows, finite numeric fields.
- `stress_sweep.csv`: 30 rows, finite numeric fields.
- `stress_sweep_seed_metrics.csv`: 7350 rows, finite numeric fields.
- `failure_cases.csv`: 8 rows, finite numeric fields.

## Main Result

On combined-cascade stress, proposed hierarchical failure containment reaches `0.576 +/- 0.007` success versus `0.492 +/- 0.006` for `failure_aware_hierarchical_controller`, a margin of `+0.084 +/- 0.009`. Proposed also improves containment from `0.394` to `0.515`, reduces state corruption from `0.098` to `0.053`, reduces cascade rate from `0.158` to `0.116`, reduces damage from `0.050` to `0.029`, and reduces false halt rate from `0.179` to `0.166`.

## Pairwise And Ablations

- Pairwise seed test against the strongest non-oracle baseline: `7/7` wins.
- Full ablation success: `0.583 +/- 0.008`.
- Best removed component: `minus_false_halt_calibration` at `0.551 +/- 0.011`.
- Ablation margin over best removed component: `+0.032`.

## Stress Sweep

Stress levels: `0.10`, `0.27`, `0.44`, `0.61`, `0.78`, `0.95`.

At maximum stress level `0.95`, proposed success is `0.581 +/- 0.008` versus `0.471 +/- 0.010` for the strongest non-oracle baseline and `0.725 +/- 0.007` for the oracle. Proposed also keeps lower state corruption (`0.055` vs `0.098`), cascade rate (`0.120` vs `0.169`), damage (`0.031` vs `0.054`), and containment latency (`0.808` vs `0.898`) than the strongest non-oracle baseline.

## Honest Submission Decision

The local evidence supports the mechanism and justifies continuing the project, but it does not make the paper ICLR-main-ready. A real submission needs real robot or independent high-fidelity simulator validation, external learned baselines, qualitative rollouts, and a stronger prior-work positioning section grounded in those external results.
