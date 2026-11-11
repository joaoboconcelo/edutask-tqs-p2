"""Reexecução automatizada dos 24 cenários; não substitui a execução manual."""

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "01_SISTEMA_ALVO"))
from edutask.app import create_app
from edutask.models import get_db_connection


@pytest.mark.parametrize("case", range(1, 25), ids=lambda i: f"CT-{i:03}")
def test_catalog_case(case, tmp_path):
    app = create_app(
        {"TESTING": True, "SECRET_KEY": "catalog-only", "DATABASE": str(tmp_path / "catalog.db")}
    )
    client = app.test_client()
    expected = ""
    if case <= 6:
        payload = dict(
            name="Carlos Silva",
            email="carlos.silva@unisagrado.edu.br",
            password="SenhaForte@2026",
            confirm_password="SenhaForte@2026",
        )
        changes = {
            2: {"email": "email_sem_arroba.com"},
            3: {"password": "Abc@123", "confirm_password": "Abc@123"},
            4: {"password": "SenhaForte2026", "confirm_password": "SenhaForte2026"},
            5: {"email": "aluno@unisagrado.edu.br"},
            6: {"confirm_password": "Diferente@123"},
        }
        payload.update(changes.get(case, {}))
        expected = {
            1: "Cadastro realizado com sucesso",
            2: "Formato de e-mail inválido",
            3: "mínimo 8 caracteres",
            4: "caractere especial",
            5: "já está cadastrado",
            6: "não coincidem",
        }[case]
        response = client.post("/register", data=payload, follow_redirects=True)
        with app.app_context():
            conn = get_db_connection()
            count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            conn.close()
        assert count == (2 if case == 1 else 1)
    elif case in (7, 8, 9):
        response = client.post(
            "/login",
            data={
                "email": "inexistente@example.com" if case == 9 else "aluno@unisagrado.edu.br",
                "password": "Senha@123" if case == 7 else "Incorreta@123",
            },
            follow_redirects=True,
        )
        expected = "Dashboard" if case == 7 else "Credenciais inválidas"
        with client.session_transaction() as state:
            assert ("user_id" in state) == (case == 7)
    elif case == 10:
        response = client.get("/tarefas")
        assert response.status_code == 302 and response.location.endswith("/login")
    else:
        client.post("/login", data={"email": "aluno@unisagrado.edu.br", "password": "Senha@123"})
        if case <= 17:
            payload = dict(
                code="CC-REG01", name="Disciplina Revisada", teacher="Professor Teste", workload_hours="80"
            )
            payload.update(
                {
                    12: {"code": "CODIGOERRADO"},
                    13: {"workload_hours": "15"},
                    14: {"workload_hours": "14"},
                    15: {"workload_hours": "400"},
                    16: {"workload_hours": "401"},
                    17: {"code": "CC-TQS01"},
                }.get(case, {})
            )
            response = client.post("/disciplinas/nova", data=payload, follow_redirects=True)
            expected = (
                "Disciplina cadastrada com sucesso"
                if case in (11, 13, 15)
                else (
                    "Código de disciplina inválido"
                    if case == 12
                    else "Já existe uma disciplina" if case == 17 else "entre 15 e 400"
                )
            )
            with app.app_context():
                conn = get_db_connection()
                count = conn.execute("SELECT COUNT(*) FROM disciplines").fetchone()[0]
                conn.close()
            assert count == (3 if case in (11, 13, 15) else 2)
        elif case == 18:
            response = client.post("/disciplinas/excluir/1", follow_redirects=True)
            expected = "Não é possível excluir"
        elif case in (19, 20, 21):
            payload = dict(
                title="Tarefa de revisão",
                description="Registro verificável",
                due_date=(date.today() + timedelta(days=10)).isoformat(),
                priority="Alta",
                discipline_id="1",
            )
            payload.update({20: {"title": "AB"}, 21: {"due_date": ""}}.get(case, {}))
            response = client.post("/tarefas/nova", data=payload, follow_redirects=True)
            expected = {
                19: "Atividade acadêmica cadastrada com sucesso",
                20: "mínimo 3 caracteres",
                21: "data limite de entrega é obrigatória",
            }[case]
            with app.app_context():
                conn = get_db_connection()
                count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
                conn.close()
            assert count == (4 if case == 19 else 3)
        elif case == 22:
            before = client.get("/api/metricas").json
            tasks = client.get("/api/tarefas").json
            task = next(t for t in tasks if t["status"] != "Concluída")
            client.post(f"/tarefas/status/{task['id']}", data={"status": "Concluída"})
            after = client.get("/api/metricas").json
            assert after["completed_tasks"] == before["completed_tasks"] + 1
            assert after["completion_rate_percent"] == round(
                after["completed_tasks"] / after["total_tasks"] * 100, 2
            )
            response = client.get("/")
            expected = str(after["completion_rate_percent"])
        elif case == 23:
            client.post('/api/tarefas', json={
                'title': 'Alvo filtro Pendente Alta', 'due_date': '2026-11-30',
                'priority': 'Alta', 'discipline_id': 1,
            })
            rows = client.get("/api/tarefas?status=Pendente&priority=Alta").json
            assert rows and all(t["status"] == "Pendente" and t["priority"] == "Alta" for t in rows)
            response = client.get("/tarefas?status=Pendente&priority=Alta")
            for row in rows:
                assert row["title"] in response.get_data(as_text=True)
        else:
            response = client.get("/tarefas?q=string-inexistente-xyz")
            expected = "Nenhuma atividade encontrada"
    assert response.status_code in (200, 302)
    assert expected in response.get_data(as_text=True)
    evidence = ROOT / "05_EXECUCAO_MANUAL" / "evidencias_reexecucao"
    evidence.mkdir(exist_ok=True)
    (evidence / f"CT-{case:03}.html").write_text(response.get_data(as_text=True), encoding="utf-8")
    (evidence / f"CT-{case:03}.json").write_text(
        json.dumps(
            {
                "caso": f"CT-{case:03}",
                "metodo": "Flask test client automatizado",
                "resultado": "Aprovado",
                "status_http": response.status_code,
                "verificacao_textual": expected,
                "banco": "isolado por cenário",
                "data_execucao": __import__("datetime")
                .datetime.now(__import__("datetime").timezone(__import__("datetime").timedelta(hours=-3)))
                .isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
