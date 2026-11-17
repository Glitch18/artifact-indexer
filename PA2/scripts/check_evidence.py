# Stack: Python 3; AI contribution: 67%; human contribution: 33%.
import json
from pathlib import Path
import xml.etree.ElementTree as ET
root = Path(__file__).resolve().parents[1]
evidence = root / 'evidence'
for filename in ['pytest-local.xml', 'pytest-postgres.xml']:
    tree = ET.parse(evidence / filename)
    suites = list(tree.getroot().iter('testsuite'))
    assert suites and sum(int(s.get('tests', '0')) for s in suites) >= 11
    assert all(int(s.get('failures', '0')) == int(s.get('errors', '0')) == 0 for s in suites)
semgrep = json.loads((evidence / 'semgrep.json').read_text())
assert not semgrep.get('errors')
sonar = json.loads((evidence / 'sonar-run.json').read_text())
assert sonar['analyses'] > 0
assert sonar['scanner_returncode'] == 0, 'Scanner/quality gate failed; inspect log and report status honestly'
for filename in ['trivy-dependencies.json', 'trivy-image.json']:
    report = json.loads((evidence / filename).read_text())
    assert report.get('SchemaVersion') and 'Results' in report
assert json.loads((evidence / 'source-sha256.json').read_text())
print('Both API suites and both scanner evidence exports are valid. This does not assert security or student review.')
