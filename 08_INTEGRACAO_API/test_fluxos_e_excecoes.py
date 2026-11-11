"""Fluxos alternativos e de exclusão que complementam a cobertura funcional."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_SISTEMA_ALVO"))
from edutask.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "flows.db")})
    client = app.test_client()
    client.post("/api/auth/login", json={"email": "aluno@unisagrado.edu.br", "password": "Senha@123"})
    return client


@pytest.mark.parametrize(
    "fields,error", [({"name": "A"}, "nome completo"), ({"email": "email-errado"}, "e-mail inválido")]
)
def test_registration_rejects_invalid_identity(client, fields, error):
    payload = dict(
        name="Estudante Teste",
        email="novo@example.com",
        password="SenhaNova@123",
        confirm_password="SenhaNova@123",
    )
    payload.update(fields)
    response = client.post("/register", data=payload)
    assert error in response.get_data(as_text=True)


def test_login_requires_both_fields(client):
    assert "Preencha todos os campos" in client.post("/login", data={}).get_data(as_text=True)
    assert client.post("/api/auth/login", json={}).status_code == 400


@pytest.mark.parametrize("fields", [{"name": "AB"}, {"teacher": "AB"}, {"code": "INVALIDO"}])
def test_api_discipline_rejects_invalid_fields(client, fields):
    payload = dict(code="CC-FLUX01", name="Disciplina Teste", teacher="Professor Teste", workload_hours=80)
    payload.update(fields)
    before = len(client.get("/api/disciplinas").json)
    response = client.post("/api/disciplinas", json=payload)
    assert response.status_code == 400
    assert len(client.get("/api/disciplinas").json) == before


@pytest.mark.parametrize(
    "fields,message", [({"name": "AB"}, "nome da disciplina"), ({"teacher": "AB"}, "nome do professor")]
)
def test_web_discipline_rejects_invalid_fields(client, fields, message):
    payload = dict(code="CC-FLUX01", name="Disciplina Teste", teacher="Professor Teste", workload_hours=80)
    payload.update(fields)
    assert message in client.post("/disciplinas/nova", data=payload).get_data(as_text=True)


def test_empty_discipline_can_be_deleted(client):
    response = client.post(
        "/api/disciplinas",
        json=dict(code="CC-DEL01", name="Disciplina Vazia", teacher="Professor", workload_hours=80),
    )
    assert response.status_code == 201
    ident = response.json["discipline"]["id"]
    response = client.post(f"/disciplinas/excluir/{ident}", follow_redirects=True)
    assert "Disciplina removida com sucesso" in response.get_data(as_text=True)
    assert all(d["id"] != ident for d in client.get("/api/disciplinas").json)


def test_task_lifecycle_update_delete_and_not_found(client):
    created = client.post(
        "/api/tarefas",
        json=dict(title="Tarefa Ciclo Completo", due_date="2026-12-10", discipline_id=1, priority="Baixa"),
    )
    assert created.status_code == 201
    ident = created.json["task"]["id"]
    assert client.get(f"/api/tarefas/{ident}").json["title"] == "Tarefa Ciclo Completo"
    changed = client.put(f"/api/tarefas/{ident}", json={"status": "Em Andamento", "priority": "Alta"})
    assert changed.status_code == 200
    assert client.get(f"/api/tarefas/{ident}").json["priority"] == "Alta"
    assert client.delete(f"/api/tarefas/{ident}").status_code == 200
    assert client.get(f"/api/tarefas/{ident}").status_code == 404


@pytest.mark.parametrize("fields", [{"status": "Inexistente"}, {"priority": "Urgente"}])
def test_invalid_task_update_does_not_change_record(client, fields):
    before = client.get("/api/tarefas/1").json
    assert client.put("/api/tarefas/1", json=fields).status_code == 400
    assert client.get("/api/tarefas/1").json == before


@pytest.mark.parametrize("date", ["2026-02-30", "data-invalida"])
def test_web_task_rejects_invalid_date(client, date):
    before = client.get("/api/metricas").json["total_tasks"]
    response = client.post(
        "/tarefas/nova",
        data=dict(title="Tarefa Invalida", due_date=date, discipline_id=1),
        follow_redirects=True,
    )
    assert "Formato de data inválido" in response.get_data(as_text=True)
    assert client.get("/api/metricas").json["total_tasks"] == before


@pytest.mark.parametrize("discipline", ["", "99999"])
def test_web_task_requires_accessible_discipline(client, discipline):
    before = client.get("/api/metricas").json["total_tasks"]
    response = client.post(
        "/tarefas/nova",
        data=dict(title="Tarefa Vinculo", due_date="2026-12-10", discipline_id=discipline),
        follow_redirects=True,
    )
    assert (
        "Selecione uma disciplina" if not discipline else "Disciplina não encontrada"
    ) in response.get_data(as_text=True)
    assert client.get("/api/metricas").json["total_tasks"] == before


def test_web_status_validation_and_deletion(client):
    original = client.get("/api/tarefas/3").json["status"]
    response = client.post("/tarefas/status/3", data={"status": "Inválido"}, follow_redirects=True)
    assert "Status inválido" in response.get_data(as_text=True)
    assert client.get("/api/tarefas/3").json["status"] == original
    response = client.post("/tarefas/excluir/3", follow_redirects=True)
    assert "Tarefa excluída com sucesso" in response.get_data(as_text=True)
    assert client.get("/api/tarefas/3").status_code == 404


@pytest.mark.parametrize("path", ["/tarefas/status/1", "/tarefas/excluir/1", "/disciplinas/excluir/1"])
def test_write_routes_require_login(client, path):
    client.get("/logout")
    response = client.post(path, data={"status": "Concluída"})
    assert response.status_code == 302 and response.location.endswith("/login")
