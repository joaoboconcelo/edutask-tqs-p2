"""Servidor local descartável para inspeção da interface, sem tocar na demonstração."""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '01_SISTEMA_ALVO'))
from edutask.app import create_app

if __name__ == '__main__':
    with tempfile.TemporaryDirectory(prefix='edutask-interface-') as folder:
        app = create_app({'TESTING': True, 'SECRET_KEY': 'validacao-interface-local',
                          'DATABASE': str(Path(folder) / 'interface.db')})
        app.run(host='127.0.0.1', port=5011, debug=False, use_reloader=False)
