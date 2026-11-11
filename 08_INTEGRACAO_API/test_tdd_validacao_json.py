"""RF-02/R-03: requisições inválidas devem gerar 400, nunca erro interno."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '01_SISTEMA_ALVO'))
from edutask.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({'TESTING': True, 'DATABASE': str(tmp_path / 'json.db')})
    return app.test_client()


@pytest.mark.parametrize('payload', [[1], 'texto', 7, True, None])
@pytest.mark.parametrize('path', ['/api/auth/login', '/api/disciplinas', '/api/tarefas'])
def test_non_object_json_returns_400(client, payload, path):
    if path != '/api/auth/login':
        client.post('/api/auth/login', json={'email': 'aluno@unisagrado.edu.br', 'password': 'Senha@123'})
    response = client.post(path, json=payload)
    assert response.status_code == 400
    assert isinstance(response.get_json().get('error'), str)


@pytest.mark.parametrize('payload', [
    {'email': None, 'password': 'Senha@123'},
    {'email': 123, 'password': 'Senha@123'},
    {'email': ['aluno'], 'password': 'Senha@123'},
    {'email': 'aluno@unisagrado.edu.br', 'password': 123},
    {'email': 'aluno@unisagrado.edu.br', 'password': ['senha']},
])
def test_non_string_credentials_return_400(client, payload):
    response = client.post('/api/auth/login', json=payload)
    assert response.status_code == 400
    assert isinstance(response.get_json().get('error'), str)
