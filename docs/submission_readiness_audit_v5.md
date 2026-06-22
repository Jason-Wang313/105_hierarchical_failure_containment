# Submission Readiness Audit v5

Date: 2026-06-22

Paper: `105_hierarchical_failure_containment`

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Artifact Checks

- Canonical PDF: `C:/Users/wangz/Downloads/105.pdf`
- PDF pages: 28
- PDF SHA256: `182EC42D72A4E8B18EEE96884078C28006BB42CEF4DA2EE1A6C170AB6E6AF061`
- Desktop PDF: absent
- Repo-root numbered PDF: absent
- Bright boxed citation links: present via hyperref border settings
- LaTeX unresolved citations/rerun warnings: absent in final log

## Evidence Checks

- Main rollouts: 345,600
- Ablation rollouts: 115,200
- Stress rollouts: 288,000
- Fixed-risk rollouts: 276,480
- Failure cases: 24
- Row-count validator: passed
- Finite numeric validator: passed
- Nonnegative regret validator: passed

## Gate Checks

All local empirical gates pass:

- success
- containment
- cascade
- state corruption
- subgoal corruption
- damage
- false halt
- missed failure
- calibration
- utility
- pairwise
- ablation
- stress
- fixed risk

Scope gate fails because no real robot, independent high-fidelity simulator, external benchmark, trained checkpoint, calibrated real failure log, or rollout video exists.

## Decision

The artifact is a strong local research package and should continue development. It should not be submitted to ICLR main as-is.
