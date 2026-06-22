# Hostile Reviewer Response

Paper: 105 Hierarchical Failure Containment

## Strongest Technical Threats

- Options and option-termination methods already formalize hierarchical control.
- Option-Critic and HIRO-style methods already learn hierarchical policies.
- Recovery RL and learned recovery chains already handle failures and safe recovery.
- Vision-language-action failure-recovery systems already reason about failures in hierarchical task settings.
- Safety filters, robust fallback controllers, and uncertainty halting already reduce damage through conservative intervention.

## v5 Response

The v5 rebuild narrows the novelty boundary to hierarchical containment: deciding the lowest safe level at which to repair, retry, halt, or escalate before a local failure corrupts subgoal or task state. The frozen benchmark includes strong non-oracle hierarchy, recovery, option-termination, robust MPC, POMDP, causal-event, anomaly, safety-filter, retry, v4 containment, and oracle references.

The local evidence supports the boundary. V5 reaches hard-aggregate success `0.83828 +/- 0.00599` versus `0.74167 +/- 0.00595` for the strongest non-oracle baseline. It improves containment from `0.57604` to `0.65243`, lowers cascade from `0.09149` to `0.04175`, and keeps false halt at `0.00582`.

## Remaining Hostile Review

A hostile reviewer would still be correct to reject a main-track submission today. The evidence is local and synthetic; the baselines are executable diagnostic models rather than external robot systems; and there is no real robot or independently validated high-fidelity simulator evidence.

## Honest Action

The paper is marked `STRONG_REVISE`. Continue only if the next version adds real robot or high-fidelity external validation, implemented learned baselines, and qualitative rollout evidence.
