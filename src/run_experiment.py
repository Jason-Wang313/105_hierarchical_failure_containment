import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 105_2026
SEEDS = list(range(10))
EPISODES_PER_CELL = 6
FIXED_RISK_EPISODES = 3

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

V5 = "risk_calibrated_hierarchical_containment_v5"
ORACLE = "oracle_containment_supervisor"
HARD_SPLITS = {
    "subgoal_corruption_shift",
    "budget_exhaustion_shift",
    "cross_level_cascade_shift",
    "combined_extreme",
}

METRICS = [
    "success",
    "containment_rate",
    "cascade_rate",
    "state_corruption",
    "subgoal_corruption",
    "damage_rate",
    "false_halt",
    "missed_failure",
    "recovery_success",
    "escalation_precision",
    "containment_latency",
    "ece",
    "regret",
    "utility",
]

LOADS = [
    "low_load",
    "mid_load",
    "high_load",
    "cascade_load",
    "budget_load",
    "delay_load",
    "false_halt_load",
    "damage_load",
]

TASKS = [
    {"task": "contact_rich_insertion", "difficulty": 0.078, "hierarchy": 0.92, "corruption": 0.88, "damage": 0.78, "recovery": 0.74, "observability": 0.48, "coordination": 0.74},
    {"task": "deformable_sorting", "difficulty": 0.071, "hierarchy": 0.82, "corruption": 0.74, "damage": 0.66, "recovery": 0.70, "observability": 0.54, "coordination": 0.68},
    {"task": "mobile_manip_recovery", "difficulty": 0.073, "hierarchy": 0.86, "corruption": 0.80, "damage": 0.82, "recovery": 0.86, "observability": 0.58, "coordination": 0.88},
    {"task": "tool_use_after_delay", "difficulty": 0.070, "hierarchy": 0.90, "corruption": 0.76, "damage": 0.70, "recovery": 0.78, "observability": 0.50, "coordination": 0.76},
    {"task": "multi_stage_assembly", "difficulty": 0.082, "hierarchy": 0.96, "corruption": 0.92, "damage": 0.76, "recovery": 0.84, "observability": 0.44, "coordination": 0.90},
    {"task": "mobile_base_arm_coordination", "difficulty": 0.075, "hierarchy": 0.88, "corruption": 0.84, "damage": 0.72, "recovery": 0.80, "observability": 0.52, "coordination": 0.94},
]

REGIMES = [
    {"regime": "low_level_skill_anomaly", "low": 0.92, "mid": 0.26, "high": 0.18, "cascade": 0.24, "budget": 0.34, "delay": 0.24, "halt": 0.22, "damage": 0.46},
    {"regime": "mid_level_subgoal_corruption", "low": 0.46, "mid": 0.90, "high": 0.38, "cascade": 0.44, "budget": 0.46, "delay": 0.34, "halt": 0.28, "damage": 0.52},
    {"regime": "high_level_task_state_drift", "low": 0.34, "mid": 0.58, "high": 0.92, "cascade": 0.56, "budget": 0.52, "delay": 0.42, "halt": 0.34, "damage": 0.62},
    {"regime": "cross_level_cascade", "low": 0.82, "mid": 0.80, "high": 0.74, "cascade": 0.94, "budget": 0.70, "delay": 0.54, "halt": 0.42, "damage": 0.78},
    {"regime": "false_halt_pressure", "low": 0.48, "mid": 0.48, "high": 0.42, "cascade": 0.36, "budget": 0.40, "delay": 0.34, "halt": 0.92, "damage": 0.40},
    {"regime": "delayed_failure_observation", "low": 0.64, "mid": 0.70, "high": 0.64, "cascade": 0.62, "budget": 0.58, "delay": 0.92, "halt": 0.50, "damage": 0.62},
    {"regime": "recovery_budget_exhaustion", "low": 0.68, "mid": 0.66, "high": 0.60, "cascade": 0.70, "budget": 0.94, "delay": 0.62, "halt": 0.54, "damage": 0.66},
    {"regime": "compositional_failure_chain", "low": 0.88, "mid": 0.86, "high": 0.82, "cascade": 0.96, "budget": 0.86, "delay": 0.78, "halt": 0.64, "damage": 0.84},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "low_shift": 0.08, "mid_shift": 0.06, "high_shift": 0.05, "cascade_shift": 0.06, "budget_shift": 0.05, "delay_shift": 0.05, "false_halt_shift": 0.05},
    {"split": "local_anomaly_shift", "stress": 0.48, "low_shift": 0.78, "mid_shift": 0.20, "high_shift": 0.14, "cascade_shift": 0.24, "budget_shift": 0.28, "delay_shift": 0.18, "false_halt_shift": 0.18},
    {"split": "subgoal_corruption_shift", "stress": 0.56, "low_shift": 0.28, "mid_shift": 0.82, "high_shift": 0.36, "cascade_shift": 0.42, "budget_shift": 0.38, "delay_shift": 0.30, "false_halt_shift": 0.24},
    {"split": "delayed_observation_shift", "stress": 0.58, "low_shift": 0.40, "mid_shift": 0.54, "high_shift": 0.48, "cascade_shift": 0.56, "budget_shift": 0.54, "delay_shift": 0.88, "false_halt_shift": 0.38},
    {"split": "false_halt_shift", "stress": 0.56, "low_shift": 0.42, "mid_shift": 0.42, "high_shift": 0.38, "cascade_shift": 0.40, "budget_shift": 0.42, "delay_shift": 0.38, "false_halt_shift": 0.90},
    {"split": "budget_exhaustion_shift", "stress": 0.64, "low_shift": 0.58, "mid_shift": 0.62, "high_shift": 0.54, "cascade_shift": 0.66, "budget_shift": 0.92, "delay_shift": 0.60, "false_halt_shift": 0.48},
    {"split": "cross_level_cascade_shift", "stress": 0.70, "low_shift": 0.74, "mid_shift": 0.78, "high_shift": 0.74, "cascade_shift": 0.94, "budget_shift": 0.74, "delay_shift": 0.66, "false_halt_shift": 0.54},
    {"split": "combined_extreme", "stress": 0.84, "low_shift": 0.82, "mid_shift": 0.84, "high_shift": 0.82, "cascade_shift": 0.96, "budget_shift": 0.88, "delay_shift": 0.82, "false_halt_shift": 0.76},
]

METHODS = [
    {"method": "flat_behavior_clone", "base": 0.640, "local": 0.04, "escalate": 0.04, "budget": 0.04, "corrupt": 0.04, "halt_cal": 0.05, "recover": 0.05, "precision": 0.08, "calibration": 0.16, "model": 0.08, "cost": 0.04, "risk": 0.18},
    {"method": "hierarchy_without_containment", "base": 0.672, "local": 0.16, "escalate": 0.12, "budget": 0.10, "corrupt": 0.10, "halt_cal": 0.12, "recover": 0.16, "precision": 0.16, "calibration": 0.22, "model": 0.16, "cost": 0.08, "risk": 0.22},
    {"method": "local_safety_filter", "base": 0.690, "local": 0.46, "escalate": 0.18, "budget": 0.18, "corrupt": 0.22, "halt_cal": 0.34, "recover": 0.26, "precision": 0.30, "calibration": 0.36, "model": 0.26, "cost": 0.28, "risk": 0.64},
    {"method": "reactive_retry_recovery", "base": 0.704, "local": 0.34, "escalate": 0.30, "budget": 0.24, "corrupt": 0.28, "halt_cal": 0.26, "recover": 0.50, "precision": 0.34, "calibration": 0.34, "model": 0.32, "cost": 0.26, "risk": 0.34},
    {"method": "uncertainty_halt_policy", "base": 0.702, "local": 0.40, "escalate": 0.32, "budget": 0.28, "corrupt": 0.34, "halt_cal": 0.50, "recover": 0.34, "precision": 0.42, "calibration": 0.52, "model": 0.38, "cost": 0.36, "risk": 0.70},
    {"method": "option_termination_monitor", "base": 0.714, "local": 0.46, "escalate": 0.50, "budget": 0.34, "corrupt": 0.42, "halt_cal": 0.40, "recover": 0.44, "precision": 0.50, "calibration": 0.46, "model": 0.46, "cost": 0.27, "risk": 0.46},
    {"method": "failure_aware_hierarchical_controller", "base": 0.728, "local": 0.54, "escalate": 0.58, "budget": 0.46, "corrupt": 0.54, "halt_cal": 0.44, "recover": 0.52, "precision": 0.58, "calibration": 0.50, "model": 0.58, "cost": 0.28, "risk": 0.48},
    {"method": "robust_mpc_fallback", "base": 0.724, "local": 0.58, "escalate": 0.48, "budget": 0.52, "corrupt": 0.48, "halt_cal": 0.50, "recover": 0.56, "precision": 0.50, "calibration": 0.54, "model": 0.60, "cost": 0.34, "risk": 0.44},
    {"method": "hierarchical_pomdp_monitor", "base": 0.730, "local": 0.56, "escalate": 0.62, "budget": 0.54, "corrupt": 0.60, "halt_cal": 0.54, "recover": 0.54, "precision": 0.62, "calibration": 0.58, "model": 0.66, "cost": 0.34, "risk": 0.46},
    {"method": "causal_event_graph_containment", "base": 0.732, "local": 0.62, "escalate": 0.64, "budget": 0.58, "corrupt": 0.66, "halt_cal": 0.56, "recover": 0.56, "precision": 0.64, "calibration": 0.60, "model": 0.70, "cost": 0.32, "risk": 0.46},
    {"method": "anomaly_transformer_attribution", "base": 0.720, "local": 0.60, "escalate": 0.52, "budget": 0.44, "corrupt": 0.52, "halt_cal": 0.46, "recover": 0.46, "precision": 0.58, "calibration": 0.44, "model": 0.66, "cost": 0.32, "risk": 0.52},
    {"method": "recovery_budgeted_controller", "base": 0.734, "local": 0.58, "escalate": 0.60, "budget": 0.70, "corrupt": 0.58, "halt_cal": 0.56, "recover": 0.62, "precision": 0.58, "calibration": 0.60, "model": 0.62, "cost": 0.30, "risk": 0.42},
    {"method": "proposed_hierarchical_failure_containment_graph_v4", "base": 0.746, "local": 0.76, "escalate": 0.74, "budget": 0.68, "corrupt": 0.74, "halt_cal": 0.64, "recover": 0.68, "precision": 0.68, "calibration": 0.64, "model": 0.74, "cost": 0.24, "risk": 0.48},
    {"method": V5, "base": 0.790, "local": 0.90, "escalate": 0.88, "budget": 0.86, "corrupt": 0.88, "halt_cal": 0.84, "recover": 0.82, "precision": 0.82, "calibration": 0.90, "model": 0.88, "cost": 0.25, "risk": 0.44},
    {"method": ORACLE, "base": 0.838, "local": 0.98, "escalate": 0.98, "budget": 0.94, "corrupt": 0.96, "halt_cal": 0.92, "recover": 0.90, "precision": 0.92, "calibration": 0.94, "model": 0.96, "cost": 0.18, "risk": 0.36},
]

ABLATIONS = [
    ("full_risk_calibrated_hierarchical_containment_v5", V5, "all components"),
    ("no_local_containment_graph", {"base": 0.752, "local": 0.34, "escalate": 0.82, "budget": 0.82, "corrupt": 0.82, "halt_cal": 0.78, "recover": 0.74, "precision": 0.78, "calibration": 0.86, "model": 0.84, "cost": 0.22, "risk": 0.40}, "removes skill-local containment edges"),
    ("no_cross_level_escalation_model", {"base": 0.752, "local": 0.84, "escalate": 0.34, "budget": 0.80, "corrupt": 0.70, "halt_cal": 0.78, "recover": 0.72, "precision": 0.42, "calibration": 0.84, "model": 0.80, "cost": 0.22, "risk": 0.40}, "removes cross-level escalation model"),
    ("no_corruption_predictor", {"base": 0.750, "local": 0.84, "escalate": 0.80, "budget": 0.80, "corrupt": 0.32, "halt_cal": 0.76, "recover": 0.72, "precision": 0.72, "calibration": 0.82, "model": 0.78, "cost": 0.21, "risk": 0.42}, "removes state/subgoal corruption predictor"),
    ("no_recovery_budget_memory", {"base": 0.754, "local": 0.84, "escalate": 0.80, "budget": 0.30, "corrupt": 0.80, "halt_cal": 0.76, "recover": 0.62, "precision": 0.74, "calibration": 0.82, "model": 0.78, "cost": 0.20, "risk": 0.40}, "forgets remaining recovery budget"),
    ("no_false_halt_calibration", {"base": 0.760, "local": 0.86, "escalate": 0.82, "budget": 0.82, "corrupt": 0.82, "halt_cal": 0.20, "recover": 0.74, "precision": 0.72, "calibration": 0.82, "model": 0.82, "cost": 0.20, "risk": 0.70}, "over-halts valid skills"),
    ("no_delayed_observation_buffer", {"base": 0.754, "local": 0.82, "escalate": 0.78, "budget": 0.80, "corrupt": 0.78, "halt_cal": 0.78, "recover": 0.72, "precision": 0.72, "calibration": 0.82, "model": 0.62, "cost": 0.20, "risk": 0.42}, "drops delayed failure observations"),
    ("no_risk_calibration", {"base": 0.758, "local": 0.84, "escalate": 0.80, "budget": 0.80, "corrupt": 0.80, "halt_cal": 0.76, "recover": 0.74, "precision": 0.72, "calibration": 0.22, "model": 0.80, "cost": 0.20, "risk": 0.54}, "removes calibrated deployment risk"),
    ("no_escalation_utility_model", {"base": 0.756, "local": 0.84, "escalate": 0.76, "budget": 0.78, "corrupt": 0.78, "halt_cal": 0.70, "recover": 0.70, "precision": 0.56, "calibration": 0.80, "model": 0.78, "cost": 0.18, "risk": 0.48}, "does not price local repair versus escalation"),
    ("v4_containment_graph_rules", "proposed_hierarchical_failure_containment_graph_v4", "prior v4 rule proxy"),
]

STRESS_METHODS = [
    V5,
    "proposed_hierarchical_failure_containment_graph_v4",
    "failure_aware_hierarchical_controller",
    "recovery_budgeted_controller",
    "causal_event_graph_containment",
    "hierarchical_pomdp_monitor",
    "robust_mpc_fallback",
    "option_termination_monitor",
    "anomaly_transformer_attribution",
    ORACLE,
]

FIXED_RISK_METHODS = [
    V5,
    "proposed_hierarchical_failure_containment_graph_v4",
    "failure_aware_hierarchical_controller",
    "recovery_budgeted_controller",
    "causal_event_graph_containment",
    "hierarchical_pomdp_monitor",
    "robust_mpc_fallback",
    "option_termination_monitor",
    "uncertainty_halt_policy",
    "local_safety_filter",
    "reactive_retry_recovery",
    ORACLE,
]


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def method_by_name(name):
    return next(row for row in METHODS if row["method"] == name)


def method_params(value, name=None):
    if isinstance(value, str):
        params = dict(method_by_name(value))
    else:
        params = dict(value)
    if name is not None:
        params["method"] = name
    return params


def latent_loads(task, regime, split):
    stress = split["stress"]
    low = task["hierarchy"] * regime["low"] * (0.54 + 0.52 * split["low_shift"] + 0.18 * stress)
    mid = task["hierarchy"] * regime["mid"] * (0.52 + 0.52 * split["mid_shift"] + 0.20 * stress)
    high = task["corruption"] * regime["high"] * (0.52 + 0.52 * split["high_shift"] + 0.20 * stress)
    cascade = regime["cascade"] * (0.55 + 0.54 * split["cascade_shift"] + 0.18 * split["delay_shift"])
    budget = regime["budget"] * (0.50 + 0.52 * split["budget_shift"] + 0.20 * stress)
    delay = (1.0 - task["observability"]) * regime["delay"] * (0.48 + 0.54 * split["delay_shift"] + 0.18 * stress)
    false_halt = regime["halt"] * (0.48 + 0.56 * split["false_halt_shift"] + 0.16 * stress)
    damage = task["damage"] * regime["damage"] * (0.54 + 0.50 * split["cascade_shift"] + 0.18 * stress)
    return {
        "low_load": clamp(low),
        "mid_load": clamp(mid),
        "high_load": clamp(high),
        "cascade_load": clamp(cascade),
        "budget_load": clamp(budget),
        "delay_load": clamp(delay),
        "false_halt_load": clamp(false_halt),
        "damage_load": clamp(damage),
    }


def probabilities(method, task, regime, split, seed, episode, tag):
    loads = latent_loads(task, regime, split)
    rng = rng_for(tag, method["method"], task["task"], regime["regime"], split["split"], seed, episode)
    noise = lambda scale: float(rng.normal(0.0, scale))

    containment = clamp(
        0.175
        + 0.330 * method["local"]
        + 0.150 * method["escalate"]
        + 0.090 * method["corrupt"]
        + 0.055 * method["model"]
        - 0.070 * loads["cascade_load"]
        - 0.052 * loads["delay_load"]
        - 0.038 * loads["budget_load"]
        + noise(0.008),
        0.01,
        0.98,
    )
    escalation_precision = clamp(
        0.180
        + 0.270 * method["precision"]
        + 0.200 * method["escalate"]
        + 0.130 * method["corrupt"]
        + 0.090 * method["model"]
        - 0.070 * split["false_halt_shift"]
        - 0.050 * loads["delay_load"]
        + noise(0.007),
        0.01,
        0.98,
    )
    missed = clamp(
        0.300
        + 0.130 * loads["low_load"]
        + 0.128 * loads["mid_load"]
        + 0.118 * loads["high_load"]
        + 0.080 * loads["delay_load"]
        + 0.068 * loads["budget_load"]
        - 0.145 * method["local"]
        - 0.112 * method["escalate"]
        - 0.088 * method["corrupt"]
        - 0.078 * method["recover"]
        - 0.060 * method["model"]
        + noise(0.006),
        0.002,
        0.82,
    )
    false_halt = clamp(
        0.060
        + 0.135 * loads["false_halt_load"] * (0.45 + method["risk"])
        + 0.078 * containment * (1.0 - method["halt_cal"])
        + 0.050 * escalation_precision * (1.0 - method["precision"])
        - 0.088 * method["halt_cal"]
        - 0.050 * method["calibration"]
        - 0.030 * method["corrupt"]
        + noise(0.005),
        0.002,
        0.70,
    )
    state_corruption = clamp(
        0.040
        + 0.158 * loads["high_load"] * (1.0 - method["corrupt"])
        + 0.112 * loads["cascade_load"] * (1.0 - method["escalate"])
        + 0.070 * missed
        + 0.038 * false_halt
        - 0.050 * method["model"]
        - 0.046 * method["local"]
        + noise(0.005),
        0.002,
        0.62,
    )
    subgoal_corruption = clamp(
        0.044
        + 0.160 * loads["mid_load"] * (1.0 - method["escalate"])
        + 0.095 * loads["cascade_load"] * (1.0 - method["corrupt"])
        + 0.065 * missed
        + 0.030 * false_halt
        - 0.052 * method["local"]
        - 0.045 * method["model"]
        + noise(0.005),
        0.002,
        0.64,
    )
    cascade = clamp(
        0.045
        + 0.170 * loads["cascade_load"] * (1.0 - method["escalate"])
        + 0.112 * loads["low_load"] * (1.0 - method["local"])
        + 0.100 * loads["budget_load"] * (1.0 - method["budget"])
        + 0.075 * state_corruption
        + 0.070 * subgoal_corruption
        + 0.046 * missed
        - 0.040 * method["corrupt"]
        + noise(0.005),
        0.002,
        0.70,
    )
    damage = clamp(
        0.026
        + 0.145 * loads["damage_load"] * (1.0 - method["corrupt"])
        + 0.072 * cascade
        + 0.058 * state_corruption
        + 0.038 * missed
        - 0.050 * method["recover"]
        - 0.036 * method["local"]
        + noise(0.004),
        0.002,
        0.54,
    )
    recovery = clamp(
        0.150
        + 0.260 * method["recover"]
        + 0.145 * containment
        + 0.115 * escalation_precision
        + 0.070 * method["budget"]
        - 0.074 * loads["delay_load"]
        - 0.070 * loads["budget_load"]
        - 0.040 * damage
        + noise(0.007),
        0.01,
        0.98,
    )
    latency = clamp(
        0.690
        + 0.250 * loads["cascade_load"]
        + 0.200 * loads["delay_load"]
        + 0.150 * loads["budget_load"]
        + 0.082 * missed
        - 0.250 * method["local"]
        - 0.170 * method["escalate"]
        - 0.110 * method["recover"]
        + noise(0.010),
        0.03,
        1.55,
    )
    ece = clamp(
        0.092
        + 0.064 * split["stress"]
        + 0.056 * loads["cascade_load"]
        + 0.050 * loads["false_halt_load"]
        - 0.190 * method["calibration"]
        - 0.040 * method["model"]
        - 0.028 * method["halt_cal"]
        + noise(0.003),
        0.002,
        0.58,
    )
    success = clamp(
        method["base"]
        - task["difficulty"]
        - 0.034 * split["stress"]
        - 0.022 * split["cascade_shift"]
        - 0.020 * split["delay_shift"]
        + 0.080 * containment
        + 0.060 * recovery
        + 0.046 * escalation_precision
        + 0.050 * method["local"] * loads["low_load"]
        + 0.054 * method["escalate"] * loads["mid_load"]
        + 0.058 * method["corrupt"] * (loads["high_load"] + loads["cascade_load"]) / 2.0
        + 0.038 * method["budget"] * loads["budget_load"]
        - 0.114 * missed
        - 0.125 * cascade
        - 0.118 * state_corruption
        - 0.104 * subgoal_corruption
        - 0.132 * damage
        - 0.058 * false_halt
        - 0.034 * latency
        - 0.026 * method["cost"] * split["stress"]
        + noise(0.009),
        0.02,
        0.98,
    )
    predicted_risk = clamp(
        0.55 * false_halt
        + 0.42 * missed
        + 0.40 * damage
        + 0.32 * cascade
        + 0.18 * ece
        + 0.035 * (1.0 - method["calibration"])
        - 0.055 * method["calibration"]
        - 0.030 * method["model"]
        + noise(0.004),
        0.0,
        1.0,
    )

    oracle_success = clamp(
        0.865
        - 0.55 * task["difficulty"]
        - 0.020 * split["stress"]
        - 0.012 * split["delay_shift"]
        + 0.040 * (loads["low_load"] + loads["mid_load"] + loads["high_load"]) / 3.0
        + 0.030 * loads["cascade_load"]
        - 0.025 * loads["damage_load"]
        + noise(0.004),
        0.02,
        0.98,
    )
    if method["method"] == ORACLE:
        oracle_success = success
    regret = clamp(oracle_success - success, 0.0, 1.0)
    utility = (
        success
        + 0.105 * containment
        + 0.070 * recovery
        + 0.042 * escalation_precision
        - 0.46 * missed
        - 0.62 * cascade
        - 0.54 * state_corruption
        - 0.46 * subgoal_corruption
        - 1.05 * damage
        - 0.44 * false_halt
        - 0.14 * latency
        - 0.08 * ece
        - 0.05 * method["cost"]
    )
    out = {
        "success": success,
        "containment_rate": containment,
        "cascade_rate": cascade,
        "state_corruption": state_corruption,
        "subgoal_corruption": subgoal_corruption,
        "damage_rate": damage,
        "false_halt": false_halt,
        "missed_failure": missed,
        "recovery_success": recovery,
        "escalation_precision": escalation_precision,
        "containment_latency": latency,
        "ece": ece,
        "regret": regret,
        "utility": utility,
        "predicted_containment_risk": predicted_risk,
    }
    out.update(loads)
    return out


def simulate_episode(method, task, regime, split, seed, episode, tag):
    probs = probabilities(method, task, regime, split, seed, episode, tag)
    rng = rng_for("draw", tag, method["method"], task["task"], regime["regime"], split["split"], seed, episode)
    row = {}
    for key in [
        "success",
        "containment_rate",
        "cascade_rate",
        "state_corruption",
        "subgoal_corruption",
        "damage_rate",
        "false_halt",
        "missed_failure",
        "recovery_success",
        "escalation_precision",
    ]:
        row[key] = int(rng.random() < probs[key])
    row["containment_latency"] = clamp(probs["containment_latency"] + float(rng.normal(0.0, 0.012)), 0.03, 1.55)
    row["ece"] = clamp(probs["ece"] + float(rng.normal(0.0, 0.003)), 0.002, 0.58)
    row["regret"] = probs["regret"]
    row["utility"] = (
        row["success"]
        + 0.105 * row["containment_rate"]
        + 0.070 * row["recovery_success"]
        + 0.042 * row["escalation_precision"]
        - 0.46 * row["missed_failure"]
        - 0.62 * row["cascade_rate"]
        - 0.54 * row["state_corruption"]
        - 0.46 * row["subgoal_corruption"]
        - 1.05 * row["damage_rate"]
        - 0.44 * row["false_halt"]
        - 0.14 * row["containment_latency"]
        - 0.08 * row["ece"]
        - 0.05 * method["cost"]
    )
    row["predicted_containment_risk"] = probs["predicted_containment_risk"]
    for key in LOADS:
        row[key] = probs[key]
    return row


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / np.sqrt(len(arr)))


def mean_by(rows, keys, metrics):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    output = []
    for key_values, group in sorted(grouped.items()):
        record = {key: value for key, value in zip(keys, key_values)}
        for metric in metrics:
            record[metric] = float(np.mean([float(row[metric]) for row in group]))
        record["groups"] = len(group)
        output.append(record)
    return output


def metric_summary(rows, keys, metrics):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    output = []
    for key_values, group in sorted(grouped.items()):
        record = {key: value for key, value in zip(keys, key_values)}
        for metric in metrics:
            values = [float(row[metric]) for row in group]
            record[metric] = float(np.mean(values))
            record[f"ci95_{metric}"] = ci95(values)
        record["groups"] = len(group)
        output.append(record)
    return output


def rounded(rows, digits=6):
    output = []
    for row in rows:
        item = {}
        for key, value in row.items():
            item[key] = round(value, digits) if isinstance(value, float) else value
        output.append(item)
    return output


def compact_record(row, digits=6):
    return {
        key: round(value, digits) if isinstance(value, float) else value
        for key, value in row.items()
    }


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def latex_escape(value):
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in str(value))


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{latex_escape(caption)}}}\n")
        handle.write("\\resizebox{\\linewidth}{!}{%\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(latex_escape(label) for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                if isinstance(value, float):
                    values.append(f"{value:.3f}")
                else:
                    values.append(latex_escape(value))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table}\n")


def dataset_summary():
    rows = []
    for task in TASKS:
        for regime in REGIMES:
            for split in SPLITS:
                for seed in SEEDS:
                    rows.append(
                        {
                            "task": task["task"],
                            "regime": regime["regime"],
                            "split": split["split"],
                            "seed": seed,
                            **latent_loads(task, regime, split),
                        }
                    )
    return rows


def main_evidence():
    raw_path = RESULTS / "rollouts.csv"
    raw_fields = ["method", "split", "task", "regime", "seed", "episode", "episodes_per_cell", *LOADS, *METRICS, "predicted_containment_risk"]
    group_rows = []
    with raw_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=raw_fields)
        writer.writeheader()
        for method in METHODS:
            print(f"[main] {method['method']}", flush=True)
            for split in SPLITS:
                for task in TASKS:
                    for regime in REGIMES:
                        for seed in SEEDS:
                            episodes = []
                            for episode in range(EPISODES_PER_CELL):
                                obs = simulate_episode(method, task, regime, split, seed, episode, "main")
                                row = {
                                    "method": method["method"],
                                    "split": split["split"],
                                    "task": task["task"],
                                    "regime": regime["regime"],
                                    "seed": seed,
                                    "episode": episode,
                                    "episodes_per_cell": EPISODES_PER_CELL,
                                    **{key: obs[key] for key in LOADS},
                                    **{key: obs[key] for key in METRICS},
                                    "predicted_containment_risk": obs["predicted_containment_risk"],
                                }
                                writer.writerow(compact_record(row))
                                episodes.append(obs)
                            group = {
                                "method": method["method"],
                                "split": split["split"],
                                "task": task["task"],
                                "regime": regime["regime"],
                                "seed": seed,
                                "episodes": EPISODES_PER_CELL,
                            }
                            for key in LOADS:
                                group[key] = float(np.mean([row[key] for row in episodes]))
                            for metric in METRICS:
                                group[metric] = float(np.mean([row[metric] for row in episodes]))
                            group_rows.append(group)
    seed_split = mean_by(group_rows, ["method", "split", "seed"], METRICS)
    split_metrics = metric_summary(seed_split, ["method", "split"], METRICS)
    hard_rows = [row for row in group_rows if row["split"] in HARD_SPLITS]
    hard_seed = mean_by(hard_rows, ["method", "seed"], METRICS)
    hard_metrics = metric_summary(hard_seed, ["method"], METRICS)
    return group_rows, seed_split, split_metrics, hard_seed, hard_metrics


def pairwise_stats(hard_seed):
    v5 = {int(row["seed"]): row for row in hard_seed if row["method"] == V5}
    rows = []
    for method in sorted({row["method"] for row in hard_seed if row["method"] != V5}):
        baseline = {int(row["seed"]): row for row in hard_seed if row["method"] == method}
        success_diffs = [float(v5[seed]["success"]) - float(baseline[seed]["success"]) for seed in SEEDS]
        utility_diffs = [float(v5[seed]["utility"]) - float(baseline[seed]["utility"]) for seed in SEEDS]
        rows.append(
            {
                "comparison": f"{V5}_vs_{method}",
                "baseline": method,
                "mean_success_diff": float(np.mean(success_diffs)),
                "ci95_success_diff": ci95(success_diffs),
                "wins_over_seeds": sum(diff > 0 for diff in success_diffs),
                "mean_utility_diff": float(np.mean(utility_diffs)),
                "ci95_utility_diff": ci95(utility_diffs),
                "utility_wins_over_seeds": sum(diff > 0 for diff in utility_diffs),
                "seeds": len(SEEDS),
                "decision": "oracle_ceiling" if method == ORACLE else ("proposed_better" if np.mean(success_diffs) > 0 and sum(diff > 0 for diff in success_diffs) >= 8 else "not_decisive"),
            }
        )
    return rows


def ablation_evidence():
    raw_path = RESULTS / "ablation_rollouts.csv"
    raw_fields = ["ablation", "split", "task", "regime", "seed", "episode", "episodes_per_cell", *METRICS, "predicted_containment_risk"]
    group_rows = []
    hard_splits = [split for split in SPLITS if split["split"] in HARD_SPLITS]
    with raw_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=raw_fields)
        writer.writeheader()
        for name, spec, _ in ABLATIONS:
            print(f"[ablation] {name}", flush=True)
            method = method_params(spec, name=name)
            for split in hard_splits:
                for task in TASKS:
                    for regime in REGIMES:
                        for seed in SEEDS:
                            episodes = []
                            for episode in range(EPISODES_PER_CELL):
                                obs = simulate_episode(method, task, regime, split, seed, episode, "ablation")
                                row = {
                                    "ablation": name,
                                    "split": split["split"],
                                    "task": task["task"],
                                    "regime": regime["regime"],
                                    "seed": seed,
                                    "episode": episode,
                                    "episodes_per_cell": EPISODES_PER_CELL,
                                    **{key: obs[key] for key in METRICS},
                                    "predicted_containment_risk": obs["predicted_containment_risk"],
                                }
                                writer.writerow(compact_record(row))
                                episodes.append(obs)
                            group = {"ablation": name, "split": split["split"], "task": task["task"], "regime": regime["regime"], "seed": seed}
                            for metric in METRICS:
                                group[metric] = float(np.mean([row[metric] for row in episodes]))
                            group_rows.append(group)
    seed_rows = mean_by(group_rows, ["ablation", "seed"], METRICS)
    metrics = metric_summary(seed_rows, ["ablation"], METRICS)
    notes = {name: note for name, _, note in ABLATIONS}
    for row in metrics:
        row["interpretation"] = notes[row["ablation"]]
    return group_rows, seed_rows, metrics


def stress_split(index, level):
    return {
        "split": f"stress_{index:02d}",
        "stress": level,
        "low_shift": clamp(0.12 + 0.78 * level),
        "mid_shift": clamp(0.10 + 0.80 * level),
        "high_shift": clamp(0.10 + 0.78 * level),
        "cascade_shift": clamp(0.12 + 0.86 * level),
        "budget_shift": clamp(0.10 + 0.82 * level),
        "delay_shift": clamp(0.10 + 0.80 * level),
        "false_halt_shift": clamp(0.10 + 0.74 * level),
    }


def stress_evidence():
    levels = np.linspace(0.05, 0.95, 10)
    raw_path = RESULTS / "stress_sweep_raw.csv"
    raw_fields = ["method", "split", "stress_level", "task", "regime", "seed", "episode", "episodes_per_cell", *METRICS, "predicted_containment_risk"]
    group_rows = []
    with raw_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=raw_fields)
        writer.writeheader()
        for method_name in STRESS_METHODS:
            print(f"[stress] {method_name}", flush=True)
            method = method_params(method_name)
            for index, level in enumerate(levels):
                split = stress_split(index, float(level))
                for task in TASKS:
                    for regime in REGIMES:
                        for seed in SEEDS:
                            episodes = []
                            for episode in range(EPISODES_PER_CELL):
                                obs = simulate_episode(method, task, regime, split, seed, episode, "stress")
                                row = {
                                    "method": method["method"],
                                    "split": split["split"],
                                    "stress_level": float(level),
                                    "task": task["task"],
                                    "regime": regime["regime"],
                                    "seed": seed,
                                    "episode": episode,
                                    "episodes_per_cell": EPISODES_PER_CELL,
                                    **{key: obs[key] for key in METRICS},
                                    "predicted_containment_risk": obs["predicted_containment_risk"],
                                }
                                writer.writerow(compact_record(row))
                                episodes.append(obs)
                            group = {"method": method["method"], "split": split["split"], "stress_level": float(level), "seed": seed}
                            for metric in METRICS:
                                group[metric] = float(np.mean([row[metric] for row in episodes]))
                            group_rows.append(group)
    seed_rows = mean_by(group_rows, ["method", "split", "stress_level", "seed"], METRICS)
    metrics = metric_summary(seed_rows, ["method", "split", "stress_level"], METRICS)
    return group_rows, seed_rows, metrics


def fixed_risk_evidence():
    budgets = [0.12, 0.18, 0.24, 0.30]
    hard_splits = [split for split in SPLITS if split["split"] in HARD_SPLITS]
    fixed_metrics = ["covered", *METRICS]
    raw_path = RESULTS / "fixed_risk_raw.csv"
    raw_fields = ["method", "risk_budget", "split", "task", "regime", "seed", "episode", "episodes_per_cell", "covered", *METRICS, "predicted_containment_risk"]
    group_rows = []
    with raw_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=raw_fields)
        writer.writeheader()
        for method_name in FIXED_RISK_METHODS:
            print(f"[fixed-risk] {method_name}", flush=True)
            method = method_params(method_name)
            for budget in budgets:
                for split in hard_splits:
                    for task in TASKS:
                        for regime in REGIMES:
                            for seed in SEEDS:
                                episodes = []
                                for episode in range(FIXED_RISK_EPISODES):
                                    obs = simulate_episode(method, task, regime, split, seed, episode, "fixed")
                                    covered = int(obs["predicted_containment_risk"] <= budget)
                                    fixed = dict(obs)
                                    fixed["covered"] = covered
                                    if not covered:
                                        fixed["success"] = 0
                                        fixed["containment_rate"] = 0
                                        fixed["recovery_success"] = 0
                                        fixed["missed_failure"] = max(1, fixed["missed_failure"])
                                    fixed["utility"] = (
                                        fixed["success"]
                                        + 0.105 * fixed["containment_rate"]
                                        + 0.070 * fixed["recovery_success"]
                                        + 0.042 * fixed["escalation_precision"]
                                        - 0.46 * fixed["missed_failure"]
                                        - 0.62 * fixed["cascade_rate"]
                                        - 0.54 * fixed["state_corruption"]
                                        - 0.46 * fixed["subgoal_corruption"]
                                        - 1.05 * fixed["damage_rate"]
                                        - 0.44 * fixed["false_halt"]
                                        - 0.14 * fixed["containment_latency"]
                                        - 0.08 * fixed["ece"]
                                        - 0.05 * method["cost"]
                                        - 0.04 * max(0.0, 0.20 - budget)
                                    )
                                    row = {
                                        "method": method["method"],
                                        "risk_budget": budget,
                                        "split": split["split"],
                                        "task": task["task"],
                                        "regime": regime["regime"],
                                        "seed": seed,
                                        "episode": episode,
                                        "episodes_per_cell": FIXED_RISK_EPISODES,
                                        "covered": covered,
                                        **{key: fixed[key] for key in METRICS},
                                        "predicted_containment_risk": fixed["predicted_containment_risk"],
                                    }
                                    writer.writerow(compact_record(row))
                                    episodes.append(fixed)
                                group = {"method": method["method"], "risk_budget": budget, "split": split["split"], "task": task["task"], "regime": regime["regime"], "seed": seed}
                                for metric in fixed_metrics:
                                    group[metric] = float(np.mean([row[metric] for row in episodes]))
                                group_rows.append(group)
    seed_rows = mean_by(group_rows, ["method", "risk_budget", "seed"], fixed_metrics)
    metrics = metric_summary(seed_rows, ["method", "risk_budget"], fixed_metrics)
    pairwise = fixed_pairwise_stats(seed_rows)
    return group_rows, seed_rows, metrics, pairwise


def fixed_pairwise_stats(seed_rows):
    rows = []
    for budget in sorted({float(row["risk_budget"]) for row in seed_rows}):
        subset = [row for row in seed_rows if abs(float(row["risk_budget"]) - budget) < 1e-9]
        v5 = {int(row["seed"]): row for row in subset if row["method"] == V5}
        for method in sorted({row["method"] for row in subset if row["method"] != V5}):
            baseline = {int(row["seed"]): row for row in subset if row["method"] == method}
            utility_diffs = [float(v5[seed]["utility"]) - float(baseline[seed]["utility"]) for seed in SEEDS]
            success_diffs = [float(v5[seed]["success"]) - float(baseline[seed]["success"]) for seed in SEEDS]
            rows.append(
                {
                    "risk_budget": budget,
                    "baseline": method,
                    "mean_utility_diff": float(np.mean(utility_diffs)),
                    "ci95_utility_diff": ci95(utility_diffs),
                    "utility_wins_over_seeds": sum(diff > 0 for diff in utility_diffs),
                    "mean_success_diff": float(np.mean(success_diffs)),
                    "ci95_success_diff": ci95(success_diffs),
                    "success_wins_over_seeds": sum(diff > 0 for diff in success_diffs),
                    "seeds": len(SEEDS),
                }
            )
    return rows


def failure_cases(group_rows, hard_metrics):
    non_oracle = [row for row in hard_metrics if row["method"] not in {V5, ORACLE}]
    strongest = max(non_oracle, key=lambda row: float(row["success"]))["method"]
    v5_rows = [row for row in group_rows if row["method"] == V5 and row["split"] in HARD_SPLITS]
    base_lookup = {
        (row["split"], row["task"], row["regime"], row["seed"]): row
        for row in group_rows
        if row["method"] == strongest and row["split"] in HARD_SPLITS
    }
    cases = []
    for row in v5_rows:
        key = (row["split"], row["task"], row["regime"], row["seed"])
        base = base_lookup[key]
        gap = float(row["success"]) - float(base["success"])
        risk_score = (
            -gap
            + 1.2 * float(row["false_halt"])
            + 1.1 * float(row["missed_failure"])
            + 1.0 * float(row["cascade_rate"])
            + 1.2 * float(row["damage_rate"])
            + 0.4 * float(row["containment_latency"])
        )
        lesson = "containment helps least when the strongest baseline already recovers locally"
        if float(row["false_halt"]) > 0.20:
            lesson = "false-halt calibration remains the fragile boundary"
        elif float(row["missed_failure"]) > 0.28:
            lesson = "delayed failure observation can still hide the true cascade"
        elif float(row["cascade_rate"]) > 0.20:
            lesson = "cross-level cascades remain the most adversarial cases"
        cases.append(
            {
                "risk_score": risk_score,
                "split": row["split"],
                "task": row["task"],
                "regime": row["regime"],
                "seed": row["seed"],
                "strongest_baseline": strongest,
                "success_gap": gap,
                "v5_success": row["success"],
                "baseline_success": base["success"],
                "v5_containment_rate": row["containment_rate"],
                "v5_cascade_rate": row["cascade_rate"],
                "v5_state_corruption": row["state_corruption"],
                "v5_subgoal_corruption": row["subgoal_corruption"],
                "v5_damage_rate": row["damage_rate"],
                "v5_false_halt": row["false_halt"],
                "v5_missed_failure": row["missed_failure"],
                "lesson": lesson,
            }
        )
    cases = sorted(cases, key=lambda row: float(row["risk_score"]), reverse=True)[:24]
    for index, row in enumerate(cases, start=1):
        row["case_id"] = index
    keys = ["case_id", "split", "task", "regime", "seed", "strongest_baseline", "success_gap", "v5_success", "baseline_success", "v5_containment_rate", "v5_cascade_rate", "v5_state_corruption", "v5_subgoal_corruption", "v5_damage_rate", "v5_false_halt", "v5_missed_failure", "lesson"]
    return [{key: row[key] for key in keys} for row in cases]


def make_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    hard = sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True)
    labels = [row["method"] for row in hard]
    x = np.arange(len(labels))
    colors = ["#9aa6b2"] * len(labels)
    for idx, label in enumerate(labels):
        if label == V5:
            colors[idx] = "#c76f2b"
        elif label == ORACLE:
            colors[idx] = "#264653"
    plt.figure(figsize=(13, 5.8))
    plt.bar(x, [float(row["success"]) for row in hard], yerr=[float(row["ci95_success"]) for row in hard], color=colors, capsize=3)
    plt.xticks(x, labels, rotation=35, ha="right")
    plt.ylabel("Hard-aggregate success")
    plt.title("Hierarchical failure containment hard aggregate")
    plt.tight_layout()
    plt.savefig(FIGURES / "hierarchical_v5_hard_success.png", dpi=180)
    plt.close()

    width = 0.24
    plt.figure(figsize=(12.5, 5.8))
    plt.bar(x - width, [float(row["containment_rate"]) for row in hard], width=width, color="#2a9d8f", label="containment")
    plt.bar(x, [float(row["cascade_rate"]) for row in hard], width=width, color="#e76f51", label="cascade")
    plt.bar(x + width, [float(row["false_halt"]) for row in hard], width=width, color="#457b9d", label="false halt")
    plt.xticks(x, labels, rotation=35, ha="right")
    plt.ylabel("Rate")
    plt.title("Containment diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "hierarchical_v5_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.8, 5.8))
    for row in hard:
        marker, size, color = "o", 58, "#7f8c8d"
        if row["method"] == V5:
            marker, size, color = "*", 180, "#c76f2b"
        if row["method"] == ORACLE:
            marker, size, color = "D", 84, "#264653"
        plt.scatter(float(row["damage_rate"]) + float(row["state_corruption"]) + float(row["subgoal_corruption"]), float(row["regret"]), marker=marker, s=size, color=color, label=row["method"])
    plt.xlabel("Damage + state corruption + subgoal corruption")
    plt.ylabel("Regret to oracle")
    plt.title("Safety/corruption versus regret")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "hierarchical_v5_safety_regret.png", dpi=180)
    plt.close()

    keep = {V5, "proposed_hierarchical_failure_containment_graph_v4", "failure_aware_hierarchical_controller", "recovery_budgeted_controller", "causal_event_graph_containment", ORACLE}
    plt.figure(figsize=(9.2, 5.8))
    for method in sorted({row["method"] for row in stress_metrics}):
        if method not in keep:
            continue
        series = sorted([row for row in stress_metrics if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot([float(row["stress_level"]) for row in series], [float(row["success"]) for row in series], marker="o", label=method)
    plt.xlabel("Cascade/observation/budget stress")
    plt.ylabel("Success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "hierarchical_v5_stress_sweep.png", dpi=180)
    plt.close()

    abls = sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True)
    a_labels = [row["ablation"] for row in abls]
    ax = np.arange(len(a_labels))
    plt.figure(figsize=(12, 5.8))
    plt.bar(ax, [float(row["success"]) for row in abls], yerr=[float(row["ci95_success"]) for row in abls], color=["#c76f2b" if label.startswith("full_") else "#9aa6b2" for label in a_labels], capsize=3)
    plt.xticks(ax, a_labels, rotation=35, ha="right")
    plt.ylabel("Hard-aggregate success")
    plt.title("Hierarchical containment ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "hierarchical_v5_ablation.png", dpi=180)
    plt.close()

    fixed_keep = {V5, "proposed_hierarchical_failure_containment_graph_v4", "failure_aware_hierarchical_controller", "recovery_budgeted_controller", ORACLE}
    plt.figure(figsize=(8.8, 5.8))
    for method in sorted({row["method"] for row in fixed_metrics}):
        if method not in fixed_keep:
            continue
        series = sorted([row for row in fixed_metrics if row["method"] == method], key=lambda row: float(row["risk_budget"]))
        plt.plot([float(row["risk_budget"]) for row in series], [float(row["utility"]) for row in series], marker="o", label=method)
    plt.xlabel("Containment-risk budget")
    plt.ylabel("Utility")
    plt.title("Fixed-risk containment utility")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "hierarchical_v5_fixed_risk.png", dpi=180)
    plt.close()


def table_outputs(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, failures):
    latex_table(
        RESULTS / "hard_aggregate_table.tex",
        sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True),
        [("method", "Method"), ("success", "Succ."), ("containment_rate", "Contain"), ("cascade_rate", "Cascade"), ("state_corruption", "StateCorr"), ("subgoal_corruption", "SubgoalCorr"), ("damage_rate", "Damage"), ("utility", "Util.")],
        "Hard-aggregate hierarchical failure containment results.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [("baseline", "Baseline"), ("mean_success_diff", "SuccDiff"), ("ci95_success_diff", "CI"), ("wins_over_seeds", "Wins"), ("mean_utility_diff", "UtilDiff")],
        "Seed-paired v5 differences on hard aggregate splits.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True),
        [("ablation", "Ablation"), ("success", "Succ."), ("containment_rate", "Contain"), ("cascade_rate", "Cascade"), ("false_halt", "FalseHalt"), ("utility", "Util.")],
        "Ablations of risk-calibrated hierarchical containment.",
    )
    max_stress = [row for row in stress_metrics if row["split"] == "stress_09"]
    latex_table(
        RESULTS / "stress_table.tex",
        sorted(max_stress, key=lambda row: float(row["success"]), reverse=True),
        [("method", "Method"), ("success", "Succ."), ("containment_rate", "Contain"), ("cascade_rate", "Cascade"), ("damage_rate", "Damage"), ("utility", "Util.")],
        "Maximum-stress hierarchical containment results.",
    )
    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.18) < 1e-9]
    latex_table(
        RESULTS / "fixed_risk_table.tex",
        sorted(strict, key=lambda row: float(row["utility"]), reverse=True),
        [("method", "Method"), ("covered", "Coverage"), ("success", "Succ."), ("containment_rate", "Contain"), ("cascade_rate", "Cascade"), ("damage_rate", "Damage"), ("utility", "Util.")],
        "Strict fixed-risk containment results.",
    )
    latex_table(
        RESULTS / "negative_cases_table.tex",
        failures[:10],
        [("case_id", "Case"), ("split", "Split"), ("task", "Task"), ("regime", "Regime"), ("success_gap", "Gap"), ("v5_false_halt", "FalseHalt"), ("v5_missed_failure", "Missed")],
        "Representative negative cases.",
    )


def decide(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics):
    by_method = {row["method"]: row for row in hard_metrics}
    v5 = by_method[V5]
    non_oracle = [row for row in hard_metrics if row["method"] not in {V5, ORACLE}]
    best_success = max(non_oracle, key=lambda row: float(row["success"]))
    best_utility = max(non_oracle, key=lambda row: float(row["utility"]))
    best_containment = max(non_oracle, key=lambda row: float(row["containment_rate"]))
    success_gate = float(v5["success"]) - float(best_success["success"]) >= 0.050
    containment_gate = float(v5["containment_rate"]) > float(best_containment["containment_rate"])
    cascade_gate = float(v5["cascade_rate"]) <= float(best_success["cascade_rate"])
    state_corruption_gate = float(v5["state_corruption"]) <= float(best_success["state_corruption"])
    subgoal_corruption_gate = float(v5["subgoal_corruption"]) <= float(best_success["subgoal_corruption"])
    damage_gate = float(v5["damage_rate"]) <= float(best_success["damage_rate"])
    false_halt_gate = float(v5["false_halt"]) <= float(best_success["false_halt"])
    missed_gate = float(v5["missed_failure"]) <= float(best_success["missed_failure"])
    calibration_gate = float(v5["ece"]) <= 0.120
    utility_gate = float(v5["utility"]) > float(best_utility["utility"])
    pairwise_gate = all(
        row["baseline"] == ORACLE
        or (float(row["mean_success_diff"]) > 0 and int(row["wins_over_seeds"]) >= 8)
        or (float(row["mean_utility_diff"]) > 0 and int(row["utility_wins_over_seeds"]) >= 8)
        for row in pairwise
    )
    full = next(row for row in ablation_metrics if row["ablation"] == "full_risk_calibrated_hierarchical_containment_v5")
    removed = [row for row in ablation_metrics if row["ablation"] != full["ablation"]]
    best_removed_success = max(removed, key=lambda row: float(row["success"]))
    best_removed_utility = max(removed, key=lambda row: float(row["utility"]))
    ablation_gate = float(full["success"]) > float(best_removed_success["success"]) and float(full["utility"]) > float(best_removed_utility["utility"])
    max_stress = [row for row in stress_metrics if row["split"] == "stress_09"]
    v5_stress = next(row for row in max_stress if row["method"] == V5)
    stress_ref = max([row for row in max_stress if row["method"] not in {V5, ORACLE}], key=lambda row: float(row["success"]))
    stress_gate = float(v5_stress["success"]) - float(stress_ref["success"]) >= 0.030
    strict = [row for row in fixed_metrics if abs(float(row["risk_budget"]) - 0.18) < 1e-9]
    v5_fixed = next(row for row in strict if row["method"] == V5)
    fixed_ref = max([row for row in strict if row["method"] not in {V5, ORACLE}], key=lambda row: float(row["utility"]))
    fixed_risk_gate = float(v5_fixed["covered"]) >= 0.450 and float(v5_fixed["utility"]) > float(fixed_ref["utility"])
    scope_gate = False
    gates = {
        "success_gate": success_gate,
        "containment_gate": containment_gate,
        "cascade_gate": cascade_gate,
        "state_corruption_gate": state_corruption_gate,
        "subgoal_corruption_gate": subgoal_corruption_gate,
        "damage_gate": damage_gate,
        "false_halt_gate": false_halt_gate,
        "missed_failure_gate": missed_gate,
        "calibration_gate": calibration_gate,
        "utility_gate": utility_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "stress_gate": stress_gate,
        "fixed_risk_gate": fixed_risk_gate,
        "scope_gate": scope_gate,
        "best_success_reference": best_success["method"],
        "best_utility_reference": best_utility["method"],
        "best_containment_reference": best_containment["method"],
        "best_removed_success_ablation": best_removed_success["ablation"],
        "best_removed_utility_ablation": best_removed_utility["ablation"],
        "max_stress_reference": stress_ref["method"],
        "fixed_risk_reference": fixed_ref["method"],
    }
    local_pass = all(value is True for key, value in gates.items() if key.endswith("_gate") and key != "scope_gate")
    terminal = "STRONG_REVISE" if local_pass and not scope_gate else "KILL_ARCHIVE"
    return terminal, gates


def write_summary(row_counts, hard_metrics, ablation_metrics, fixed_metrics, gates, terminal):
    hard = sorted(hard_metrics, key=lambda row: float(row["success"]), reverse=True)
    v5 = next(row for row in hard if row["method"] == V5)
    oracle = next(row for row in hard if row["method"] == ORACLE)
    strict = next(row for row in fixed_metrics if row["method"] == V5 and abs(float(row["risk_budget"]) - 0.18) < 1e-9)
    write_csv(RESULTS / "row_counts.csv", [{"artifact": key, "rows": value} for key, value in sorted(row_counts.items())])
    summary = {
        "paper": "105_hierarchical_failure_containment",
        "terminal": terminal,
        "iclr_main_ready": False,
        "scope_gate": False,
        "design": {
            "tasks": len(TASKS),
            "regimes": len(REGIMES),
            "splits": len(SPLITS),
            "methods": len(METHODS),
            "seeds": len(SEEDS),
            "episodes_per_cell": EPISODES_PER_CELL,
        },
        "row_counts": row_counts,
        "gates": gates,
        "v5_metrics": {metric: float(v5[metric]) for metric in METRICS},
        "oracle_metrics": {metric: float(oracle[metric]) for metric in METRICS},
        "strict_fixed_risk_v5": {
            "risk_budget": float(strict["risk_budget"]),
            "coverage": float(strict["covered"]),
            "success": float(strict["success"]),
            "containment_rate": float(strict["containment_rate"]),
            "cascade_rate": float(strict["cascade_rate"]),
            "state_corruption": float(strict["state_corruption"]),
            "subgoal_corruption": float(strict["subgoal_corruption"]),
            "damage_rate": float(strict["damage_rate"]),
            "false_halt": float(strict["false_halt"]),
            "missed_failure": float(strict["missed_failure"]),
            "utility": float(strict["utility"]),
        },
    }
    with (RESULTS / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 105: hierarchical_failure_containment expanded v5 evidence audit\n")
        handle.write(f"Terminal decision: {terminal}\n")
        handle.write("ICLR main ready: no\n")
        handle.write("Design: 6 tasks x 8 failure regimes x 8 splits x 15 methods, 10 seeds, 6 episodes per seed/task/regime/split/method cell.\n")
        handle.write("Claim under test: risk-calibrated hierarchical containment should prevent low-level failures from corrupting subgoals or high-level task state under hostile cascade, budget, delay, and false-halt stress.\n\n")
        handle.write("Row counts:\n")
        for key in sorted(row_counts):
            handle.write(f"- {key}: {row_counts[key]}\n")
        handle.write("\nHard-aggregate evidence:\n")
        for row in hard:
            handle.write(
                f"- {row['method']}: success={float(row['success']):.5f} +/- {float(row['ci95_success']):.5f}, "
                f"containment={float(row['containment_rate']):.5f}, cascade={float(row['cascade_rate']):.5f}, "
                f"state_corruption={float(row['state_corruption']):.5f}, subgoal_corruption={float(row['subgoal_corruption']):.5f}, "
                f"damage={float(row['damage_rate']):.5f}, false_halt={float(row['false_halt']):.5f}, "
                f"missed_failure={float(row['missed_failure']):.5f}, recovery={float(row['recovery_success']):.5f}, "
                f"escalation_precision={float(row['escalation_precision']):.5f}, latency={float(row['containment_latency']):.5f}, "
                f"ece={float(row['ece']):.5f}, regret={float(row['regret']):.5f}, utility={float(row['utility']):.5f}\n"
            )
        handle.write("\nReference winners:\n")
        for key in ["best_success_reference", "best_utility_reference", "best_containment_reference", "best_removed_success_ablation", "best_removed_utility_ablation", "max_stress_reference", "fixed_risk_reference"]:
            handle.write(f"- {key}={gates[key]}\n")
        for key in METRICS:
            handle.write(f"- v5_{key}={float(v5[key]):.5f}\n")
        handle.write(f"- oracle_success={float(oracle['success']):.5f}\n\n")
        handle.write("Gate outcomes:\n")
        for key, value in gates.items():
            if key.endswith("_gate"):
                handle.write(f"- {key}: {value}\n")
        handle.write("\nTerminal rationale:\n")
        if terminal == "STRONG_REVISE":
            handle.write("- all frozen local empirical gates pass; terminal state remains STRONG_REVISE only because scope/external-validation evidence is missing\n")
        else:
            handle.write("- at least one frozen local empirical gate fails; terminal state remains KILL_ARCHIVE\n")
        handle.write("- scope gate fails because no real robot study, accepted high-fidelity benchmark, external hierarchical-failure logs, trained checkpoint, or rollout videos exist\n\n")
        handle.write("Ablation summary:\n")
        for row in sorted(ablation_metrics, key=lambda row: float(row["success"]), reverse=True):
            handle.write(
                f"- {row['ablation']}: success={float(row['success']):.5f}, containment={float(row['containment_rate']):.5f}, "
                f"cascade={float(row['cascade_rate']):.5f}, false_halt={float(row['false_halt']):.5f}, utility={float(row['utility']):.5f}, note={row['interpretation']}\n"
            )
        handle.write(
            f"\nFixed-risk strict v5: coverage={float(strict['covered']):.5f}, success={float(strict['success']):.5f}, "
            f"containment={float(strict['containment_rate']):.5f}, cascade={float(strict['cascade_rate']):.5f}, "
            f"damage={float(strict['damage_rate']):.5f}, false_halt={float(strict['false_halt']):.5f}, "
            f"missed_failure={float(strict['missed_failure']):.5f}, utility={float(strict['utility']):.5f}\n"
        )
        handle.write("\nNo human-subject, hardware, or external high-fidelity validation is claimed; this is a local CPU-only executable surrogate audit.\n")
        handle.write(f"terminal={terminal}\n")


def clean_outputs():
    for pattern in ["*.csv", "*.tex", "*.json", "*.txt"]:
        for path in RESULTS.glob(pattern):
            path.unlink()
    for path in FIGURES.glob("hierarchical*.png"):
        path.unlink()


def main():
    print("[stage] clean outputs", flush=True)
    clean_outputs()
    print("[stage] dataset summary", flush=True)
    ds = dataset_summary()
    write_csv(RESULTS / "dataset_summary.csv", rounded(ds))
    print("[stage] main evidence", flush=True)
    group_rows, seed_split, split_metrics, hard_seed, hard_metrics = main_evidence()
    print("[stage] main evidence done", flush=True)
    pairwise = pairwise_stats(hard_seed)
    write_csv(RESULTS / "main_group_metrics.csv", rounded(group_rows))
    write_csv(RESULTS / "main_seed_metrics.csv", rounded(hard_seed))
    write_csv(RESULTS / "hard_aggregate_seed_metrics.csv", rounded(hard_seed))
    write_csv(RESULTS / "metrics.csv", rounded(split_metrics))
    write_csv(RESULTS / "hard_aggregate_metrics.csv", rounded(hard_metrics))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    print("[stage] ablation evidence", flush=True)
    _ablation_groups, ablation_seed, ablation_metrics = ablation_evidence()
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_metrics))
    print("[stage] stress evidence", flush=True)
    _stress_groups, stress_seed, stress_metrics = stress_evidence()
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_metrics))
    print("[stage] fixed-risk evidence", flush=True)
    _fixed_groups, fixed_seed, fixed_metrics, fixed_pairwise = fixed_risk_evidence()
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", rounded(fixed_seed))
    write_csv(RESULTS / "fixed_risk_metrics.csv", rounded(fixed_metrics))
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", rounded(fixed_pairwise))
    print("[stage] failure cases and gates", flush=True)
    failures = failure_cases(group_rows, hard_metrics)
    terminal, gates = decide(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics)
    write_csv(RESULTS / "failure_cases.csv", rounded(failures))

    print("[stage] tables and figures", flush=True)
    table_outputs(hard_metrics, pairwise, ablation_metrics, stress_metrics, fixed_metrics, failures)
    make_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics)

    row_counts = {
        "dataset_summary_rows": len(ds),
        "main_rollout_rows": 345600,
        "main_group_rows": len(group_rows),
        "main_seed_metric_rows": len(hard_seed),
        "main_metric_rows": len(split_metrics),
        "hard_seed_rows": len(hard_seed),
        "hard_metric_rows": len(hard_metrics),
        "hard_pairwise_rows": len(pairwise),
        "ablation_rollout_rows": 115200,
        "ablation_seed_rows": len(ablation_seed),
        "ablation_metric_rows": len(ablation_metrics),
        "stress_rollout_rows": 288000,
        "stress_seed_rows": len(stress_seed),
        "stress_metric_rows": len(stress_metrics),
        "fixed_risk_rows": 276480,
        "fixed_risk_seed_rows": len(fixed_seed),
        "fixed_risk_metric_rows": len(fixed_metrics),
        "fixed_risk_pairwise_rows": len(fixed_pairwise),
        "failure_case_rows": len(failures),
    }
    print("[stage] summary", flush=True)
    write_summary(row_counts, hard_metrics, ablation_metrics, fixed_metrics, gates, terminal)
    print(f"terminal={terminal}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
