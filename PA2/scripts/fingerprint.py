# Stack: Python 3; AI contribution: 67%; human contribution: 33%.
import hashlib
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
base = root / 'functional-codebase'
files = [p for p in base.rglob('*') if p.is_file() and not any(part in {'.venv', '__pycache__', '.pytest_cache', 'data'} for part in p.relative_to(base).parts) and p.suffix != '.db']
manifest = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
(root / 'evidence/source-sha256.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(f'Fingerprint recorded for {len(manifest)} baseline files')
