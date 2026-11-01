#!/usr/bin/env bash
# AI Contribution Weight: 100% AI Generated / 0% Human Refactored
set -euo pipefail
cd "$(dirname "$0")/.."
kind="${1:?Usage: bash scripts/scan.sh semgrep|trivy [report-directory]}"
reports="${2:-evidence/local}"
mkdir -p "$reports"
reports="$(cd "$reports" && pwd)"
# Immutable multi-platform digests observed from the official image registries.
semgrep_image='semgrep/semgrep@sha256:451b3d875c00dac7ed5db5293e584a07de11449a409c10b3c2d2652f429630b6'
trivy_image='aquasec/trivy@sha256:790fd66d1697395d8693d1acaa1ea702406a20f109b6fc7bac8db623eca6c06c'
case "$kind" in
  semgrep)
    docker run --rm -e SEMGREP_SEND_METRICS=off -e SEMGREP_ENABLE_VERSION_CHECK=0 \
      -v "$PWD:/src:ro" -v "$reports:/reports" -w /src \
      "$semgrep_image" semgrep scan --config p/python --config p/security-audit \
      --metrics off --disable-version-check --strict \
      --json --output /reports/semgrep.json app scripts tests \
      2>&1 | tee "$reports/semgrep.log"
    ;;
  trivy)
    docker run --rm -v "$PWD:/src:ro" -v "$reports:/reports" \
      -v cs763-trivy-cache:/root/.cache/trivy "$trivy_image" fs \
      --scanners vuln --list-all-pkgs --no-progress --exit-code 0 --format json --output /reports/trivy-dependencies.json \
      --skip-dirs /src/.venv --skip-dirs /src/.git --skip-dirs /src/evidence /src \
      2>&1 | tee "$reports/trivy-dependencies.log"
    archive="$reports/image.tar"
    trap 'rm -f "$archive"' EXIT
    docker image save cs763-artifact-indexer:week1 -o "$archive"
    docker run --rm -v "$reports:/reports" -v cs763-trivy-cache:/root/.cache/trivy \
      "$trivy_image" image --input /reports/image.tar --scanners vuln --list-all-pkgs --no-progress \
      --exit-code 0 --format json --output /reports/trivy-image.json \
      2>&1 | tee "$reports/trivy-image.log"
    ;;
  *) echo "Unknown scanner: $kind" >&2; exit 2 ;;
esac
