# PRODUTO P08 - TESTES DE SISTEMA E INTERFACE (SELENIUM WEBDRIVER)
**Projeto:** EduTask Web v1.0.0-p2  
**Disciplina:** Testes e Qualidade de Software | **UNISAGRADO 2026**  
**Ferramenta:** Selenium WebDriver 4.51 + Google Chrome / Microsoft Edge  
**Total de Testes E2E Automatizados:** 4 fluxos completos (mínimo exigido: 4)  
**Responsável:** João Lucas de Antonio Boconcelo  

---

## 1. Descrição dos Fluxos Ponta a Ponta (E2E)

| ID do Teste | Fluxo do Usuário | Elementos / Ações | Asserção de Sucesso |
| :--- | :--- | :--- | :--- |
| **test_01** | **Autenticação e Sessão** | Acessa `/login`, preenche `#email`, `#password` e clica em `#btn-login`. | Redirecionamento 302 para `/`, verificação do menu `#nav-dashboard` e exibição dos cards de métricas. |
| **test_02** | **Cadastro de Disciplina** | Acessa `/disciplinas/nova`, preenche código único, nome, docente e carga horária (80h). | Submissão bem-sucedida, redirecionamento para `/disciplinas` e localização da matéria na tabela `#table-disciplines`. |
| **test_03** | **Criação de Atividade Acadêmica** | Acessa `/tarefas/nova`, preenche título, seleciona disciplina, prioridade Alta e data limite. | Redirecionamento para a listagem `/tarefas` e confirmação da linha recém-criada na tabela `#table-tasks`. |
| **test_04** | **Transição de Status e Dashboard** | Seleciona status "Concluída" em tarefa existente, salva status e navega até o Dashboard (`/`). | Verificação do alerta `#flash-alert` e recálculo da barra de progresso `#progress-bar-completion`. |

---

## 2. Como Executar os Testes E2E

### Execução Automatizada:
O script inicia o servidor em segundo plano e executa os testes em modo *headless* (sem interferir na tela do usuário):
```powershell
python test_selenium_e2e.py
```

---

## 3. Log de Execução Real
```text
----------------------------------------------------------------------
127.0.0.1 - "GET /login HTTP/1.1" 200
127.0.0.1 - "POST /login HTTP/1.1" 302
127.0.0.1 - "GET / HTTP/1.1" 200
.
127.0.0.1 - "GET /disciplinas/nova HTTP/1.1" 200
127.0.0.1 - "POST /disciplinas/nova HTTP/1.1" 302
127.0.0.1 - "GET /disciplinas HTTP/1.1" 200
.
127.0.0.1 - "GET /tarefas/nova HTTP/1.1" 200
127.0.0.1 - "POST /tarefas/nova HTTP/1.1" 302
127.0.0.1 - "GET /tarefas HTTP/1.1" 200
.
127.0.0.1 - "POST /tarefas/status/1 HTTP/1.1" 302
127.0.0.1 - "GET / HTTP/1.1" 200
.
----------------------------------------------------------------------
Ran 4 tests in 6.132s

OK (100% de aprovação)
```
