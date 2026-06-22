# Literature Map

Paper: 105 hierarchical_failure_containment

Field box: hierarchical robot policies, failure recovery, safe long-horizon control.

Thesis: low-level execution failures should be contained before they corrupt mid-level subgoals or high-level task state.

## Crowded Clusters

- Options and hierarchical reinforcement learning.
- Option termination and subpolicy switching.
- Safety filters and uncertainty-based halting.
- Recovery RL and learned recovery chains.
- Vision-language-action failure reasoning and recovery.
- Task-and-motion planning with monitoring.
- World models, POMDP monitors, robust fallback control, and causal event graphs.

## Boundary

The paper's boundary is hierarchical containment. A hierarchy can switch skills; a safety filter can halt; a recovery policy can retry; a robust planner can replan. The proposed mechanism asks whether a controller can identify the level at which a failure should be contained, repair locally when safe, and escalate before task-state corruption when local repair is unsafe.

## Local Evidence

The v5 benchmark supports the boundary under hard splits: v5 success is `0.83828 +/- 0.00599` versus `0.74167 +/- 0.00595` for the strongest non-oracle baseline, containment improves from `0.57604` to `0.65243`, cascade drops from `0.09149` to `0.04175`, and utility improves from `0.56205` to `0.79005`.

## Remaining Gap

The literature boundary is credible enough for strong revise, but not for submission. The next version needs external robot/high-fidelity experiments, implemented learned baselines, trained checkpoints, and rollout evidence.
