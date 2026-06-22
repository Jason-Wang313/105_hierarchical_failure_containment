import csv
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
DOWNLOADS_PDF = Path.home() / "Downloads" / "105.pdf"
DESKTOP_PDF = Path.home() / "Desktop" / "105.pdf"
EXPECTED_PAGES_MIN = 25

EXPECTED_ROWS = {
    "dataset_summary.csv": 3840,
    "rollouts.csv": 345600,
    "main_group_metrics.csv": 57600,
    "main_seed_metrics.csv": 150,
    "metrics.csv": 120,
    "hard_aggregate_seed_metrics.csv": 150,
    "hard_aggregate_metrics.csv": 15,
    "pairwise_stats.csv": 14,
    "ablation_rollouts.csv": 115200,
    "ablation_seed_metrics.csv": 100,
    "ablation_metrics.csv": 10,
    "stress_sweep_raw.csv": 288000,
    "stress_sweep_seed_metrics.csv": 1000,
    "stress_sweep.csv": 100,
    "fixed_risk_raw.csv": 276480,
    "fixed_risk_seed_metrics.csv": 480,
    "fixed_risk_metrics.csv": 48,
    "fixed_risk_pairwise_stats.csv": 44,
    "failure_cases.csv": 24,
    "row_counts.csv": 19,
}


def count_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        next(reader)
        return sum(1 for _ in reader)


def assert_finite_csv(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            for key, value in row.items():
                if value is None or value == "":
                    continue
                try:
                    number = float(value)
                except ValueError:
                    continue
                if not math.isfinite(number):
                    raise AssertionError(f"non-finite value in {path}:{key}: {value}")
                if key == "regret" and number < -1e-12:
                    raise AssertionError(f"negative regret in {path}: {number}")


def pdf_pages(path: Path) -> int:
    output = subprocess.check_output(["pdfinfo", str(path)], text=True)
    for line in output.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise AssertionError("pdfinfo did not report page count")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def assert_summary() -> None:
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    if summary["terminal"] != "STRONG_REVISE":
        raise AssertionError(f"unexpected terminal decision: {summary['terminal']}")
    if summary["iclr_main_ready"] is not False or summary["scope_gate"] is not False:
        raise AssertionError("scope gate must remain false for local-only evidence")
    local_gate_failures = [
        key for key, value in summary["gates"].items()
        if key.endswith("_gate") and key != "scope_gate" and value is not True
    ]
    if local_gate_failures:
        raise AssertionError(f"local gates failed: {local_gate_failures}")
    if int(summary["row_counts"]["main_rollout_rows"]) != 345600:
        raise AssertionError("summary.json row counts are stale")
    if float(summary["v5_metrics"]["regret"]) < 0:
        raise AssertionError("v5 regret must be nonnegative")


def assert_latex() -> None:
    tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    required = [
        "citebordercolor={0 1 0}",
        "linkbordercolor={1 0.55 0}",
        "urlbordercolor={0 0.55 1}",
        "pdfborder={0 0 1.2}",
        r"\usepackage{hyperref}",
        r"\bibliography{references}",
        "Risk-Calibrated Hierarchical Failure Containment",
        "ICLR-main readiness remains",
    ]
    for needle in required:
        if needle not in tex:
            raise AssertionError(f"missing manuscript requirement: {needle}")

    log = (PAPER / "main.log").read_text(encoding="utf-8", errors="replace")
    bad_patterns = [
        r"Citation `[^']+' .* undefined",
        r"There were undefined citations",
        r"Rerun to get citations correct",
        r"Label\(s\) may have changed",
    ]
    for pattern in bad_patterns:
        if re.search(pattern, log):
            raise AssertionError(f"LaTeX log still has unresolved state: {pattern}")


def assert_figures() -> None:
    expected = [
        "hierarchical_v5_hard_success.png",
        "hierarchical_v5_diagnostics.png",
        "hierarchical_v5_safety_regret.png",
        "hierarchical_v5_stress_sweep.png",
        "hierarchical_v5_ablation.png",
        "hierarchical_v5_fixed_risk.png",
    ]
    for name in expected:
        path = ROOT / "figures" / name
        if not path.exists() or path.stat().st_size <= 0:
            raise AssertionError(f"missing or empty figure: {path}")


def main() -> None:
    for name, expected in EXPECTED_ROWS.items():
        path = RESULTS / name
        if not path.exists():
            raise AssertionError(f"missing expected result file: {path}")
        observed = count_rows(path)
        if observed != expected:
            raise AssertionError(f"{name}: expected {expected} rows, observed {observed}")
        assert_finite_csv(path)

    assert_summary()
    assert_latex()
    assert_figures()

    if not DOWNLOADS_PDF.exists():
        raise AssertionError(f"missing canonical PDF: {DOWNLOADS_PDF}")
    if DESKTOP_PDF.exists():
        raise AssertionError(f"Desktop PDF is forbidden: {DESKTOP_PDF}")
    if (ROOT / "105.pdf").exists():
        raise AssertionError("repo-local numbered PDF is forbidden")

    pages = pdf_pages(DOWNLOADS_PDF)
    if pages < EXPECTED_PAGES_MIN:
        raise AssertionError(f"expected at least {EXPECTED_PAGES_MIN} pages, observed {pages}")
    digest = sha256(DOWNLOADS_PDF)
    print(f"validated Paper 105 artifacts: pages={pages}, sha256={digest}")


if __name__ == "__main__":
    main()
