#!/usr/bin/env bash
# Stack: Bash / Docker / Semgrep; AI contribution: 67%; human contribution: 33%.
set -euo pipefail
pa2_root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$pa2_root/evidence"
docker run --rm -v "$pa2_root/functional-codebase:/src:ro" -v "$pa2_root/evidence:/out" -w /src \
  semgrep/semgrep@sha256:451b3d875c00dac7ed5db5293e584a07de11449a409c10b3c2d2652f429630b6 \
  semgrep scan --config p/python --config p/security-audit --metrics=off --disable-version-check \
  --json --output /out/semgrep.json app tests > "$pa2_root/evidence/semgrep.log" 2>&1
python3 - "$pa2_root/evidence/semgrep.json" <<'PYCODE'
import json, sys
report = json.load(open(sys.argv[1]))
assert not report.get('errors'), report['errors']
print('Semgrep findings:', len(report.get('results', [])))
PYCODE
