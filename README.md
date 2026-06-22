# 105 Hierarchical Failure Containment

Submission-hardening version: v5-expanded

Terminal decision: STRONG_REVISE for ICLR main conference.

The 2026-06-22 rebuild expands Paper 105 into a 28-page hostile-review evidence package for risk-calibrated hierarchical failure containment. The local benchmark tests whether a controller can contain low-level skill anomalies before they corrupt mid-level subgoals or high-level task state under cascade, delay, recovery-budget, and false-halt stress.

## Evidence Snapshot

- Benchmark: 6 tasks x 8 failure regimes x 8 splits x 15 methods.
- Repeats: 10 seeds, 6 episodes per factorial cell.
- Raw evidence: 345,600 main rollouts, 115,200 ablation rollouts, 288,000 stress rollouts, 276,480 fixed-risk rollouts.
- Strongest non-oracle baseline: `proposed_hierarchical_failure_containment_graph_v4`.
- Hard-aggregate success: v5 `0.83828 +/- 0.00599`, strongest non-oracle `0.74167 +/- 0.00595`.
- Hard-aggregate containment: v5 `0.65243`, strongest non-oracle `0.57604`.
- Safety/cascade: v5 cascade `0.04175`, state corruption `0.00217`, subgoal corruption `0.00182`, damage `0.00182`, false halt `0.00582`, missed failure `0.14332`.
- Utility/regret: v5 utility `0.79005`, regret to oracle `0.11311`; oracle success `0.91510`.
- Strict fixed-risk budget `0.18`: coverage `1.00000`, success `0.83854`, utility `0.79059`.
- Terminal gate: all frozen local gates pass; scope gate fails because external robot/high-fidelity validation is missing.

## Reproduce

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/105.pdf`

Validation:

```powershell
python scripts\validate_submission_artifacts.py
```

The canonical validated PDF has 28 pages and SHA256 `182EC42D72A4E8B18EEE96884078C28006BB42CEF4DA2EE1A6C170AB6E6AF061`.
