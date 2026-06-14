# Hostile Prior Work

The closest threats are methods that already use hierarchical control, option termination, safety filters, recovery policies, or failure-aware task planning.

- Options formalize temporally extended actions and termination.
- Option-Critic learns options and termination conditions.
- HIRO-style methods learn hierarchical policies for long-horizon control.
- Recovery RL and recovery-chain methods learn policies that recover from unsafe or failed states.
- Vision-language-action failure recovery systems reason about failures and recovery in task hierarchies.
- Conservative safety filters and uncertainty halt policies already reduce damage by stopping risky actions.

The v4 novelty boundary is therefore narrow: Paper 105 is not "use a hierarchy" and not "add a safety filter." It must show containment of failures before they corrupt higher-level task state, while avoiding excessive false stops.

Current evidence supports this boundary locally, but real robot or independent high-fidelity validation remains required.
