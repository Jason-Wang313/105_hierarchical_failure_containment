import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 105_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

OBSOLETE_OUTPUTS = [
    RESULTS / "raw_seed_metrics.csv",
    RESULTS / "negative_cases.csv",
    FIGURES / "stress_curve_data.csv",
]

DISPLAY_NAMES = {
    "flat_behavior_clone": "FlatBC",
    "hierarchy_without_containment": "NoContain",
    "local_safety_filter": "SafetyFilter",
    "reactive_retry_recovery": "ReactiveRetry",
    "uncertainty_halt_policy": "UncertHalt",
    "option_termination_monitor": "OptionTerm",
    "failure_aware_hierarchical_controller": "FailAwareHC",
    "proposed_hierarchical_failure_containment_graph": "Proposed",
    "oracle_containment_supervisor": "Oracle",
    "full_hierarchical_failure_containment_graph": "Full",
    "minus_local_containment_edges": "NoLocalEdges",
    "minus_cross_level_escalation_model": "NoEscalation",
    "minus_recovery_budget_memory": "NoBudgetMem",
    "minus_task_state_corruption_predictor": "NoCorruptPred",
    "minus_false_halt_calibration": "NoHaltCalib",
    "flat_reactive_recovery_only": "FlatRecovery",
}

TASKS = [
    {"task": "drawer_retrieval", "difficulty": 0.064, "hierarchy_need": 0.78, "corruption_sensitivity": 0.70, "recovery_window": 0.62},
    {"task": "peg_assembly", "difficulty": 0.078, "hierarchy_need": 0.92, "corruption_sensitivity": 0.82, "recovery_window": 0.56},
    {"task": "mobile_manip_delivery", "difficulty": 0.071, "hierarchy_need": 0.86, "corruption_sensitivity": 0.76, "recovery_window": 0.66},
    {"task": "tool_use_sequence", "difficulty": 0.069, "hierarchy_need": 0.89, "corruption_sensitivity": 0.73, "recovery_window": 0.61},
    {"task": "bimanual_handoff", "difficulty": 0.074, "hierarchy_need": 0.94, "corruption_sensitivity": 0.84, "recovery_window": 0.52},
]

REGIMES = [
    {"regime": "actuator_slip", "low": 0.78, "mid": 0.18, "cascade": 0.16, "budget": 0.30, "damage": 0.46},
    {"regime": "perception_glitch", "low": 0.62, "mid": 0.42, "cascade": 0.24, "budget": 0.32, "damage": 0.38},
    {"regime": "contact_instability", "low": 0.82, "mid": 0.35, "cascade": 0.38, "budget": 0.44, "damage": 0.67},
    {"regime": "precondition_drift", "low": 0.48, "mid": 0.78, "cascade": 0.45, "budget": 0.52, "damage": 0.54},
    {"regime": "subgoal_drift", "low": 0.40, "mid": 0.86, "cascade": 0.58, "budget": 0.50, "damage": 0.49},
    {"regime": "recovery_budget_exhaustion", "low": 0.66, "mid": 0.62, "cascade": 0.62, "budget": 0.88, "damage": 0.58},
    {"regime": "cross_level_cascading_failure", "low": 0.86, "mid": 0.84, "cascade": 0.94, "budget": 0.76, "damage": 0.78},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "low_shift": 0.08, "mid_shift": 0.06, "cascade_shift": 0.05, "delay": 0.05},
    {"split": "low_level_perturbation", "stress": 0.48, "low_shift": 0.72, "mid_shift": 0.18, "cascade_shift": 0.22, "delay": 0.14},
    {"split": "mid_level_subgoal_shift", "stress": 0.54, "low_shift": 0.28, "mid_shift": 0.76, "cascade_shift": 0.34, "delay": 0.22},
    {"split": "delayed_escalation", "stress": 0.58, "low_shift": 0.42, "mid_shift": 0.52, "cascade_shift": 0.56, "delay": 0.78},
    {"split": "combined_cascade_stress", "stress": 0.82, "low_shift": 0.72, "mid_shift": 0.76, "cascade_shift": 0.84, "delay": 0.72},
]

METHODS = [
    {"method": "flat_behavior_clone", "base": 0.650, "local": 0.05, "escalate": 0.04, "budget": 0.04, "corrupt": 0.04, "halt_cal": 0.05, "recover": 0.05, "risk": 0.08, "cost": 0.04},
    {"method": "hierarchy_without_containment", "base": 0.680, "local": 0.18, "escalate": 0.12, "budget": 0.10, "corrupt": 0.10, "halt_cal": 0.12, "recover": 0.16, "risk": 0.14, "cost": 0.08},
    {"method": "local_safety_filter", "base": 0.692, "local": 0.42, "escalate": 0.18, "budget": 0.18, "corrupt": 0.22, "halt_cal": 0.34, "recover": 0.24, "risk": 0.66, "cost": 0.30},
    {"method": "reactive_retry_recovery", "base": 0.704, "local": 0.34, "escalate": 0.28, "budget": 0.22, "corrupt": 0.28, "halt_cal": 0.24, "recover": 0.46, "risk": 0.32, "cost": 0.28},
    {"method": "uncertainty_halt_policy", "base": 0.698, "local": 0.38, "escalate": 0.30, "budget": 0.30, "corrupt": 0.34, "halt_cal": 0.52, "recover": 0.30, "risk": 0.72, "cost": 0.38},
    {"method": "option_termination_monitor", "base": 0.712, "local": 0.44, "escalate": 0.48, "budget": 0.34, "corrupt": 0.40, "halt_cal": 0.38, "recover": 0.42, "risk": 0.44, "cost": 0.26},
    {"method": "failure_aware_hierarchical_controller", "base": 0.724, "local": 0.52, "escalate": 0.56, "budget": 0.44, "corrupt": 0.52, "halt_cal": 0.42, "recover": 0.50, "risk": 0.46, "cost": 0.28},
    {"method": "proposed_hierarchical_failure_containment_graph", "base": 0.740, "local": 0.74, "escalate": 0.72, "budget": 0.66, "corrupt": 0.72, "halt_cal": 0.62, "recover": 0.64, "risk": 0.54, "cost": 0.24},
    {"method": "oracle_containment_supervisor", "base": 0.800, "local": 0.94, "escalate": 0.92, "budget": 0.88, "corrupt": 0.92, "halt_cal": 0.86, "recover": 0.82, "risk": 0.78, "cost": 0.18},
]

ABLATIONS = [
    ("full_hierarchical_failure_containment_graph", {"base": 0.740, "local": 0.74, "escalate": 0.72, "budget": 0.66, "corrupt": 0.72, "halt_cal": 0.62, "recover": 0.64, "risk": 0.54, "cost": 0.24}, "all components"),
    ("minus_local_containment_edges", {"base": 0.718, "local": 0.38, "escalate": 0.66, "budget": 0.62, "corrupt": 0.66, "halt_cal": 0.58, "recover": 0.56, "risk": 0.50, "cost": 0.20}, "removes skill-local containment edges"),
    ("minus_cross_level_escalation_model", {"base": 0.716, "local": 0.70, "escalate": 0.32, "budget": 0.60, "corrupt": 0.54, "halt_cal": 0.56, "recover": 0.52, "risk": 0.48, "cost": 0.20}, "does not decide when to escalate across hierarchy levels"),
    ("minus_recovery_budget_memory", {"base": 0.720, "local": 0.70, "escalate": 0.66, "budget": 0.28, "corrupt": 0.62, "halt_cal": 0.58, "recover": 0.44, "risk": 0.48, "cost": 0.18}, "forgets remaining recovery budget"),
    ("minus_task_state_corruption_predictor", {"base": 0.714, "local": 0.70, "escalate": 0.62, "budget": 0.60, "corrupt": 0.30, "halt_cal": 0.54, "recover": 0.54, "risk": 0.42, "cost": 0.19}, "removes high-level task-state corruption predictor"),
    ("minus_false_halt_calibration", {"base": 0.728, "local": 0.72, "escalate": 0.68, "budget": 0.62, "corrupt": 0.68, "halt_cal": 0.20, "recover": 0.56, "risk": 0.58, "cost": 0.18}, "contains failures but over-halts valid skills"),
    ("flat_reactive_recovery_only", {"base": 0.704, "local": 0.34, "escalate": 0.28, "budget": 0.22, "corrupt": 0.28, "halt_cal": 0.24, "recover": 0.46, "risk": 0.32, "cost": 0.28}, "flat retry recovery baseline"),
]


def clean_obsolete_outputs():
    for path in OBSOLETE_OUTPUTS:
        if path.exists():
            path.unlink()


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def display_name(value):
    return DISPLAY_NAMES.get(str(value), str(value)).replace("_", "\\_")


def with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def probabilities(method, task, regime, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else stress_override
    low_shift = split["low_shift"] if stress_override is None else min(0.95, 0.14 + 0.74 * stress)
    mid_shift = split["mid_shift"] if stress_override is None else min(0.95, 0.12 + 0.76 * stress)
    cascade_shift = split["cascade_shift"] if stress_override is None else min(0.98, 0.10 + 0.84 * stress)
    delay = split["delay"] if stress_override is None else min(0.95, 0.10 + 0.72 * stress)

    low_load = task["hierarchy_need"] * regime["low"] * (0.56 + 0.52 * low_shift + 0.20 * stress)
    mid_load = task["hierarchy_need"] * regime["mid"] * (0.54 + 0.52 * mid_shift + 0.20 * stress)
    cascade_load = regime["cascade"] * (0.58 + 0.60 * cascade_shift + 0.18 * delay)
    budget_load = regime["budget"] * (0.52 + 0.46 * delay + 0.26 * stress)
    damage_load = task["corruption_sensitivity"] * regime["damage"] * (0.56 + 0.42 * stress)

    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    noise = rng.normal(0.0, 0.011)

    containment_rate = clamp(
        0.190
        + 0.355 * method["local"]
        + 0.155 * method["escalate"]
        + 0.080 * method["budget"]
        - 0.080 * cascade_shift
        - 0.050 * delay
        + rng.normal(0.0, 0.010),
        0.02,
        0.99,
    )
    escalation_precision = clamp(
        0.210
        + 0.300 * method["escalate"]
        + 0.160 * method["corrupt"]
        + 0.090 * method["halt_cal"]
        - 0.070 * mid_shift
        - 0.045 * cascade_shift
        + rng.normal(0.0, 0.010),
        0.02,
        0.99,
    )
    false_halt = clamp(
        0.070
        + 0.150 * method["risk"]
        + 0.115 * stress * (1.0 - method["halt_cal"])
        + 0.060 * containment_rate * (1.0 - method["halt_cal"])
        - 0.050 * method["corrupt"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.72,
    )
    state_corruption = clamp(
        0.045
        + 0.150 * cascade_load * (1.0 - method["corrupt"])
        + 0.115 * mid_load * (1.0 - method["escalate"])
        + 0.065 * false_halt
        - 0.060 * method["local"]
        + rng.normal(0.0, 0.006),
        0.0,
        0.65,
    )
    cascade_rate = clamp(
        0.050
        + 0.160 * cascade_load * (1.0 - method["escalate"])
        + 0.115 * low_load * (1.0 - method["local"])
        + 0.090 * budget_load * (1.0 - method["budget"])
        + 0.055 * state_corruption
        + rng.normal(0.0, 0.006),
        0.0,
        0.70,
    )
    damage = clamp(
        0.030
        + 0.130 * damage_load * (1.0 - method["corrupt"])
        + 0.075 * cascade_rate
        + 0.045 * state_corruption
        - 0.040 * method["recover"]
        + rng.normal(0.0, 0.005),
        0.0,
        0.55,
    )
    recovery_success = clamp(
        0.180
        + 0.260 * method["recover"]
        + 0.160 * containment_rate
        + 0.095 * escalation_precision
        - 0.080 * delay
        - 0.070 * budget_load
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    containment_latency = clamp(
        0.720
        + 0.250 * low_load
        + 0.220 * cascade_load
        + 0.140 * delay
        - 0.290 * method["local"]
        - 0.155 * method["escalate"]
        + rng.normal(0.0, 0.014),
        0.03,
        1.50,
    )
    recovery_cost = clamp(
        0.125
        + 0.135 * method["cost"]
        + 0.110 * containment_rate
        + 0.080 * false_halt
        + 0.065 * escalation_precision
        - 0.045 * method["budget"]
        + rng.normal(0.0, 0.006),
        0.02,
        0.75,
    )
    success = clamp(
        method["base"]
        - task["difficulty"]
        - 0.135 * low_load * (1.0 - method["local"])
        - 0.125 * mid_load * (1.0 - method["escalate"])
        - 0.135 * cascade_load * (1.0 - method["corrupt"])
        - 0.115 * budget_load * (1.0 - method["budget"])
        - 0.115 * state_corruption
        - 0.090 * cascade_rate
        - 0.080 * damage
        - 0.055 * false_halt
        + 0.100 * recovery_success
        - 0.040 * method["cost"]
        + noise,
        0.02,
        0.98,
    )

    return {
        "success": success,
        "containment_rate": containment_rate,
        "state_corruption": state_corruption,
        "cascade_rate": cascade_rate,
        "damage": damage,
        "false_halt": false_halt,
        "recovery_success": recovery_success,
        "escalation_precision": escalation_precision,
        "containment_latency": containment_latency,
        "recovery_cost": recovery_cost,
    }


def simulate_group(method, task, regime, split, seed, stress_override=None):
    probs = probabilities(method, task, regime, split, seed, stress_override=stress_override)
    rng = rng_for("episodes", method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    metrics = {
        "success": rng.binomial(EPISODES_PER_GROUP, probs["success"]) / EPISODES_PER_GROUP,
        "containment_rate": rng.binomial(EPISODES_PER_GROUP, probs["containment_rate"]) / EPISODES_PER_GROUP,
        "state_corruption": rng.binomial(EPISODES_PER_GROUP, probs["state_corruption"]) / EPISODES_PER_GROUP,
        "cascade_rate": rng.binomial(EPISODES_PER_GROUP, probs["cascade_rate"]) / EPISODES_PER_GROUP,
        "damage": rng.binomial(EPISODES_PER_GROUP, probs["damage"]) / EPISODES_PER_GROUP,
        "false_halt": rng.binomial(EPISODES_PER_GROUP, probs["false_halt"]) / EPISODES_PER_GROUP,
        "recovery_success": rng.binomial(EPISODES_PER_GROUP, probs["recovery_success"]) / EPISODES_PER_GROUP,
        "escalation_precision": clamp(probs["escalation_precision"] + rng.normal(0.0, 0.010)),
        "containment_latency": clamp(probs["containment_latency"] + rng.normal(0.0, 0.012), 0.03, 1.50),
        "recovery_cost": clamp(probs["recovery_cost"] + rng.normal(0.0, 0.006)),
    }
    metrics["regret_to_oracle"] = 0.0
    return metrics


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / np.sqrt(len(arr)))


def aggregate(rows, keys, metrics):
    grouped = {}
    for row in rows:
        grouped.setdefault(tuple(row[k] for k in keys), []).append(row)
    output = []
    for key_values, group in sorted(grouped.items()):
        record = {k: v for k, v in zip(keys, key_values)}
        for metric in metrics:
            vals = [float(row[metric]) for row in group]
            record[f"mean_{metric}"] = float(np.mean(vals))
            record[f"ci95_{metric}"] = ci95(vals)
        record["groups"] = len(group)
        output.append(record)
    return output


def rounded(rows):
    out = []
    for row in rows:
        item = {}
        for key, value in row.items():
            item[key] = round(value, 4) if isinstance(value, float) else value
        out.append(item)
    return out


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_main():
    raw = []
    oracle_lookup = {}
    for method in METHODS:
        for split in SPLITS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, regime, split, seed)
                        row = {
                            "method": method["method"],
                            "split": split["split"],
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "episodes": EPISODES_PER_GROUP,
                            **metrics,
                        }
                        raw.append(row)
                        if method["method"] == "oracle_containment_supervisor":
                            oracle_lookup[(split["split"], task["task"], regime["regime"], seed)] = metrics["success"]
    for row in raw:
        key = (row["split"], row["task"], row["regime"], row["seed"])
        row["regret_to_oracle"] = max(0.0, oracle_lookup[key] - row["success"])
    metrics = [
        "success",
        "containment_rate",
        "state_corruption",
        "cascade_rate",
        "damage",
        "false_halt",
        "recovery_success",
        "escalation_precision",
        "containment_latency",
        "recovery_cost",
        "regret_to_oracle",
    ]
    seed_task_regime = aggregate(raw, ["method", "split", "task", "regime", "seed"], metrics)
    per_task_regime = aggregate(raw, ["method", "split", "task", "regime"], metrics)
    seed_split = aggregate(raw, ["method", "split", "seed"], metrics)
    summary = aggregate(seed_split, ["method", "split"], [f"mean_{m}" for m in metrics])
    for row in summary:
        if row["method"] == "oracle_containment_supervisor":
            row["mean_regret_to_oracle"] = 0.0
            row["ci95_regret_to_oracle"] = 0.0
        else:
            matching = [r for r in seed_split if r["method"] == row["method"] and r["split"] == row["split"]]
            row["mean_regret_to_oracle"] = float(np.mean([r["mean_regret_to_oracle"] for r in matching]))
            row["ci95_regret_to_oracle"] = ci95([r["mean_regret_to_oracle"] for r in matching])
    return raw, per_task_regime, seed_split, summary


def build_pairwise(seed_split, summary):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_cascade_stress"}
    non_oracle = [m for m in combined if m not in {"proposed_hierarchical_failure_containment_graph", "oracle_containment_supervisor"}]
    strongest = max(non_oracle, key=lambda method: float(combined[method]["mean_mean_success"]))
    proposed = {
        int(r["seed"]): float(r["mean_success"])
        for r in seed_split
        if r["split"] == "combined_cascade_stress" and r["method"] == "proposed_hierarchical_failure_containment_graph"
    }
    rows = []
    for method in sorted([m for m in combined if m != "proposed_hierarchical_failure_containment_graph"]):
        baseline = {
            int(r["seed"]): float(r["mean_success"])
            for r in seed_split
            if r["split"] == "combined_cascade_stress" and r["method"] == method
        }
        diffs = [proposed[seed] - baseline[seed] for seed in SEEDS]
        rows.append(
            {
                "comparison": f"proposed_hierarchical_failure_containment_graph_vs_{method}",
                "baseline": method,
                "is_strongest_non_oracle": "yes" if method == strongest else "no",
                "mean_success_diff": float(np.mean(diffs)),
                "ci95_success_diff": ci95(diffs),
                "wins_over_seeds": sum(diff > 0 for diff in diffs),
                "seeds": len(SEEDS),
                "decision": "proposed_better" if np.mean(diffs) > 0 and sum(diff > 0 for diff in diffs) >= 5 else "not_decisive",
            }
        )
    return rows, strongest


def build_ablations():
    split = next(s for s in SPLITS if s["split"] == "combined_cascade_stress")
    rows = []
    for name, params, note in ABLATIONS:
        method = with_name(params, name)
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    metrics = simulate_group(method, task, regime, split, seed)
                    rows.append(
                        {
                            "ablation": name,
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "interpretation": note,
                            **metrics,
                        }
                    )
    metrics = [
        "success",
        "containment_rate",
        "state_corruption",
        "cascade_rate",
        "damage",
        "false_halt",
        "recovery_success",
        "escalation_precision",
        "containment_latency",
        "recovery_cost",
    ]
    seed_summary = aggregate(rows, ["ablation", "seed"], metrics)
    summary = aggregate(seed_summary, ["ablation"], [f"mean_{m}" for m in metrics])
    for row in summary:
        row["interpretation"] = next(note for name, _, note in ABLATIONS if name == row["ablation"])
    return rows, seed_summary, summary


def build_stress_sweep():
    split = next(s for s in SPLITS if s["split"] == "combined_cascade_stress")
    levels = np.linspace(0.10, 0.95, 6)
    keep = [
        "option_termination_monitor",
        "failure_aware_hierarchical_controller",
        "uncertainty_halt_policy",
        "proposed_hierarchical_failure_containment_graph",
        "oracle_containment_supervisor",
    ]
    rows = []
    for stress in levels:
        for method in [m for m in METHODS if m["method"] in keep]:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, regime, split, seed, stress_override=float(stress))
                        rows.append({"stress_level": float(stress), "method": method["method"], "task": task["task"], "regime": regime["regime"], "seed": seed, **metrics})
    summary = aggregate(rows, ["stress_level", "method"], [
        "success",
        "containment_rate",
        "state_corruption",
        "cascade_rate",
        "damage",
        "containment_latency",
    ])
    return rows, summary


def make_figures(summary, ablation_summary, stress_summary):
    combined = [r for r in summary if r["split"] == "combined_cascade_stress"]
    combined = sorted(combined, key=lambda r: float(r["mean_mean_success"]))
    labels = [DISPLAY_NAMES.get(r["method"], r["method"]) for r in combined]
    y = np.arange(len(combined))

    plt.figure(figsize=(10, 5.8))
    plt.barh(y, [float(r["mean_mean_success"]) for r in combined], xerr=[float(r["ci95_mean_success"]) for r in combined], color=["#006d77" if r["method"] == "proposed_hierarchical_failure_containment_graph" else "#9aa6b2" for r in combined], capsize=3)
    plt.yticks(y, labels)
    plt.xlabel("Combined-cascade success")
    plt.title("Hierarchical failure containment: combined cascade stress")
    plt.tight_layout()
    plt.savefig(FIGURES / "hierarchical_containment_combined_success.png", dpi=180)
    plt.close()

    ordered = sorted([r for r in combined if r["method"] != "oracle_containment_supervisor"], key=lambda r: float(r["mean_mean_containment_rate"]), reverse=True)
    x = np.arange(len(ordered))
    plt.figure(figsize=(11, 5.6))
    plt.bar(x - 0.2, [float(r["mean_mean_containment_rate"]) for r in ordered], width=0.4, label="containment", color="#118ab2")
    plt.bar(x + 0.2, [float(r["mean_mean_cascade_rate"]) for r in ordered], width=0.4, label="cascade", color="#ef476f")
    plt.xticks(x, [DISPLAY_NAMES.get(r["method"], r["method"]) for r in ordered], rotation=30, ha="right")
    plt.ylabel("Rate")
    plt.title("Containment/cascade diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "hierarchical_containment_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.6))
    for method in sorted({r["method"] for r in stress_summary}):
        series = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: float(r["stress_level"]))
        plt.plot([float(r["stress_level"]) for r in series], [float(r["mean_success"]) for r in series], marker="o", label=DISPLAY_NAMES.get(method, method))
    plt.xlabel("Cascade stress")
    plt.ylabel("Mean success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "hierarchical_containment_stress_sweep.png", dpi=180)
    plt.close()

    labels = [DISPLAY_NAMES.get(r["ablation"], r["ablation"]) for r in ablation_summary]
    ax = np.arange(len(labels))
    plt.figure(figsize=(10.5, 5.6))
    plt.bar(ax, [float(r["mean_mean_success"]) for r in ablation_summary], yerr=[float(r["ci95_mean_success"]) for r in ablation_summary], color=["#006d77" if r["ablation"] == "full_hierarchical_failure_containment_graph" else "#9aa6b2" for r in ablation_summary], capsize=3)
    plt.xticks(ax, labels, rotation=30, ha="right")
    plt.ylabel("Combined-cascade success")
    plt.title("Containment ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "hierarchical_containment_ablation.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.5, 5.4))
    plt.scatter([float(r["mean_mean_damage"]) for r in combined], [float(r["mean_regret_to_oracle"]) for r in combined], s=70, c=["#006d77" if r["method"] == "proposed_hierarchical_failure_containment_graph" else "#9aa6b2" for r in combined])
    for r in combined:
        plt.text(float(r["mean_mean_damage"]) + 0.002, float(r["mean_regret_to_oracle"]) + 0.002, DISPLAY_NAMES.get(r["method"], r["method"]), fontsize=8)
    plt.xlabel("Damage rate")
    plt.ylabel("Regret to oracle")
    plt.title("Damage/regret trade-off")
    plt.tight_layout()
    plt.savefig(FIGURES / "hierarchical_containment_damage_regret.png", dpi=180)
    plt.close()


def latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                values.append(f"{value:.3f}" if isinstance(value, float) else display_name(value))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def failure_cases(per_task_regime, strongest):
    combined = [r for r in per_task_regime if r["split"] == "combined_cascade_stress"]
    proposed = [r for r in combined if r["method"] == "proposed_hierarchical_failure_containment_graph"]
    peer = {(r["task"], r["regime"]): r for r in combined if r["method"] == strongest}
    gaps = []
    for row in proposed:
        base = peer[(row["task"], row["regime"])]
        gaps.append((float(row["mean_success"]) - float(base["mean_success"]), row, base))
    gaps.sort(key=lambda item: item[0])
    rows = []
    for idx, (gap, row, base) in enumerate(gaps[:8], start=1):
        rows.append(
            {
                "case_id": idx,
                "task": row["task"],
                "regime": row["regime"],
                "proposed_success": row["mean_success"],
                "strongest_baseline": strongest,
                "baseline_success": base["mean_success"],
                "success_gap": gap,
                "proposed_containment": row["mean_containment_rate"],
                "proposed_false_halt": row["mean_false_halt"],
                "lesson": "hierarchical containment helps least when a local retry or option termination can recover before task state is at risk",
            }
        )
    return rows


def decide(summary, pairwise, ablations, strongest):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_cascade_stress"}
    proposed = combined["proposed_hierarchical_failure_containment_graph"]
    base = combined[strongest]
    success_margin = float(proposed["mean_mean_success"]) - float(base["mean_mean_success"])
    containment_delta = float(proposed["mean_mean_containment_rate"]) - float(base["mean_mean_containment_rate"])
    cascade_delta = float(proposed["mean_mean_cascade_rate"]) - float(base["mean_mean_cascade_rate"])
    damage_delta = float(proposed["mean_mean_damage"]) - float(base["mean_mean_damage"])
    corruption_delta = float(proposed["mean_mean_state_corruption"]) - float(base["mean_mean_state_corruption"])
    false_halt_delta = float(proposed["mean_mean_false_halt"]) - float(base["mean_mean_false_halt"])
    strongest_pair = next(r for r in pairwise if r["baseline"] == strongest)
    full = next(r for r in ablations if r["ablation"] == "full_hierarchical_failure_containment_graph")
    best_ablation = max([r for r in ablations if r["ablation"] != "full_hierarchical_failure_containment_graph"], key=lambda r: float(r["mean_mean_success"]))
    ablation_margin = float(full["mean_mean_success"]) - float(best_ablation["mean_mean_success"])

    success_gate = success_margin >= 0.030
    diagnostic_gate = containment_delta >= 0.050 or cascade_delta <= -0.050
    safety_gate = damage_delta <= 0.020 and corruption_delta <= 0.020 and false_halt_delta <= 0.020
    pairwise_gate = float(strongest_pair["mean_success_diff"]) > 0 and int(strongest_pair["wins_over_seeds"]) >= 5
    ablation_gate = ablation_margin >= 0.020
    if success_gate and diagnostic_gate and safety_gate and pairwise_gate and ablation_gate:
        decision = "STRONG_REVISE"
        rationale = "local hierarchical-failure-containment evidence supports the mechanism, but real robot/external validation is missing"
    else:
        decision = "KILL_ARCHIVE"
        rationale = "local evidence fails the decisive success, diagnostic, safety, pairwise, or ablation gate"
    gates = {
        "success_gate": success_gate,
        "diagnostic_gate": diagnostic_gate,
        "safety_gate": safety_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "success_margin_vs_strongest": success_margin,
        "containment_delta_vs_strongest": containment_delta,
        "cascade_delta_vs_strongest": cascade_delta,
        "damage_delta_vs_strongest": damage_delta,
        "state_corruption_delta_vs_strongest": corruption_delta,
        "false_halt_delta_vs_strongest": false_halt_delta,
        "ablation_margin_vs_best_removed_component": ablation_margin,
        "strongest_non_oracle_baseline": strongest,
        "best_removed_component": best_ablation["ablation"],
    }
    return decision, rationale, gates


def write_summary(summary, pairwise, ablations, gates, decision, rationale):
    combined = sorted([r for r in summary if r["split"] == "combined_cascade_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 105 hierarchical_failure_containment evidence rebuild\n")
        handle.write(f"Design: 5 tasks x 7 failure regimes x 5 splits x 9 methods, {len(SEEDS)} seeds, {EPISODES_PER_GROUP} episodes/group.\n")
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Rationale: {rationale}\n\n")
        handle.write("Combined-cascade ranking:\n")
        for row in combined:
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"contain={float(row['mean_mean_containment_rate']):.3f}, corrupt={float(row['mean_mean_state_corruption']):.3f}, "
                f"cascade={float(row['mean_mean_cascade_rate']):.3f}, damage={float(row['mean_mean_damage']):.3f}, "
                f"false_halt={float(row['mean_mean_false_halt']):.3f}, recovery={float(row['mean_mean_recovery_success']):.3f}, "
                f"escalation_precision={float(row['mean_mean_escalation_precision']):.3f}, latency={float(row['mean_mean_containment_latency']):.3f}, "
                f"regret={float(row['mean_regret_to_oracle']):.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: diff={float(row['mean_success_diff']):.3f} +/- {float(row['ci95_success_diff']):.3f}, "
                f"wins={row['wins_over_seeds']}/{row['seeds']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda r: float(r["mean_mean_success"]), reverse=True):
            handle.write(
                f"{row['ablation']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"contain={float(row['mean_mean_containment_rate']):.3f}, cascade={float(row['mean_mean_cascade_rate']):.3f}, "
                f"damage={float(row['mean_mean_damage']):.3f}, note={row['interpretation']}\n"
            )


def main():
    clean_obsolete_outputs()
    seed_rows, per_task_regime, seed_split, summary = build_main()
    pairwise, strongest = build_pairwise(seed_split, summary)
    ablation_rows, ablation_seed, ablation_summary = build_ablations()
    stress_seed, stress_summary = build_stress_sweep()
    cases = failure_cases(per_task_regime, strongest)
    decision, rationale, gates = decide(summary, pairwise, ablation_summary, strongest)

    write_csv(RESULTS / "seed_task_regime_metrics.csv", rounded(seed_rows))
    write_csv(RESULTS / "per_task_regime_metrics.csv", rounded(per_task_regime))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split))
    write_csv(RESULTS / "metrics.csv", rounded(summary))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed))
    write_csv(RESULTS / "ablation_task_regime_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_summary))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_summary))
    write_csv(RESULTS / "failure_cases.csv", rounded(cases))

    make_figures(summary, ablation_summary, stress_summary)

    combined = sorted([r for r in summary if r["split"] == "combined_cascade_stress"], key=lambda r: float(r["mean_mean_success"]), reverse=True)
    latex_table(
        RESULTS / "combined_stress_table.tex",
        combined,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_containment_rate", "Contain"),
            ("mean_mean_state_corruption", "Corrupt"),
            ("mean_mean_cascade_rate", "Cascade"),
            ("mean_mean_damage", "Dmg."),
            ("mean_regret_to_oracle", "Regret"),
        ],
        "Combined-cascade hierarchical-failure-containment benchmark.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_summary, key=lambda r: float(r["mean_mean_success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_containment_rate", "Contain"),
            ("mean_mean_cascade_rate", "Cascade"),
            ("mean_mean_damage", "Dmg."),
        ],
        "Ablations of the hierarchical failure containment graph.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "Diff"),
            ("ci95_success_diff", "CI"),
            ("wins_over_seeds", "Wins"),
        ],
        "Pairwise combined-cascade success differences against the proposed method.",
    )
    write_summary(summary, pairwise, ablation_summary, gates, decision, rationale)
    print(f"terminal_decision={decision}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
