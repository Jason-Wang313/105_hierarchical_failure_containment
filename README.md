# 105 Hierarchical Failure Containment

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE for ICLR main conference.

The rebuilt evidence package tests whether hierarchical robot policies can contain low-level failures before they corrupt mid-level subgoals or high-level task state. The 2026-06-15 continuation audit reran the full benchmark from source and preserved the terminal decision: the local benchmark supports the mechanism, but the paper is not yet ICLR-main-ready because it still lacks real-robot or independent high-fidelity simulator validation.

## Evidence Snapshot

- Benchmark: 5 tasks x 7 failure regimes x 5 splits x 9 methods.
- Repeats: 7 seeds, 84 episodes per task/regime/split/method group.
- Strongest non-oracle baseline: `failure_aware_hierarchical_controller`.
- Combined-cascade success: proposed `0.576 +/- 0.007`, strongest non-oracle `0.492 +/- 0.006`.
- Containment: proposed `0.515` vs `0.394`.
- Safety: proposed state corruption `0.053`, cascade `0.116`, damage `0.029`.
- Pairwise seeds: proposed beats strongest non-oracle baseline in `7/7` seeds.
- Maximum stress level `0.95`: proposed `0.581 +/- 0.008` success vs strongest non-oracle `0.471 +/- 0.010`.
- Terminal gate: `STRONG_REVISE`, not submit-as-is.

## Reproduce

```powershell
python src\run_experiment.py
```

Key outputs are in `results/` and `figures/`.

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/105.pdf`
