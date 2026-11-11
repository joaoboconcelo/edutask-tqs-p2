"""Casos de regressão rastreados a requisitos e riscos do produto P02."""

import sys
from pathlib import Path

import pytest
from werkzeug.security import check_password_hash

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_SISTEMA_ALVO"))
from edutask.app import create_app
from edutask.models import get_db_connection


@pytest.fixture
def app(tmp_path):
    return create_app(
        {"TESTING": True, "SECRET_KEY": "regression-only", "DATABASE": str(tmp_path / "regression.db")}
    )


@pytest.fixture
def client(app):
    client = app.test_client()
    client.post("/api/auth/login", json={"email": "aluno@unisagrado.edu.br", "password": "Senha@123"})
    return client


@pytest.mark.parametrize("path", ["/api/tarefas", "/api/disciplinas", "/api/metricas"])
def test_r02_api_requires_session(app, path):
    assert app.test_client().get(path).status_code == 401


@pytest.mark.parametrize("path", ["/", "/tarefas", "/disciplinas", "/tarefas/nova", "/disciplinas/nova"])
def test_ct010_private_pages_redirect(app, path):
    response = app.test_client().get(path)
    assert response.status_code == 302
    assert response.location.endswith("/login")


def test_rnf02_password_hash_and_login(app):
    client = app.test_client()
    response = client.post(
        "/register",
        data={
            "name": "Aluno Novo",
            "email": "novo@example.com",
            "password": "NovaSenha@123",
            "confirm_password": "NovaSenha@123",
        },
    )
    assert response.status_code == 302
    with app.app_context():
        conn = get_db_connection()
        row = conn.execute(
            "SELECT password_hash FROM users WHERE email = ?", ("novo@example.com",)
        ).fetchone()
        conn.close()
    assert row is not None
    assert row["password_hash"].startswith("pbkdf2:sha256:")
    assert "NovaSenha@123" not in row["password_hash"]
    assert check_password_hash(row["password_hash"], "NovaSenha@123")
    assert (
        client.post("/login", data={"email": "novo@example.com", "password": "NovaSenha@123"}).status_code
        == 302
    )


@pytest.mark.parametrize(
    "password,confirm,message",
    [
        ("Abc@123", "Abc@123", "mínimo 8"),
        ("SenhaForte2026", "SenhaForte2026", "caractere especial"),
        ("senhaforte@123", "senhaforte@123", "maiúscula"),
        ("SenhaForte@2026", "OutraSenha@2026", "não coincidem"),
    ],
)
def test_rf01_rejects_invalid_registration(app, password, confirm, message):
    response = app.test_client().post(
        "/register",
        data={
            "name": "Aluno Novo",
            "email": "novo@example.com",
            "password": password,
            "confirm_password": confirm,
        },
    )
    assert message in response.get_data(as_text=True)
    with app.app_context():
        conn = get_db_connection()
        assert (
            conn.execute("SELECT COUNT(*) FROM users WHERE email = ?", ("novo@example.com",)).fetchone()[0]
            == 0
        )
        conn.close()


@pytest.mark.parametrize("hours,status", [(14, 400), (15, 201), (400, 201), (401, 400), ("abc", 400)])
def test_rf03_workload_boundaries(client, hours, status):
    response = client.post(
        "/api/disciplinas",
        json={"code": "CC-REG01", "name": "Regressão", "teacher": "Professor", "workload_hours": hours},
    )
    assert response.status_code == status
    assert any(d["code"] == "CC-REG01" for d in client.get("/api/disciplinas").json) == (status == 201)


def task_payload(**overrides):
    return dict(
        {
            "title": "Tarefa de regressão",
            "description": "Evidência controlada",
            "due_date": "2026-11-30",
            "priority": "Alta",
            "discipline_id": 1,
        },
        **overrides,
    )


@pytest.mark.parametrize(
    "override,status",
    [
        ({"title": "AB"}, 400),
        ({"due_date": ""}, 400),
        ({"due_date": "2026-02-30"}, 400),
        ({"due_date": "data inválida"}, 400),
        ({"priority": "Urgente"}, 400),
        ({"discipline_id": 99999}, 404),
    ],
)
def test_rf04_invalid_task_does_not_persist(client, override, status):
    before = client.get("/api/metricas").json["total_tasks"]
    response = client.post("/api/tarefas", json=task_payload(**override))
    assert response.status_code == status
    assert client.get("/api/metricas").json["total_tasks"] == before


def test_rf05_status_updates_exact_dashboard_rate(client):
    task = client.post("/api/tarefas", json=task_payload()).json["task"]
    assert client.put(f"/api/tarefas/{task['id']}", json={"status": "Concluída"}).status_code == 200
    metrics = client.get("/api/metricas").json
    assert metrics["completion_rate_percent"] == round(
        metrics["completed_tasks"] / metrics["total_tasks"] * 100, 2
    )
    assert client.get(f"/api/tarefas/{task['id']}").json["status"] == "Concluída"
    assert str(metrics["completion_rate_percent"]) in client.get("/").get_data(as_text=True)


def test_rf06_combined_filters_and_search(client):
    created = client.post("/api/tarefas", json=task_payload(title="Busca Única Regressão")).json["task"]
    rows = client.get("/api/tarefas?status=Pendente&priority=Alta").json
    assert any(t["id"] == created["id"] for t in rows)
    assert all(t["status"] == "Pendente" and t["priority"] == "Alta" for t in rows)
    assert "Busca Única Regressão" in client.get("/tarefas?q=Busca+Única+Regressão").get_data(as_text=True)
    assert "Busca Única Regressão" not in client.get("/tarefas?q=string-inexistente-xyz").get_data(
        as_text=True
    )


def test_r05_discipline_with_tasks_cannot_be_deleted(client):
    response = client.post("/disciplinas/excluir/1", follow_redirects=True)
    assert "Não é possível excluir" in response.get_data(as_text=True)
    assert any(d["id"] == 1 for d in client.get("/api/disciplinas").json)


def test_r02_users_cannot_read_or_modify_each_others_records(app, client):
    stranger = app.test_client()
    stranger.post(
        "/register",
        data={
            "name": "Outro Aluno",
            "email": "outro@example.com",
            "password": "OutraSenha@123",
            "confirm_password": "OutraSenha@123",
        },
    )
    stranger.post("/api/auth/login", json={"email": "outro@example.com", "password": "OutraSenha@123"})
    assert stranger.get("/api/tarefas").json == []
    assert stranger.get("/api/disciplinas").json == []
    assert stranger.get("/api/metricas").json["total_tasks"] == 0
    assert stranger.get("/api/tarefas/1").status_code == 404
    assert stranger.put("/api/tarefas/1", json={"status": "Concluída"}).status_code == 404
    assert stranger.delete("/api/tarefas/1").status_code == 404
    assert stranger.post("/api/tarefas", json=task_payload()).status_code == 404
    before = client.get("/api/tarefas/1").json
    stranger.post("/tarefas/status/1", data={"status": "Concluída"})
    stranger.post("/tarefas/excluir/1")
    assert client.get("/api/tarefas/1").json == before


def test_r03_sql_injection_does_not_authenticate_or_delete(app, client):
    anon = app.test_client()
    assert (
        anon.post("/api/auth/login", json={"email": "' OR '1'='1", "password": "qualquer"}).status_code == 401
    )
    before = client.get("/api/metricas").json
    assert client.get("/tarefas?q=';DROP+TABLE+tasks;--").status_code == 200
    assert client.get("/api/metricas").json == before


def test_isolated_databases_do_not_share_records(app, tmp_path, client):
    other_app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "other.db")})
    other = other_app.test_client()
    other.post("/api/auth/login", json={"email": "aluno@unisagrado.edu.br", "password": "Senha@123"})
    before = other.get("/api/metricas").json
    client.post("/api/tarefas", json=task_payload())
    assert other.get("/api/metricas").json == before
