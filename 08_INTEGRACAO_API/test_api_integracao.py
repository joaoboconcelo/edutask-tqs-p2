"""
SUÍTE DE TESTES DE INTEGRAÇÃO E API AUTOMATIZADOS
Projeto: EduTask Web v1.0.0-p2
UNISAGRADO - Ciência da Computação - Testes e Qualidade de Software
Responsável: João Lucas de Antonio Boconcelo
Total: 6 testes automatizados cobrindo fluxos positivos e negativos da API RESTful.
"""

import sys
import os
import unittest
import json
import tempfile

# Inclui caminho da aplicação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01_SISTEMA_ALVO")))

from edutask.app import create_app
from edutask.services.task_service import calculate_task_urgency


class TestEduTaskAPIIntegration(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-key-tqs",
                "DATABASE": os.path.join(self.tempdir.name, "test.db"),
            }
        )
        self.client = self.app.test_client()
        self.client.post(
            "/api/auth/login", json={"email": "aluno@unisagrado.edu.br", "password": "Senha@123"}
        )

    # 1. API Login - Fluxo Positivo (Status 200)
    def test_01_api_login_success(self):
        payload = {"email": "aluno@unisagrado.edu.br", "password": "Senha@123"}
        response = self.client.post(
            "/api/auth/login", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Autenticação realizada com sucesso.")
        self.assertIn("user", data)
        self.assertEqual(data["user"]["email"], "aluno@unisagrado.edu.br")

    # 2. API Login - Fluxo Negativo (Status 401)
    def test_02_api_login_invalid_credentials(self):
        payload = {"email": "aluno@unisagrado.edu.br", "password": "SenhaIncorreta@99"}
        response = self.client.post(
            "/api/auth/login", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data["error"], "Credenciais inválidas.")

    # 3. API Disciplinas - Criar Disciplina Válida (Status 201)
    def test_03_api_create_discipline_success(self):
        payload = {
            "code": "CC-AUTO01",
            "name": "Automação de Testes de Software",
            "teacher": "Prof. Dr. Elvio Gilberto da Silva",
            "workload_hours": 80,
        }
        response = self.client.post(
            "/api/disciplinas", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        if response.status_code == 201:
            data = response.get_json()
            self.assertEqual(data["discipline"]["code"], "CC-AUTO01")
            self.assertEqual(data["discipline"]["workload_hours"], 80)

    # 4. API Disciplinas - Código Duplicado (Status 409)
    def test_04_api_create_discipline_duplicate_conflict(self):
        payload = {
            "code": "CC-TQS01",
            "name": "Matéria Duplicada",
            "teacher": "Professor",
            "workload_hours": 60,
        }
        response = self.client.post(
            "/api/disciplinas", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertIn("já existe", data["error"])

    # 5. API Tarefas - Criar Atividade com Urgência Calculada (Status 201)
    def test_05_api_create_task_with_calculated_urgency(self):
        payload = {
            "title": "Entrega do Relatório de Métricas e Gráficos",
            "description": "Consolidar 8 indicadores em documento",
            "due_date": "2026-11-20",
            "priority": "Alta",
            "discipline_id": 1,
        }
        response = self.client.post("/api/tarefas", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["task"]["title"], "Entrega do Relatório de Métricas e Gráficos")
        self.assertEqual(data["task"]["priority"], "Alta")
        self.assertIn("urgency_score", data["task"])
        self.assertIsInstance(data["task"]["urgency_score"], int)

    # 6. API Métricas - Consulta de Indicadores Gerais (Status 200)
    def test_06_api_get_metrics_success(self):
        for task in self.client.get('/api/tarefas').get_json():
            self.assertEqual(
                (task['urgency_score'], task['urgency_level']),
                calculate_task_urgency(task['due_date']),
            )
        response = self.client.get("/api/metricas")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("total_tasks", data)
        self.assertIn("completed_tasks", data)
        self.assertIn("completion_rate_percent", data)
        self.assertIsInstance(data["completion_rate_percent"], (int, float))


if __name__ == "__main__":
    unittest.main()
