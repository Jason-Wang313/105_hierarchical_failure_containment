# Experiment Rigor Checklist

## v5 Local Evidence

- [x] Paper-specific hierarchical-failure-containment benchmark.
- [x] 6 robot task families.
- [x] 8 failure regimes.
- [x] 8 distribution/stress splits.
- [x] 15 methods including oracle, v4 graph, recovery, option-termination, robust MPC, POMDP, causal-event, anomaly, safety-filter, retry, and hierarchy-only baselines.
- [x] 10 random seeds.
- [x] 345,600 raw main rollouts.
- [x] Confidence intervals.
- [x] Pairwise seed comparisons against every baseline.
- [x] Success, containment, cascade, state corruption, subgoal corruption, damage, false halt, missed failure, recovery, escalation precision, latency, ECE, regret, and utility metrics.
- [x] Ablations for local containment graph, cross-level escalation, corruption prediction, recovery-budget memory, false-halt calibration, delayed-observation buffer, risk calibration, and escalation utility.
- [x] Stress sweep over cascade, observation delay, budget pressure, and false-halt pressure.
- [x] Fixed-risk containment budgets with coverage reported.
- [x] Negative-case table.
- [x] Generated figures, LaTeX manuscript, and boxed clickable citations.
- [x] Validation script checks row counts, finite values, nonnegative regret, page count, PDF placement, LaTeX link settings, and scope gate.

## Remaining ICLR-Main Gaps

- [ ] Real-robot validation.
- [ ] Independent high-fidelity simulator benchmark.
- [ ] Implemented learned model checkpoints.
- [ ] Implemented external competing baselines.
- [ ] External benchmark comparison.
- [ ] Deployment videos or qualitative real/high-fidelity rollouts.

Decision: `STRONG_REVISE`. The local evidence is serious, but not enough to submit.
