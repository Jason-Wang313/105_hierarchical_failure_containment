# Claims

- Mechanism claim: hierarchical robot policies can contain low-level failures before they corrupt subgoals or task state.
- Method claim: a containment graph over local skill anomalies, cross-level escalation, recovery budgets, corruption prediction, and false-halt calibration can decide when to repair locally versus escalate.
- Evidence claim: in the local benchmark, the proposed graph beats the strongest non-oracle baseline by `0.084 +/- 0.009` combined-cascade success and wins `7/7` paired seeds.
- Safety claim: the proposed graph lowers state corruption, cascade rate, and damage relative to the strongest non-oracle baseline.
- Scope claim: the evidence supports a strong-revise decision only; it does not establish real-robot deployment performance.
- Unsupported claim explicitly avoided: no claim of ICLR-main readiness or state-of-the-art robot performance.
