# Submission Attack Log

Paper: 105 hierarchical_failure_containment

This v5 pass expands the archive into a 28-page hostile-review evidence package. The result is `STRONG_REVISE`, not submit-as-is.

## Attack 1: This could just be option termination.

Response: `option_termination_monitor` is included. V5 reaches hard success `0.83828` while option termination reaches `0.59097`, with lower cascade and higher utility for v5.

## Attack 2: The v4 containment graph may already solve it.

Response: `proposed_hierarchical_failure_containment_graph_v4` is the strongest non-oracle baseline at `0.74167 +/- 0.00595` success. V5 improves success by `0.09661`, containment by `0.07639`, and utility by `0.22800`.

## Attack 3: The method may only halt more often.

Response: V5 false halt is `0.00582`, far below the strongest non-oracle baseline's `0.03029`. The gain is not purchased by excessive halting.

## Attack 4: The method may buy success with damage.

Response: V5 damage is `0.00182`, below `0.00408` for the strongest non-oracle baseline. State and subgoal corruption are also lower.

## Attack 5: A local safety filter may be sufficient.

Response: `local_safety_filter` reaches `0.48915` success with higher cascade, state corruption, damage, false halt, and missed failure. It contains some local anomalies but does not protect hierarchical task state.

## Attack 6: A single component may carry the result.

Response: The best removed-component ablation is `no_false_halt_calibration` at `0.78559` success, below full v5 at `0.84045`. Removing cross-level escalation, local containment, corruption prediction, budget memory, delayed observation, risk calibration, or utility modeling creates distinct failure signatures.

## Attack 7: Fixed-risk deployment may be abstention gaming.

Response: Coverage is reported. At risk budget `0.18`, v5 coverage is `1.00000`, success is `0.83854`, and utility is `0.79059`.

## Attack 8: The result may be a lucky seed.

Response: Pairwise seed comparisons are reported against every baseline. The gate requires v5 to clear non-oracle references on success or utility.

## Attack 9: The evaluation is still not real robotics evidence.

Response: Correct. The terminal decision is `STRONG_REVISE`, not ICLR-ready. The manuscript explicitly requires real robot or independent high-fidelity simulator validation before submission.

## Attack 10: Can this be submitted now?

Response: No. The correct action is strong revise with external robot/high-fidelity experiments, trained policies, external baselines, and rollout evidence.
