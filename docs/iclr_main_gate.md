# ICLR Main Gate

Paper: 105 hierarchical_failure_containment

Previous v3 decision: KILL_ARCHIVE

v4.1 continuation gate verdict: STRONG_REVISE

Evidence digest: 5 tasks x 7 failure regimes x 5 splits x 9 methods x 7 seeds x 84 episodes/group.

Gate outcomes:

- Success gate: pass. Proposed combined-cascade success exceeds the strongest non-oracle baseline by `0.084`.
- Diagnostic gate: pass. Containment rate improves by `0.121` over the strongest non-oracle baseline.
- Safety gate: pass. Damage, state corruption, and false-halt rates are not worse than the strongest non-oracle baseline.
- Pairwise gate: pass. Proposed beats the strongest non-oracle baseline in `7/7` seeds.
- Ablation gate: pass. The full model beats the best removed-component ablation by `0.0321`.
- Stress gate: pass locally. At stress level `0.95`, proposed success is `0.581 +/- 0.008` versus `0.471 +/- 0.010`.

Terminal decision: STRONG_REVISE.

Submission status: not ICLR-main-ready until real robot or independent high-fidelity validation is added.
