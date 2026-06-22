# Novelty Decision

Chosen thesis: hierarchical robot policies need explicit containment models that decide whether a failure should be repaired locally, retried, halted, or escalated before it corrupts subgoal or task state.

New central mechanism: a risk-calibrated hierarchical containment state over local containment edges, cross-level escalation, recovery budget, delayed observations, task-state and subgoal corruption prediction, false-halt calibration, and escalation utility.

Decision: STRONG_REVISE.

Reason: the v5 local evidence passes success, containment, cascade, corruption, safety, pairwise, ablation, stress, fixed-risk, and utility gates, but real robot or independent high-fidelity validation is still missing.
