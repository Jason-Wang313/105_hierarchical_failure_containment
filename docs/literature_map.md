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

## Boundary

The paper's boundary is hierarchical containment. A hierarchy can switch skills; a safety filter can halt; a recovery policy can retry. The proposed mechanism asks whether a controller can identify the level at which a failure should be contained, repair locally when safe, and escalate before task-state corruption when local repair is unsafe.

## Local Evidence

The v4 benchmark supports the boundary under combined cascade stress: proposed success is `0.576 +/- 0.007` versus `0.492 +/- 0.006` for the strongest non-oracle baseline, containment rate improves from `0.394` to `0.515`, and state corruption drops from `0.098` to `0.053`.

## Remaining Gap

The literature boundary is credible enough for strong revise, but not for submission. The next version needs external robot/high-fidelity experiments and implemented learned baselines.
