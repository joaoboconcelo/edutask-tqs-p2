"""Empacota a entrega e verifica hashes sem incluir bancos ou dependências locais."""
import hashlib
import json
import os
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '16_BACKUP_ENTREGA'
ARCHIVE = OUT / 'P2_TQS_2026_TURMAA_GRUPO01_EDUTASK-WEB_BACKUP.zip'
MANIFEST = OUT / 'MANIFESTO_SHA256.json'
SKIP = {'.git', '.pytest_cache', '__pycache__', '.deps', 'node_modules', 'tmp', '.venv', 'venv'}


def files():
    for parent, folders, names in os.walk(ROOT, followlinks=False):
        folders[:] = [n for n in folders if n not in SKIP and not Path(parent, n).is_symlink()]
        for name in names:
            path = Path(parent, name)
            if path in (ARCHIVE, MANIFEST) or name.startswith('.coverage') or path.suffix in {'.db', '.pyc'}:
                continue
            if path.suffix == '.zip' or path.name.endswith('.inspect.ndjson'):
                continue
            yield path


paths = sorted(files())
hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
MANIFEST.write_text(json.dumps({'algoritmo': 'SHA-256', 'escopo': 'Entrega sem este manifesto, ZIP, banco local, dependências e temporários',
                               'arquivos': hashes}, ensure_ascii=False, indent=2), encoding='utf-8')
with ZipFile(ARCHIVE, 'w', ZIP_DEFLATED) as archive:
    for path in paths + [MANIFEST]:
        archive.write(path, path.relative_to(ROOT).as_posix())
with ZipFile(ARCHIVE) as archive:
    assert archive.testzip() is None
    for name, expected in hashes.items():
        assert hashlib.sha256(archive.read(name)).hexdigest() == expected, name
print(f'ZIP íntegro: {len(paths)+1} arquivos; {ARCHIVE.stat().st_size:,} bytes')
