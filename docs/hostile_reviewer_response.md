# Hostile Reviewer Response

Paper: 105 Hierarchical Failure Containment

## Strongest Technical Threats

- Options and option-termination methods already formalize hierarchical control.
- Option-Critic and HIRO-style methods already learn hierarchical policies.
- Recovery RL and learned recovery chains already handle failures and safe recovery.
- Vision-language-action failure-recovery systems already reason about failures in hierarchical task settings.
- Safety filters and uncertainty halting already reduce damage through conservative intervention.

## ICLR Main Response

The v4 rebuild narrows the novelty boundary to hierarchical containment: stopping or repairing low-level failures before they corrupt higher-level task state. The local benchmark supports that boundary: proposed combined-cascade success is `0.576 +/- 0.007` versus `0.492 +/- 0.006` for the strongest non-oracle baseline, with lower state corruption, cascade, and damage rates.

## Remaining Hostile Review

A hostile reviewer would still be correct to reject a main-track submission today. The evidence is local and synthetic; the baselines are executable diagnostic models rather than external robot systems; and there is no real robot or independently validated high-fidelity simulator evidence.

## Honest Action

The paper is marked `STRONG_REVISE`. Continue only if the next version adds real robot or high-fidelity external validation and implemented learned baselines.
