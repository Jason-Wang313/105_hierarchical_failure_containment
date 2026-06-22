# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v5 rebuild expands the local evidence to 6 tasks, 8 failure regimes, 8 splits, 15 methods, 10 seeds, 345,600 main rollouts, ablations, stress sweeps, fixed-risk containment, negative cases, nonnegative regret, and a 28-page manuscript with boxed clickable citations.

The evidence supports the local mechanism: on hard aggregate splits, v5 reaches `0.83828 +/- 0.00599` success versus `0.74167 +/- 0.00595` for the strongest non-oracle baseline, with containment `0.65243`, cascade `0.04175`, damage `0.00182`, false halt `0.00582`, and utility `0.79005`. The oracle remains higher at `0.91510` success.

The honest terminal action is strong-revise, not submit. A submission-quality revival still requires real robot or independent high-fidelity simulator validation, implemented learned baselines, external benchmark evidence, trained checkpoints, and qualitative rollout evidence.
