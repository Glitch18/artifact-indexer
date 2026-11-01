# AI Contribution Weight: 100% AI Generated / 0% Human Refactored
"""Poll a running Compose API, checking both liveness and real SQL readiness."""

import json
import os
import time
from urllib.error import URLError
from urllib.request import urlopen

base_url = os.getenv("SMOKE_BASE_URL", "http://127.0.0.1:8000")
expected = {
    "/healthz": {"status": "ok", "service": "artifact-indexer", "phase": "week-1"},
    "/readyz": {"status": "ready", "database": "reachable"},
}
for path, payload in expected.items():
    for attempt in range(30):
        try:
            with urlopen(base_url + path, timeout=5) as response:
                actual = json.load(response)
                assert response.status == 200 and actual == payload, (path, actual)
            print(json.dumps({"path": path, "status": 200, "body": actual}), flush=True)
            break
        except (URLError, TimeoutError):
            if attempt == 29:
                raise
            time.sleep(1)

with urlopen(base_url + "/openapi.json", timeout=5) as response:
    schema = json.load(response)
    assert set(schema["paths"]) == {"/healthz", "/readyz"}
print("PASS: container liveness, PostgreSQL readiness, and week-one API boundary")
