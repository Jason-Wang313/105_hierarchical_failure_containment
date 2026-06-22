# Paper 105 Terminal Audit

Date: 2026-06-22

## Summary

Paper 105 was rebuilt under the expanded v5 submission-hardening standard. The rebuild created a frozen plan, replaced the experiment runner, generated a 28-page manuscript, validated all result artifacts, and copied the numbered PDF only to Downloads.

## Key Results

- v5 hard success: `0.83828 +/- 0.00599`
- strongest non-oracle hard success: `0.74167 +/- 0.00595`
- v5 containment: `0.65243`
- v5 cascade: `0.04175`
- v5 state corruption: `0.00217`
- v5 subgoal corruption: `0.00182`
- v5 damage: `0.00182`
- v5 false halt: `0.00582`
- v5 missed failure: `0.14332`
- v5 utility: `0.79005`
- v5 regret to oracle: `0.11311`
- oracle hard success: `0.91510`
- strict fixed-risk budget `0.18`: coverage `1.00000`, success `0.83854`, utility `0.79059`

## Validation

`python scripts/validate_submission_artifacts.py` passed with:

`validated Paper 105 artifacts: pages=28, sha256=182EC42D72A4E8B18EEE96884078C28006BB42CEF4DA2EE1A6C170AB6E6AF061`

## Terminal Decision

`STRONG_REVISE`, ICLR main ready: no.

The local evidence is strong enough to continue, but external robot or independent high-fidelity validation is required before submission.
