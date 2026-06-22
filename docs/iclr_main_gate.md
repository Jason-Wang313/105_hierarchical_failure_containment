# ICLR Main Gate

Paper: 105 hierarchical_failure_containment

Previous v4.1 continuation gate verdict: STRONG_REVISE

v5-expanded gate verdict: STRONG_REVISE

Evidence digest: 6 tasks x 8 failure regimes x 8 splits x 15 methods x 10 seeds x 6 episodes/cell, with ablation, stress, fixed-risk, and negative-case audits.

Gate outcomes:

- Success gate: pass. V5 hard success exceeds the strongest non-oracle baseline by `0.09661`.
- Containment gate: pass. V5 containment improves over the best non-oracle containment reference by `0.07639`.
- Cascade gate: pass. V5 cascade is `0.04175` versus `0.09149` for the strongest non-oracle success reference.
- Corruption gates: pass. V5 state corruption `0.00217` and subgoal corruption `0.00182` are below the strongest non-oracle reference.
- Safety gates: pass. V5 damage `0.00182`, false halt `0.00582`, and missed failure `0.14332` are below the strongest non-oracle reference.
- Calibration gate: pass. V5 ECE is `0.00328`.
- Utility gate: pass. V5 utility is `0.79005` versus `0.56205` for the strongest non-oracle reference.
- Pairwise gate: pass. V5 clears all non-oracle seed-paired comparisons on success or utility.
- Ablation gate: pass. Full v5 beats every removed-component ablation on success and utility.
- Stress gate: pass locally. V5 remains above the strongest non-oracle reference at maximum stress.
- Fixed-risk gate: pass locally. At risk budget `0.18`, v5 keeps coverage `1.00000` and utility `0.79059`.
- Scope gate: fail. No real robot, independent high-fidelity simulator, external benchmark, trained checkpoint, calibrated real failure log, or rollout video exists.

Terminal decision: STRONG_REVISE.

Submission status: not ICLR-main-ready until external robot or high-fidelity validation is added.
