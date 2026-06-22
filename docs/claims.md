# Claims

- Mechanism claim: hierarchical robot policies need explicit containment boundaries between low-level skill anomalies, mid-level subgoal corruption, and high-level task-state corruption.
- Method claim: `risk_calibrated_hierarchical_containment_v5` combines a local containment graph, cross-level escalation model, recovery-budget memory, delayed-observation buffer, corruption predictor, false-halt calibration, and escalation utility model.
- Evidence claim: on hard aggregate splits, v5 reaches `0.83828 +/- 0.00599` success versus `0.74167 +/- 0.00595` for the strongest non-oracle baseline, `proposed_hierarchical_failure_containment_graph_v4`.
- Diagnostic claim: v5 improves containment from `0.57604` to `0.65243` while lowering cascade from `0.09149` to `0.04175`.
- Safety claim: v5 reports state corruption `0.00217`, subgoal corruption `0.00182`, damage `0.00182`, false halt `0.00582`, and missed failure `0.14332`.
- Fixed-risk claim: at strict budget `0.18`, v5 keeps coverage `1.00000`, success `0.83854`, and utility `0.79059`.
- Scope claim: the evidence supports `STRONG_REVISE` only; it does not establish real-robot deployment performance.
- Unsupported claim explicitly avoided: no claim of ICLR-main readiness, hardware robustness, or state-of-the-art robot performance.
