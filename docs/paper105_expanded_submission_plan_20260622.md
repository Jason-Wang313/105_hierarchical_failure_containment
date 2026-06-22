# Paper 105 Expanded Submission Plan

Date: 2026-06-22

Paper: `105_hierarchical_failure_containment`

Target: rebuild the v4.1 local audit into a 25+ page hostile-review v5 evidence package. The paper must test whether hierarchical robot policies can contain low-level failures before they corrupt subgoals or high-level task state under stronger baselines, adversarial stress, ablations, fixed-risk deployment budgets, and explicit scope gating.

## Frozen Claim

Hierarchical robot policies need an explicit failure-containment state that separates low-level skill anomalies, mid-level subgoal corruption, high-level task-state corruption, recovery-budget exhaustion, and false-halt pressure. The v5 method must beat strong non-oracle hierarchy, option-termination, recovery, uncertainty, causal-event, and risk-budget baselines while reporting safety tradeoffs honestly.

The paper must not claim ICLR-main readiness unless external robot or accepted high-fidelity validation exists. Local CPU-only evidence can support only `STRONG_REVISE`.

## Frozen Design

The v5 runner will use a RAM-light streaming design with raw rollout persistence:

- 6 tasks: `contact_rich_insertion`, `deformable_sorting`, `mobile_manip_recovery`, `tool_use_after_delay`, `multi_stage_assembly`, `mobile_base_arm_coordination`.
- 8 failure regimes: `low_level_skill_anomaly`, `mid_level_subgoal_corruption`, `high_level_task_state_drift`, `cross_level_cascade`, `false_halt_pressure`, `delayed_failure_observation`, `recovery_budget_exhaustion`, `compositional_failure_chain`.
- 8 splits: `nominal`, `local_anomaly_shift`, `subgoal_corruption_shift`, `delayed_observation_shift`, `false_halt_shift`, `budget_exhaustion_shift`, `cross_level_cascade_shift`, `combined_extreme`.
- 15 methods: `flat_behavior_clone`, `hierarchy_without_containment`, `local_safety_filter`, `reactive_retry_recovery`, `uncertainty_halt_policy`, `option_termination_monitor`, `failure_aware_hierarchical_controller`, `robust_mpc_fallback`, `hierarchical_pomdp_monitor`, `causal_event_graph_containment`, `anomaly_transformer_attribution`, `recovery_budgeted_controller`, `proposed_hierarchical_failure_containment_graph_v4`, `risk_calibrated_hierarchical_containment_v5`, `oracle_containment_supervisor`.
- 10 seeds.
- 6 episodes per factorial cell.

Expected main coverage:

- Dataset summaries: 3,840 rows.
- Raw main rollouts: 345,600 rows.
- Main group metrics: 57,600 rows.
- Main seed metrics: 150 rows.
- Main split metrics: 120 rows.
- Hard aggregate seed metrics: 150 rows.
- Hard aggregate metrics: 15 rows.
- Pairwise tests: 14 comparisons.

## Frozen Additional Experiments

- Ablations: full v5 plus removals of local containment graph, cross-level escalation model, corruption predictor, recovery-budget memory, false-halt calibration, delayed observation buffer, risk calibration, and escalation utility model.
- Stress sweep: cascade severity, observation delay, subgoal drift, budget pressure, and false-halt pressure across 10 levels.
- Fixed-risk containment budgets: strict escalation/intervention budgets with coverage, success, corruption, cascade, damage, missed failure, false halt, and utility reported honestly.
- Negative cases: at least 24 generated cases where simpler baselines are close, containment is late, local repair corrupts task state, or the v5 method over-halts.

## Frozen Metrics

Primary metrics:

- Task success.
- Containment rate.
- Cascade rate.
- State-corruption rate.
- Subgoal-corruption rate.
- Damage rate.
- False-halt rate.
- Missed-failure rate.
- Recovery success.
- Escalation precision.
- Containment latency.
- Calibration ECE.
- Regret to oracle.
- Utility.

Fixed-risk metrics:

- Coverage.
- Conditional success.
- Containment.
- Cascade.
- State corruption.
- Damage.
- False halt.
- Missed failure.
- Utility.

## Frozen Gates

Local `STRONG_REVISE` requires all of the following:

- v5 hard-aggregate success beats the strongest non-oracle baseline by at least 0.05.
- v5 containment improves over the best non-oracle containment baseline.
- v5 cascade, state-corruption, subgoal-corruption, damage, false-halt, and missed-failure rates are no worse than the strongest non-oracle success reference.
- v5 ECE is below 0.12.
- v5 utility beats the best non-oracle utility baseline.
- Paired seed tests against every non-oracle baseline are positive on success or utility; v5 is expected to lose to the oracle.
- Full v5 beats every removed-component ablation on hard-aggregate success or utility.
- Maximum-stress v5 remains above the strongest non-oracle success reference.
- Strict fixed-risk containment keeps nontrivial coverage and better utility than the strongest non-oracle fixed-risk reference.

The paper remains `not ICLR-main-ready` unless at least one accepted scope-evidence source exists:

- real robot experiments,
- an accepted high-fidelity simulator benchmark,
- an external benchmark with trained policies,
- calibrated real hierarchical-failure logs,
- released trained checkpoints, or
- rollout videos from a real or high-fidelity system.

## Execution Order

1. Replace the v4.1 aggregate runner with the frozen v5 streaming runner.
2. Run the full CPU-only experiment and keep memory bounded by streaming raw rollouts to CSV.
3. Generate all tables, figures, summaries, stress tests, fixed-risk results, and negative cases from CSV/JSON outputs only.
4. Generate a 25+ page manuscript with bright boxed clickable citations and an explicit scope-gate decision.
5. Compile LaTeX, copy only `C:/Users/wangz/Downloads/105.pdf`, and do not place any PDF on the visible Desktop.
6. Validate row counts, finite values, PDF page count, SHA256, boxed citation settings, stale documentation, and GitHub public push.
7. Update root ledgers only after the child repo, canonical PDF, and GitHub checks pass.

## Expected Terminal Honesty

If v5 passes local gates but lacks external validation, the terminal state is `STRONG_REVISE`, `ICLR main ready: no`.

If any local gate fails, the terminal state becomes `KILL_ARCHIVE`, even if the manuscript is 25+ pages.
