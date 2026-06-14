# Experiment Rigor Checklist

## v4 Local Evidence

- [x] Paper-specific hierarchical-failure-containment benchmark.
- [x] 5 robot task families.
- [x] 7 failure regimes.
- [x] 5 distribution/stress splits.
- [x] 9 methods including oracle and strong non-oracle baselines.
- [x] 7 random seeds.
- [x] 84 episodes per group.
- [x] Confidence intervals.
- [x] Pairwise seed comparisons.
- [x] Success, containment, state corruption, cascade, damage, false halt, recovery, escalation precision, latency, cost, and regret metrics.
- [x] Ablations for local containment edges, cross-level escalation, recovery-budget memory, corruption prediction, and false-halt calibration.
- [x] Stress sweep over cascade intensity.
- [x] Failure-case table.
- [x] Generated figures and LaTeX tables.

## Remaining ICLR-Main Gaps

- [ ] Real-robot validation.
- [ ] Independent high-fidelity simulator benchmark.
- [ ] Implemented learned model checkpoints.
- [ ] Implemented real competing baselines.
- [ ] External benchmark comparison.
- [ ] Deployment videos or qualitative rollouts.

Decision: strong-revise. The local evidence is serious enough to continue, but not enough to submit.
