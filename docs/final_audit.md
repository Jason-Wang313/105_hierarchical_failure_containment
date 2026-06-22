# Final Audit

1. Chosen thesis: hierarchical robot policies need explicit containment boundaries that prevent low-level failures from corrupting subgoals or task state.
2. ICLR-main decision: STRONG_REVISE.
3. Submission-hardening version: v5-expanded.
4. Evidence: 6 tasks x 8 failure regimes x 8 splits x 15 methods, 10 seeds, 6 episodes/cell.
5. Raw rows: 345,600 main; 115,200 ablation; 288,000 stress; 276,480 fixed-risk.
6. Strongest non-oracle baseline: `proposed_hierarchical_failure_containment_graph_v4`.
7. Main result: v5 hard success `0.83828 +/- 0.00599` vs strongest non-oracle `0.74167 +/- 0.00595`.
8. Diagnostic result: containment `0.65243` vs `0.57604`; cascade `0.04175` vs `0.09149`.
9. Safety result: state corruption `0.00217`, subgoal corruption `0.00182`, damage `0.00182`, false halt `0.00582`, missed failure `0.14332`.
10. Utility/regret result: utility `0.79005`; regret to oracle `0.11311`; oracle success `0.91510`.
11. Ablation result: full v5 success `0.84045`; best removed-component success `0.78559` for `no_false_halt_calibration`.
12. Fixed-risk result: budget `0.18`, coverage `1.00000`, success `0.83854`, utility `0.79059`.
13. Claim-validity status: mechanism supported locally; not submission-ready without external robot/high-fidelity validation.
14. Exact Downloads PDF path: `C:/Users/wangz/Downloads/105.pdf`.
15. PDF pages and SHA256: 28 pages, `182EC42D72A4E8B18EEE96884078C28006BB42CEF4DA2EE1A6C170AB6E6AF061`.
16. GitHub URL: https://github.com/Jason-Wang313/105_hierarchical_failure_containment
17. Confirmation: no visible Desktop copy was requested or made.
