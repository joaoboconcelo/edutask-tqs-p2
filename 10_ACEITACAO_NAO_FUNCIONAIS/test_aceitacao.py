"""Verificação técnica dos cenários de aceitação; homologação humana separada."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '01_SISTEMA_ALVO'))
from edutask.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({'TESTING': True, 'DATABASE': str(tmp_path / 'uat.db')})
    client = app.test_client()
    client.post('/login', data={'email': 'aluno@unisagrado.edu.br', 'password': 'Senha@123'})
    return client


def test_uat01_student_registers_and_logs_in(client):
    client.get('/logout')
    client.post('/register', data={'name': 'Estudante UAT', 'email': 'uat@example.com',
                'password': 'Aceitacao@123', 'confirm_password': 'Aceitacao@123'})
    response = client.post('/login', data={'email': 'uat@example.com', 'password': 'Aceitacao@123'}, follow_redirects=True)
    assert 'Estudante UAT' in response.get_data(as_text=True)
    assert client.get('/api/metricas').json['total_tasks'] == 0


def test_uat02_student_organizes_disciplines(client):
    response = client.post('/disciplinas/nova', data={'code': 'CC-UAT01', 'name': 'Disciplina Aceitação',
                           'teacher': 'Professor UAT', 'workload_hours': 80}, follow_redirects=True)
    assert 'CC-UAT01' in response.get_data(as_text=True)
    assert any(d['code'] == 'CC-UAT01' for d in client.get('/api/disciplinas').json)


def test_uat03_student_sees_urgency(client):
    from datetime import date, timedelta
    response = client.post('/tarefas/nova', data={'title': 'Entrega UAT', 'discipline_id': 1,
        'due_date': (date.today() + timedelta(days=2)).isoformat(), 'priority': 'Alta'}, follow_redirects=True)
    assert 'Alta Urgência' in response.get_data(as_text=True)
    assert any(t['title'] == 'Entrega UAT' for t in client.get('/api/tarefas').json)


def test_uat04_student_tracks_completion(client):
    before = client.get('/api/metricas').json
    task = next(t for t in client.get('/api/tarefas').json if t['status'] != 'Concluída')
    client.post(f"/tarefas/status/{task['id']}", data={'status': 'Concluída'})
    after = client.get('/api/metricas').json
    assert after['completed_tasks'] == before['completed_tasks'] + 1
    assert after['completion_rate_percent'] == round(after['completed_tasks'] / after['total_tasks'] * 100, 2)
    assert str(after['completion_rate_percent']) in client.get('/').get_data(as_text=True)
