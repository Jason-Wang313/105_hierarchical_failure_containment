# Reproducibility Checklist

## Reproduces Locally

- [x] `python -m py_compile src/run_experiment.py`
- [x] `python src/run_experiment.py`
- [x] `results/dataset_summary.csv`
- [x] `results/rollouts.csv`
- [x] `results/main_group_metrics.csv`
- [x] `results/main_seed_metrics.csv`
- [x] `results/metrics.csv`
- [x] `results/hard_aggregate_seed_metrics.csv`
- [x] `results/hard_aggregate_metrics.csv`
- [x] `results/pairwise_stats.csv`
- [x] `results/ablation_rollouts.csv`
- [x] `results/ablation_seed_metrics.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/stress_sweep_raw.csv`
- [x] `results/stress_sweep_seed_metrics.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/fixed_risk_raw.csv`
- [x] `results/fixed_risk_seed_metrics.csv`
- [x] `results/fixed_risk_metrics.csv`
- [x] `results/fixed_risk_pairwise_stats.csv`
- [x] `results/failure_cases.csv`
- [x] `results/row_counts.csv`
- [x] `figures/hierarchical_v5_hard_success.png`
- [x] `figures/hierarchical_v5_diagnostics.png`
- [x] `figures/hierarchical_v5_safety_regret.png`
- [x] `figures/hierarchical_v5_stress_sweep.png`
- [x] `figures/hierarchical_v5_ablation.png`
- [x] `figures/hierarchical_v5_fixed_risk.png`
- [x] `scripts/generate_manuscript.py`
- [x] `scripts/validate_submission_artifacts.py`
- [x] `paper/main.tex`
- [x] Canonical PDF: `C:/Users/wangz/Downloads/105.pdf`
- [x] Validator output: `validated Paper 105 artifacts: pages=28, sha256=182EC42D72A4E8B18EEE96884078C28006BB42CEF4DA2EE1A6C170AB6E6AF061`

## Does Not Yet Reproduce

- [ ] Real robot results.
- [ ] Independent high-fidelity simulator runs.
- [ ] Trained policy checkpoints.
- [ ] External baseline implementations.
- [ ] Real deployment videos.

This repository reproduces a v5 strong-revise evidence package, not a finished ICLR-main submission.
