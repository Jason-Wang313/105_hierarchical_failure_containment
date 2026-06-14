# Paper 105 Rebuild Plan: Hierarchical Failure Containment

Started: 2026-06-15 00:14:00 +0100

## Goal

Rebuild Paper 105 from a v3 archive into an honest ICLR-main-target evidence package if, and only if, the evidence supports it. The falsifiable claim is that a hierarchical robot policy can contain low-level execution failures before they corrupt mid-level subgoals or high-level task state.

## Claimed Mechanism

The proposed method, `proposed_hierarchical_failure_containment_graph`, maintains a containment graph over:

- low-level controller anomalies;
- skill-local precondition drift;
- mid-level subgoal validity;
- high-level task-state corruption;
- recovery budget and escalation rules;
- false-containment risk;
- cross-level cascade paths.

It should terminate or repair a failing skill locally when possible, escalate only when local repair would corrupt the task state, and avoid both under-containment and excessive false stops.

## Benchmark To Build

Create a RAM-light executable benchmark with aggregate metrics rather than full trajectory storage. The benchmark will cover:

- 5 tasks: drawer retrieval, peg assembly, mobile manipulation delivery, tool-use sequence, and bimanual handoff.
- 7 failure regimes: actuator slip, perception glitch, contact instability, precondition drift, subgoal drift, recovery-budget exhaustion, and cross-level cascading failure.
- 5 splits: nominal, low-level perturbation, mid-level subgoal shift, delayed escalation, and combined cascade stress.
- 9 methods: flat behavior cloning, hierarchy without containment, local safety filter, reactive retry recovery, uncertainty halt policy, option-termination monitor, failure-aware hierarchical controller, proposed hierarchical containment graph, and oracle containment supervisor.
- 7 random seeds with independent task/regime groups.
- 84 episodes per task/regime/split/method group.

## Evidence Requirements

The rebuild must produce:

- Task success, containment rate, state-corruption rate, cascade rate, damage, false halt, recovery success, escalation precision, containment latency, recovery cost, and regret to oracle.
- Per-task/per-regime breakdowns.
- Pairwise seed-level tests against the strongest non-oracle baseline.
- Stress sweep over cascade intensity.
- Ablations for local containment edges, cross-level escalation model, recovery-budget memory, task-state corruption predictor, and false-halt calibration.
- Failure cases explaining where containment is unnecessary, too conservative, or dominated by simpler recovery.
- Figures and LaTeX tables generated from CSVs.

## Terminal Gate

Mark `STRONG_REVISE` only if the proposed method:

- Beats the strongest non-oracle closed-loop baseline on combined-cascade task success by at least 0.030.
- Improves containment rate or reduces cascade rate over the strongest non-oracle baseline by at least 0.050.
- Does not buy success by increasing damage, state corruption, or false halts.
- Wins paired seed comparisons against the strongest non-oracle baseline in at least 5/7 seeds.
- Survives core ablations: removing local containment edges, cross-level escalation, recovery-budget memory, corruption prediction, or false-halt calibration must not match the full method.
- States clearly that real robot/external benchmark validation is still missing.

Otherwise mark `KILL_ARCHIVE` with evidence.

## Execution Steps

1. Replace the shared v3 probability script with a paper-specific hierarchical-failure-containment benchmark.
2. Generate metrics, seed metrics, per-task/per-regime tables, pairwise tests, stress sweep, ablations, failure cases, figures, and LaTeX tables.
3. Update repository docs to reflect the actual terminal gate.
4. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative archive report.
5. Compile and copy only `105.pdf` to `C:/Users/wangz/Downloads/105.pdf`.
6. Verify finite CSVs, py_compile, LaTeX log, PDF hash, no Desktop PDF, clean child repo, public GitHub push, and root report consistency.

## RAM Discipline

Use vectorized or aggregate group simulation and write summary tables directly. Keep all seeds, tasks, regimes, methods, stress levels, ablations, and failure cases; do not reduce experimental coverage to save memory.
