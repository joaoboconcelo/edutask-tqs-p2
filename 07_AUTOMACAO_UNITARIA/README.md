# PRODUTO P08 - TESTES UNITÁRIOS AUTOMATIZADOS
**Projeto:** EduTask Web v1.0.0-p2  
**Disciplina:** Testes e Qualidade de Software | **UNISAGRADO 2026**  
**Framework:** Pytest 9.1 / Unittest  
**Total de Testes Automatizados:** 8 testes unitários independentes (exigência mínima: 6)  

---

## 1. Descrição dos Casos de Teste Unitários
1. `test_validate_email_valid_formats`: Valida e-mails institucionais legítimos (`RF-01`).
2. `test_validate_email_invalid_formats`: Valida rejeição de e-mails sem arroba, sem domínio ou nulos (`RF-01`).
3. `test_password_strength_valid`: Valida aceitação de senha que atende aos 4 critérios de complexidade (`RF-01`).
4. `test_password_strength_invalid_rules`: Explora limites de comprimento (7 chars) e ausência de maiúsculas/números/especiais (`RF-01`, `CT-003`, `DEF-01`).
5. `test_validate_discipline_code`: Valida formato com expressão regular `[A-Z]{2,4}-[A-Z0-9]{2,6}` (`RF-03`, `CT-011`, `CT-012`).
6. `test_validate_workload_boundary_values`: Aplica Análise de Valor Limite em 14h, 15h, 400h e 401h (`RF-03`, `CT-013`, `CT-014`, `CT-015`, `CT-016`, `DEF-02`).
7. `test_calculate_completion_rate`: Valida precisão matemática da taxa de progresso e prevenção de divisão por zero (`RF-05`, `R-06`).
8. `test_calculate_task_urgency`: Valida regras de urgência da data limite desenvolvidas pelo ciclo TDD (`RF-04`, `R-07`).

---

## 2. Como Executar
No terminal, execute:
```powershell
pytest -v test_unitarios.py
```
Ou utilizando o unittest integrado do Python:
```powershell
python test_unitarios.py
```

---

## 3. Log de Execução Real
```text
============================= test session starts =============================
platform win32 -- Python 3.13.2, pytest-9.1.1
collected 8 items

test_unitarios.py::TestTaskServiceUnit::test_calculate_completion_rate PASSED [ 12%]
test_unitarios.py::TestTaskServiceUnit::test_calculate_task_urgency PASSED [ 25%]
test_unitarios.py::TestTaskServiceUnit::test_password_strength_invalid_rules PASSED [ 37%]
test_unitarios.py::TestTaskServiceUnit::test_password_strength_valid PASSED [ 50%]
test_unitarios.py::TestTaskServiceUnit::test_validate_discipline_code PASSED [ 62%]
test_unitarios.py::TestTaskServiceUnit::test_validate_email_invalid_formats PASSED [ 75%]
test_unitarios.py::TestTaskServiceUnit::test_validate_email_valid_formats PASSED [ 87%]
test_unitarios.py::TestTaskServiceUnit::test_validate_workload_boundary_values PASSED [100%]

============================== 8 passed in 0.49s ==============================
```
