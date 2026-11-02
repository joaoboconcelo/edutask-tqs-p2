# PRODUTO P08 - TESTES DE INTEGRAÇÃO E API (POSTMAN / PYTHON)
**Projeto:** EduTask Web v1.0.0-p2  
**Disciplina:** Testes e Qualidade de Software | **UNISAGRADO 2026**  
**Total de Testes Automatizados de API:** 6 testes (mínimo exigido: 5)  
**Artefatos Exportados:**
* `edutask_api_collection.postman_collection.json`: Coleção oficial Postman v2.1
* `edutask_environment.postman_environment.json`: Variáveis de ambiente (`base_url`, credenciais)
* `test_api_integracao.py`: Script automatizado Python para execução em linha de comando e CI/CD

---

## 1. Cobertura dos Endpoints e Contratos

| Requisição | Método / Rota | Tipo | Critério Validado no Teste |
| :--- | :---: | :---: | :--- |
| **01 - Login Válido** | `POST /api/auth/login` | Positivo | Status 200, mensagem de sucesso e objeto `user` |
| **02 - Login Inválido** | `POST /api/auth/login` | Negativo | Status 401, rejeição de credenciais incorretas |
| **03 - Criar Disciplina** | `POST /api/disciplinas` | Positivo | Status 201, persistência e retorno dos campos |
| **04 - Conflito de Código** | `POST /api/disciplinas` | Negativo | Status 409, bloqueio de código duplicado |
| **05 - Criar Tarefa** | `POST /api/tarefas` | Positivo | Status 201, cálculo automático do score de urgência |
| **06 - Consultar Métricas** | `GET /api/metricas` | Positivo | Status 200, integridade dos indicadores e taxas |

---

## 2. Como Executar

### 2.1 Pelo Postman (Interface Gráfica)
1. Abra o Postman.
2. Clique em **Import** e selecione os dois arquivos JSON desta pasta (`edutask_api_collection.postman_collection.json` e `edutask_environment.postman_environment.json`).
3. Selecione o ambiente **EduTask Local Environment** no canto superior direito.
4. Execute as requisições individualmente ou use o **Collection Runner** para rodar a suíte completa com 1 clique.

### 2.2 Pelo Terminal / Pipeline CI/CD (Sem Postman instalado)
Execute:
```powershell
pytest -v test_api_integracao.py
```

---

## 3. Log de Execução Real
```text
============================= test session starts =============================
platform win32 -- Python 3.13.2, pytest-9.1.1
collected 6 items

test_api_integracao.py::TestEduTaskAPIIntegration::test_01_api_login_success PASSED [ 16%]
test_api_integracao.py::TestEduTaskAPIIntegration::test_02_api_login_invalid_credentials PASSED [ 33%]
test_api_integracao.py::TestEduTaskAPIIntegration::test_03_api_create_discipline_success PASSED [ 50%]
test_api_integracao.py::TestEduTaskAPIIntegration::test_04_api_create_discipline_duplicate_conflict PASSED [ 66%]
test_api_integracao.py::TestEduTaskAPIIntegration::test_05_api_create_task_with_calculated_urgency PASSED [ 83%]
test_api_integracao.py::TestEduTaskAPIIntegration::test_06_api_get_metrics_success PASSED [100%]

============================== 6 passed in 0.70s ==============================
```
