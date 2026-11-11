"""Medições HTTP reais, com dados brutos e ambiente identificável."""
import csv
import hashlib
import json
import logging
import platform
import statistics
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from werkzeug.serving import make_server

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '01_SISTEMA_ALVO'))
from edutask.app import create_app


def main():
    output = ROOT / '11_METRICAS_E_QUALIDADE' / 'evidencias'
    output.mkdir(exist_ok=True)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    with tempfile.TemporaryDirectory() as folder:
        app = create_app({'TESTING': True, 'SECRET_KEY': 'measurement-only', 'DATABASE': str(Path(folder) / 'measure.db')})
        server = make_server('127.0.0.1', 0, app)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f'http://127.0.0.1:{server.server_port}'
        rows = []
        try:
            with requests.Session() as client:
                client.post(base + '/api/auth/login', json={'email': 'aluno@unisagrado.edu.br', 'password': 'Senha@123'}, timeout=10).raise_for_status()
                for route in ['/tarefas', '/api/tarefas', '/api/metricas']:
                    for _ in range(3):
                        client.get(base + route, timeout=10).raise_for_status()
                    for repetition in range(1, 31):
                        start = time.perf_counter_ns()
                        response = client.get(base + route, timeout=10)
                        elapsed = (time.perf_counter_ns() - start) / 1e6
                        response.raise_for_status()
                        rows.append({'rota': route, 'repeticao': repetition, 'status_http': response.status_code,
                                     'tempo_ms': round(elapsed, 4), 'bytes_resposta': len(response.content)})
        finally:
            server.shutdown()
            thread.join(5)
    with (output / 'latencias_http.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    summary = {'data': datetime.now(timezone(timedelta(hours=-3))).isoformat(),
               'python': platform.python_version(), 'sistema': platform.platform(),
               'metodo': 'HTTP loopback real com requests, Flask/Werkzeug, SQLite temporário, 3 aquecimentos e 30 amostras por rota, 1 cliente sequencial',
               'carga': '1 usuário, 2 disciplinas e 3 tarefas; sem teste de concorrência', 'rotas': {}}
    for route in sorted({r['rota'] for r in rows}):
        values = [r['tempo_ms'] for r in rows if r['rota'] == route]
        summary['rotas'][route] = {'n': len(values), 'min_ms': min(values), 'media_ms': round(statistics.mean(values), 4),
                                  'max_ms': max(values), 'p95_ms': sorted(values)[28], 'criterio_ms': 500,
                                  'atende': max(values) < 500}
    (output / 'desempenho.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
