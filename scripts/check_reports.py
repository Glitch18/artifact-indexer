# AI Contribution Weight: 100% AI Generated / 0% Human Refactored
"""Reject absent/broken scan evidence; findings themselves are non-blocking."""

import json
import sys
from collections import Counter
from pathlib import Path

reports = Path(sys.argv[1] if len(sys.argv) > 1 else "evidence/local")
semgrep = json.loads((reports / "semgrep.json").read_text())
if semgrep.get("errors") or not semgrep.get("paths", {}).get("scanned"):
    raise SystemExit("Semgrep failed or scanned no source files")
summary = {
    "semgrep": {
        "version": semgrep["version"],
        "scanned_files": len(semgrep["paths"]["scanned"]),
        "findings": len(semgrep["results"]),
    }
}
for name in ("trivy-dependencies", "trivy-image"):
    result = json.loads((reports / f"{name}.json").read_text())
    if result.get("SchemaVersion") != 2 or not result.get("Results"):
        raise SystemExit(f"{name}: missing valid scan results")
    if name == "trivy-dependencies" and not any(
        item.get("Type") in {"pip", "uv"} and item.get("Packages") for item in result["Results"]
    ):
        raise SystemExit("Trivy did not inventory Python dependencies")
    counts = Counter(
        finding["Severity"]
        for item in result["Results"]
        for finding in item.get("Vulnerabilities", [])
    )
    summary[name] = {"findings_by_severity": dict(counts), "targets": len(result["Results"])}
(reports / "scan-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
