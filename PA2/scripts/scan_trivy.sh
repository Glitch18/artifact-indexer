#!/usr/bin/env bash
# Stack: Bash / Docker / Trivy; AI contribution: 67%; human contribution: 33%.
set -euo pipefail
pa2_root="$(cd "$(dirname "$0")/.." && pwd)"
scanner_image='aquasec/trivy@sha256:790fd66d1697395d8693d1acaa1ea702406a20f109b6fc7bac8db623eca6c06c'
archive_path="$pa2_root/evidence/pa2-image.tar"
trap 'rm -f "$archive_path"' EXIT
docker save cs763-artifact-indexer:pa2 -o "$archive_path"
docker run --rm -v "$pa2_root/functional-codebase:/src:ro" -v "$pa2_root/evidence:/out" -v cs763-pa2-trivy-cache:/root/.cache/ \
  "$scanner_image" fs --scanners vuln --format json --output /out/trivy-dependencies.json /src > "$pa2_root/evidence/trivy-dependencies.log" 2>&1
docker run --rm -v "$pa2_root/evidence:/out" -v cs763-pa2-trivy-cache:/root/.cache/ \
  "$scanner_image" image --input /out/pa2-image.tar --scanners vuln --format json --output /out/trivy-image.json > "$pa2_root/evidence/trivy-image.log" 2>&1
