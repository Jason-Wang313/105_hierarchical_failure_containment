# Final Audit

1. Chosen thesis: hierarchical robot policies can contain low-level failures before they corrupt subgoals or task state.
2. ICLR-main decision: STRONG_REVISE.
3. Submission-hardening version: v4.1.
4. Evidence: 5 tasks x 7 failure regimes x 5 splits x 9 methods, 7 seeds, 84 episodes/group.
5. Strongest non-oracle baseline: `failure_aware_hierarchical_controller`.
6. Main result: proposed combined-cascade success `0.576 +/- 0.007` vs strongest non-oracle `0.492 +/- 0.006`.
7. Diagnostic result: proposed containment rate `0.515` vs `0.394`; cascade rate `0.116` vs `0.158`.
8. Safety result: proposed state corruption `0.053` and damage `0.029` vs baseline `0.098` and `0.050`.
9. Ablation result: full model `0.583 +/- 0.008`; best removed component `minus_false_halt_calibration` at `0.551 +/- 0.011`.
10. Stress result: at maximum stress level `0.95`, proposed success `0.581 +/- 0.008` vs strongest non-oracle `0.471 +/- 0.010`.
11. Claim-validity status: mechanism supported locally; not submission-ready without external robot/high-fidelity validation.
12. Exact Downloads PDF path: `C:/Users/wangz/Downloads/105.pdf`.
13. GitHub URL: https://github.com/Jason-Wang313/105_hierarchical_failure_containment
14. Confirmation: no visible Desktop copy was requested or made.
