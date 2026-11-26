"""Demonstra localmente uma falha controlada seguida da suíte correta."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '12_TDD_CICD_MELHORIA' / 'evidencias'
OUT.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONIOENCODING='utf-8')
with tempfile.TemporaryDirectory() as tmp:
    failing = Path(tmp) / 'test_falha_controlada.py'
    failing.write_text('def test_falha_controlada():\n    assert 25 == 100\n', encoding='utf-8')
    bad = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', str(failing)],
                         cwd=ROOT, capture_output=True, text=True, encoding='utf-8', env=env)
    (OUT / 'pipeline_local_falha.txt').write_text(bad.stdout + bad.stderr, encoding='utf-8')
    assert bad.returncode == 1, 'A asserção controlada deve produzir código 1'
good = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                       '05_EXECUCAO_MANUAL/test_reexecucao_catalogo.py', '07_AUTOMACAO_UNITARIA', '08_INTEGRACAO_API', '10_ACEITACAO_NAO_FUNCIONAIS'],
                      cwd=ROOT, capture_output=True, text=True, encoding='utf-8', env=env)
(OUT / 'pipeline_local_sucesso.txt').write_text(good.stdout + good.stderr, encoding='utf-8')
(OUT / 'pipeline_local.json').write_text(json.dumps({'data': datetime.now(timezone(timedelta(hours=-3))).isoformat(),
    'ambiente': 'local; não é uma execução do GitHub Actions', 'falha_exit_code': bad.returncode,
    'sucesso_exit_code': good.returncode}, ensure_ascii=False, indent=2), encoding='utf-8')
assert good.returncode == 0, good.stdout
print(good.stdout)
