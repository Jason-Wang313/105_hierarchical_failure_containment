# Paper 105 Terminal Audit

Date: 2026-06-15 16:41:19 +0100

## Terminal Decision

STRONG_REVISE

## Why Not KILL_ARCHIVE

The regenerated full local benchmark clears the predefined mechanism gates. The proposed method beats the strongest non-oracle baseline on combined-cascade success by `+0.084 +/- 0.009`, wins `7/7` paired seeds, improves containment by `+0.121`, reduces state corruption by `-0.045`, reduces cascade rate by `-0.042`, reduces damage by `-0.022`, and reduces false halts by `-0.012`. Core ablations remain below the full model.

## Why Not ICLR Main Ready

The evidence is still local and synthetic. The repo does not contain real-robot deployment, independent high-fidelity simulator validation, learned policy checkpoints, training curves, external benchmark comparisons, or rollout videos. The correct action is to preserve the paper as a strong-revise candidate, not to represent it as submission-ready.

## Required Next Evidence

- Real robot or independent high-fidelity simulator evaluation.
- Implemented learned baselines for failure-aware hierarchy, recovery, option termination, and uncertainty halting.
- Qualitative rollouts showing when containment prevents high-level task corruption.
- External benchmark split such as LIBERO, RLBench, Meta-World, BridgeData, or a comparable hardware manipulation suite.
- A revised related-work section tied to those external results.
