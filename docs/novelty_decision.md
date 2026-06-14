# Novelty Decision

Chosen thesis: hierarchical robot policies need explicit containment models that decide whether a failure should be repaired locally or escalated before it corrupts task state.

New central mechanism: a hierarchical failure containment graph over local containment edges, cross-level escalation, recovery budget, task-state corruption prediction, and false-halt calibration.

Decision: STRONG_REVISE.

Reason: the v4 local evidence passes success, diagnostic, safety, pairwise, and ablation gates, but real robot or independent high-fidelity validation is still missing.
