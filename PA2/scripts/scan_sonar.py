# Stack: Python 3 / Docker / SonarQube; AI contribution: 67%; human contribution: 33%.
# Runs a dedicated local evaluation server; never sends code to SonarCloud.
import base64
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import time
import urllib.parse
import urllib.request

root = Path(__file__).resolve().parents[1]
out = root / 'evidence'
out.mkdir(exist_ok=True)
host = 'http://127.0.0.1:9002'
server_image = 'sonarqube@sha256:1ce197471f5f2bac347694a336862fd2c23e9f57c6edb46acebbfbe70f2c7d9c'
scanner_image = os.getenv('PA2_SONAR_SCANNER_IMAGE', 'sonarsource/sonar-scanner-cli@sha256:6e6eca4d552695a98fb7dab84f0c1bd0885ebbfe272654d1552e24bd7f452d51')
project = 'cs763-pa2-artifact-indexer'
auth = 'Basic ' + base64.b64encode(b'admin:admin').decode()

def api(path, data=None):
    request = urllib.request.Request(host + path, data=urllib.parse.urlencode(data).encode() if data is not None else None,
                                     headers={'Authorization': auth})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read()
        return json.loads(raw) if raw else {}

if subprocess.run(['docker', 'inspect', 'cs763-pa2-sonar'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
    if subprocess.run(['docker', 'network', 'inspect', 'cs763-pa2-scanners'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
        subprocess.run(['docker', 'network', 'create', 'cs763-pa2-scanners'], stdout=subprocess.DEVNULL, check=True)
    subprocess.run(['docker', 'run', '-d', '--name', 'cs763-pa2-sonar', '--network', 'cs763-pa2-scanners', '-p', '127.0.0.1:9002:9000', '-e', 'SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true', '--memory=3g', server_image], check=True)
subprocess.run(['docker', 'start', 'cs763-pa2-sonar'], stdout=subprocess.DEVNULL, check=True)
for attempt in range(90):
    try:
        if api('/api/system/status').get('status') == 'UP':
            break
    except Exception:
        pass
    time.sleep(2)
else:
    raise RuntimeError('Local SonarQube did not become ready')
try:
    api('/api/projects/create', {'project': project, 'name': 'CS763 PA2 baseline', 'visibility': 'private'})
except urllib.error.HTTPError as error:
    if error.code != 400:
        raise
# Default credentials belong solely to the new throwaway local evaluation container.
# Token is passed through the child environment, never written into evidence.
name = 'pa2-local-scan-' + str(int(time.time()))
token = api('/api/user_tokens/generate', {'name': name})['token']
try:
    environment = dict(os.environ, SONAR_TOKEN=token)
    command = ['docker', 'run', '--rm', '--network', 'cs763-pa2-scanners', '-e', 'SONAR_TOKEN',
               '-e', 'SONAR_HOST_URL=http://cs763-pa2-sonar:9000',
               '-v', str(root / 'functional-codebase') + ':/usr/src:ro', scanner_image,
               '-Dsonar.projectKey=' + project, '-Dsonar.sources=app', '-Dsonar.tests=tests',
               '-Dsonar.python.version=3.13', '-Dsonar.scm.disabled=true',
               '-Dsonar.working.directory=/tmp/pa2-scanner', '-Dsonar.qualitygate.wait=true']
    if '--export-only' in sys.argv:
        assert 'EXECUTION SUCCESS' in (out / 'sonar-scanner.log').read_text(), 'No successful prior scan'
        result = SimpleNamespace(returncode=0)
    else:
        with (out / 'sonar-scanner.log').open('w') as log:
            result = subprocess.run(command, env=environment, stdout=log, stderr=subprocess.STDOUT)
    issues = api('/api/issues/search?componentKeys=' + project + '&ps=100')
    hotspots = api('/api/hotspots/search?project=' + project + '&ps=100')
    analyses = api('/api/project_analyses/search?project=' + project)
    measures = api('/api/measures/component?component=' + project + '&metricKeys=bugs,vulnerabilities,code_smells,security_hotspots,ncloc')
    for filename, value in [('sonar-issues.json', issues), ('sonar-hotspots.json', hotspots), ('sonar-analyses.json', analyses), ('sonar-measures.json', measures)]:
        (out / filename).write_text(json.dumps(value, indent=2) + '\n')
    status = {'scanner_returncode': result.returncode, 'server': api('/api/system/status'),
              'issue_total': issues['total'], 'hotspot_total': hotspots['paging']['total'],
              'analyses': len(analyses['analyses']), 'server_image': server_image, 'scanner_image': scanner_image}
    (out / 'sonar-run.json').write_text(json.dumps(status, indent=2) + '\n')
    print(json.dumps(status, indent=2))
    if not analyses['analyses']:
        raise RuntimeError('No completed Sonar analysis; inspect scanner log')
    if issues['total'] > 100 or hotspots['paging']['total'] > 100:
        raise RuntimeError('Pagination required; evidence is incomplete')
finally:
    api('/api/user_tokens/revoke', {'name': name})
