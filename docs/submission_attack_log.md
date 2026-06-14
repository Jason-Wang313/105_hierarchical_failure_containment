# Submission Attack Log

Paper: 105 hierarchical_failure_containment

This v4 pass rebuilds the archive into a paper-specific local evidence package. The result is `STRONG_REVISE`, not submit-as-is.

## Attack 1: This could just be option termination.

Response: `option_termination_monitor` reaches `0.442 +/- 0.008` combined-cascade success. Proposed reaches `0.576 +/- 0.007` and has better containment and lower cascade rates.

## Attack 2: A failure-aware hierarchical controller may already solve it.

Response: `failure_aware_hierarchical_controller` is the strongest non-oracle baseline at `0.492 +/- 0.006`. Proposed improves success by `0.084 +/- 0.009` and wins `7/7` paired seeds.

## Attack 3: The method may only halt more often.

Response: Proposed false halt is `0.166`, slightly below the strongest baseline at `0.179`. The gain is not purchased by excessive halting.

## Attack 4: The method may buy success with damage.

Response: Proposed damage is `0.029`, below `0.050` for the strongest non-oracle baseline. State corruption also drops from `0.098` to `0.053`.

## Attack 5: A local safety filter may be sufficient.

Response: `local_safety_filter` reaches `0.349 +/- 0.008` success with high false halt and damage. It contains some local failures but does not protect hierarchical task state.

## Attack 6: A single component may carry the result.

Response: The best removed-component ablation is `minus_false_halt_calibration` at `0.551 +/- 0.011`, below the full model at `0.583 +/- 0.008`. Removing cross-level escalation or local containment edges drops success near `0.50`.

## Attack 7: The evaluation is still not real robotics evidence.

Response: Correct. The terminal decision is `STRONG_REVISE`, not ICLR-ready. The manuscript explicitly requires real robot or independent high-fidelity simulator validation before submission.

## Attack 8: Tables and figures could be stale from v3.

Response: The v4 runner deletes obsolete v3 files (`raw_seed_metrics.csv`, `negative_cases.csv`, and `figures/stress_curve_data.csv`) before generating new outputs. Current CSVs passed a finite-value audit.

## Attack 9: The benchmark may be too narrow.

Response: The local benchmark spans 5 tasks, 7 regimes, 5 splits, 9 methods, 7 seeds, and 84 episodes/group. This is adequate for a strong-revise local package but not enough to replace external validation.

## Attack 10: Can this be submitted now?

Response: No. The correct action is strong revise with external robot/high-fidelity experiments and implemented learned baselines.
