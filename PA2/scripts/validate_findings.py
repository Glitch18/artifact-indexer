# Stack: Python 3.13 / HTTPX; AI contribution: 67%; human contribution: 33%.
# Audit-only validation after functional baseline; does not change application source.
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import threading
import time

import httpx

base = os.getenv('PA2_BASE_URL', 'http://127.0.0.1:8002')
report = {'target': base, 'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'checks': []}
payload = {'title': 'Audit fixture', 'description': 'Fictional local record', 'members': [{'id': 'alice', 'role': 'student'}], 'units': [{'type': 'course', 'id': 'CS763'}]}
with httpx.Client(base_url=base, timeout=30) as client:
    created = client.post('/api/v1/projects', json=payload)
    created.raise_for_status()
    pid = created.json()['id']
    prefix = f'/api/v1/projects/{pid}'
    try:
        # A fresh client with no credentials reads and modifies a record assigned to alice.
        with httpx.Client(base_url=base, timeout=30) as anonymous:
            read = anonymous.get(prefix)
            change = anonymous.put(prefix, json={**payload, 'title': 'Changed without credentials'})
            report['checks'].append({'id': 'V1', 'cwe': 'CWE-306', 'authorization_header_sent': False,
                'read_status': read.status_code, 'update_status': change.status_code,
                'stored_title': client.get(prefix).json()['title'], 'members': created.json()['members'],
                'confirmed': read.status_code == change.status_code == 200})
        manuscript = client.post(prefix + '/artifacts/manuscripts/', json={'title': 'Audit upload'}).json()
        path = prefix + f"/artifacts/manuscripts/{manuscript['id']}/file"
        content = b'A' * (4 * 1024 * 1024)
        upload = client.post(path, files={'file': ('fixture.bin', content, 'application/octet-stream')})
        upload.raise_for_status()
        report['checks'].append({'id': 'V2', 'cwe': 'CWE-770', 'bytes_sent': len(content),
            'status': upload.status_code, 'stored_size': upload.json()['file']['size'],
            'hash_matches': upload.json()['file']['sha256'] == hashlib.sha256(content).hexdigest(),
            'scope': 'Bounded 4 MiB acceptance test plus source review; no exhaustion or maximum capacity measured',
            'confirmed': upload.json()['file']['size'] == len(content)})
        start_revision = client.get(prefix).json()['revision']
        workers = 12
        barrier = threading.Barrier(workers)
        def update(number):
            with httpx.Client(base_url=base, timeout=30) as c:
                barrier.wait(timeout=20)
                response = c.put(prefix, json={**payload, 'title': f'Concurrent change {number}'})
                return {'status': response.status_code, 'revision': response.json().get('revision')}
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(update, range(workers)))
        end_revision = client.get(prefix).json()['revision']
        successes = sum(r['status'] == 200 for r in results)
        report['checks'].append({'id': 'V3', 'cwe': 'CWE-362', 'before_revision': start_revision,
            'successful_updates': successes, 'expected_revision': start_revision + successes,
            'actual_revision': end_revision, 'responses': results,
            'confirmed': end_revision < start_revision + successes})
    finally:
        deleted = client.delete(prefix)
        report['fixture_cleanup_status'] = deleted.status_code
output = Path(__file__).resolve().parents[1] / 'evidence' / 'manual-validation.json'
output.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
assert all(c['confirmed'] for c in report['checks']), 'One candidate was not reproduced; investigate rather than claim confirmation'
