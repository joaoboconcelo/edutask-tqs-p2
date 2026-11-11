"""
SUÍTE DE TESTES UNITÁRIOS AUTOMATIZADOS (PYTEST / UNITTEST)
Projeto: EduTask Web v1.0.0-p2
UNISAGRADO - Ciência da Computação - Testes e Qualidade de Software
Responsável: João Lucas de Antonio Boconcelo
"""

import sys
import os
import unittest
from datetime import date, timedelta

# Adiciona o caminho da aplicação ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01_SISTEMA_ALVO")))

from edutask.services.task_service import (
    validate_email,
    validate_password_strength,
    validate_discipline_code,
    validate_workload,
    calculate_completion_rate,
    calculate_task_urgency,
    filter_task_list,
)


class TestTaskServiceUnit(unittest.TestCase):

    # 1. Teste de Validação de Formato de E-mail (Válidos)
    def test_validate_email_valid_formats(self):
        self.assertTrue(validate_email("aluno@unisagrado.edu.br"))
        self.assertTrue(validate_email("usuario.teste@exemplo.com"))
        self.assertTrue(validate_email("contato@dominio.org"))

    # 2. Teste de Validação de Formato de E-mail (Inválidos)
    def test_validate_email_invalid_formats(self):
        self.assertFalse(validate_email("emailsemarroba.com"))
        self.assertFalse(validate_email("@semusuario.com"))
        self.assertFalse(validate_email("usuario@.com"))
        self.assertFalse(validate_email(""))
        self.assertFalse(validate_email(None))

    # 3. Teste de Política de Força de Senha (Válida)
    def test_password_strength_valid(self):
        is_valid, msg = validate_password_strength("SenhaForte@2026")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "Senha válida.")

    # 4. Teste de Política de Força de Senha (Inválida por Regras e Limites)
    def test_password_strength_invalid_rules(self):
        # Limite inferior de tamanho (7 caracteres)
        is_valid, msg = validate_password_strength("Abc@123")
        self.assertFalse(is_valid)
        self.assertIn("mínimo 8 caracteres", msg)

        # Sem letra maiúscula
        is_valid, msg = validate_password_strength("senhafraca@123")
        self.assertFalse(is_valid)
        self.assertIn("letra maiúscula", msg)

        # Sem número
        is_valid, msg = validate_password_strength("SenhaSemNumero@")
        self.assertFalse(is_valid)
        self.assertIn("pelo menos um número", msg)

        # Sem caractere especial
        is_valid, msg = validate_password_strength("SenhaSemEspecial2026")
        self.assertFalse(is_valid)
        self.assertIn("caractere especial", msg)

    # 5. Teste de Formato de Código de Disciplina
    def test_validate_discipline_code(self):
        self.assertTrue(validate_discipline_code("CC-TQS01"))
        self.assertTrue(validate_discipline_code("ENG-101"))
        self.assertTrue(validate_discipline_code("MAT-01"))

        # Códigos inválidos
        self.assertFalse(validate_discipline_code("CODIGOERRADO"))
        self.assertFalse(validate_discipline_code("C-1"))
        self.assertFalse(validate_discipline_code(""))

    # 6. Teste de Carga Horária com Análise de Valor Limite (BVA)
    def test_validate_workload_boundary_values(self):
        # Limite inferior válido e inválido
        self.assertFalse(validate_workload(14))  # 14h -> Inválido (DEF-02)
        self.assertTrue(validate_workload(15))  # 15h -> Limite inferior válido

        # Ponto médio válido
        self.assertTrue(validate_workload(80))

        # Limite superior válido e inválido
        self.assertTrue(validate_workload(400))  # 400h -> Limite superior válido
        self.assertFalse(validate_workload(401))  # 401h -> Inválido

        # Entradas não numéricas
        self.assertFalse(validate_workload("abc"))

    # 7. Teste de Cálculo de Taxa de Conclusão e Tratamento de Divisão por Zero
    def test_calculate_completion_rate(self):
        # Caso clássico de risco: 0 tarefas cadastradas (Divisão por zero)
        self.assertEqual(calculate_completion_rate(0, 0), 0.0)

        # Casos normais
        self.assertEqual(calculate_completion_rate(10, 5), 50.0)
        self.assertEqual(calculate_completion_rate(3, 1), 33.33)
        self.assertEqual(calculate_completion_rate(4, 4), 100.0)

        # Exceções esperadas para dados inconsistentes
        with self.assertRaises(ValueError):
            calculate_completion_rate(5, 6)  # Concluídas > Total

    # 8. Teste de Cálculo de Urgência de Tarefas (Regra do TDD)
    def test_calculate_task_urgency(self):
        hoje = date.today()

        # Tarefa em atraso / vencida (Score 100)
        passado = (hoje - timedelta(days=2)).strftime("%Y-%m-%d")
        score, nivel = calculate_task_urgency(passado, hoje)
        self.assertEqual(score, 100)
        self.assertEqual(nivel, "Crítica / Em Atraso")

        # Tarefa para daqui 2 dias (Alta Urgência - Score 75)
        dois_dias = (hoje + timedelta(days=2)).strftime("%Y-%m-%d")
        score, nivel = calculate_task_urgency(dois_dias, hoje)
        self.assertEqual(score, 75)
        self.assertEqual(nivel, "Alta Urgência")

        # Tarefa para daqui 5 dias (Média Urgência - Score 50)
        cinco_dias = (hoje + timedelta(days=5)).strftime("%Y-%m-%d")
        score, nivel = calculate_task_urgency(cinco_dias, hoje)
        self.assertEqual(score, 50)
        self.assertEqual(nivel, "Média Urgência")

        # Tarefa para daqui 15 dias (Normal - Score 25)
        quinze_dias = (hoje + timedelta(days=15)).strftime("%Y-%m-%d")
        score, nivel = calculate_task_urgency(quinze_dias, hoje)
        self.assertEqual(score, 25)
        self.assertEqual(nivel, "Normal")


if __name__ == "__main__":
    unittest.main()
