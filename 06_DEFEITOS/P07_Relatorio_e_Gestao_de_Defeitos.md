# Defeitos confirmados na revisão de 11 de novembro de 2026

DEF-03 a DEF-06 correspondem às issues #1 a #4, encerradas com reteste remoto. DEF-07 e DEF-08 correspondem às issues #6 e #7, encerradas após correção publicada, regressão local e reteste remoto aprovado na execução 43099616601. A decisão humana de homologação é separada do reteste técnico.

## DEF-03 Taxa de conclusão aceita concluídas positivas com total zero

Requisito: RF-05. Risco: R-06. Severidade: Média. Prioridade: Alta.

Ambiente: Python 3.13.2, Flask, SQLite local isolado. Data: 11/11/2026. Status: Encerrado na revisão local.

Obtido antes: calculate_completion_rate(0, 1) retornava 0.0 em vez de rejeitar a inconsistência.

Esperado: rejeitar entradas inconsistentes, preservar isolamento e responder sem erro interno.

Correção: Verificar completed_tasks > total_tasks antes do caso vazio.

Reprodução e reteste: `test_tdd_consistencia.py / red.xml e green.xml`. Linha de base: commit a0df9e6a2dd69687bc88222fca707bdc6f877583. Correção publicada: commit 33d441c7f6dc4599da735727f232c5c1aa5d41f3. Logs consolidados em `11_METRICAS_E_QUALIDADE/evidencias/testes.xml`.

Responsabilidade: revisão técnica; validação dos integrantes pendente.

## DEF-04 Configuração de banco ignorada e testes contaminam demonstração

Requisito: RF-03/RF-04. Risco: R-05. Severidade: Média. Prioridade: Alta.

Ambiente: Python 3.13.2, Flask, SQLite local isolado. Data: 11/11/2026. Status: Encerrado na revisão local.

Obtido antes: models.py usava caminho global enquanto create_app aceitava DATABASE sem aplicá-lo.

Esperado: rejeitar entradas inconsistentes, preservar isolamento e responder sem erro interno.

Correção: Ler DATABASE de current_app, inicializar dentro do contexto e usar temporários.

Reprodução e reteste: `test_isolated_databases_do_not_share_records`. Linha de base: commit a0df9e6a2dd69687bc88222fca707bdc6f877583. Correção publicada: commit 33d441c7f6dc4599da735727f232c5c1aa5d41f3. Logs consolidados em `11_METRICAS_E_QUALIDADE/evidencias/testes.xml`.

Responsabilidade: revisão técnica; validação dos integrantes pendente.

## DEF-05 API permite leitura e alteração sem sessão e mistura dados de usuários

Requisito: RF-02. Risco: R-02. Severidade: Alta. Prioridade: Alta.

Ambiente: Python 3.13.2, Flask, SQLite local isolado. Data: 11/11/2026. Status: Encerrado na revisão local.

Obtido antes: Endpoints não verificavam sessão e gravavam user_id=1. Consultas HTML não filtravam o proprietário.

Esperado: rejeitar entradas inconsistentes, preservar isolamento e responder sem erro interno.

Correção: Exigir sessão na API e filtrar leituras e escritas por user_id.

Reprodução e reteste: `test_r02_api_requires_session / test_r02_users_cannot_read_or_modify_each_others_records`. Linha de base: commit a0df9e6a2dd69687bc88222fca707bdc6f877583. Correção publicada: commit 33d441c7f6dc4599da735727f232c5c1aa5d41f3. Logs consolidados em `11_METRICAS_E_QUALIDADE/evidencias/testes.xml`.

Responsabilidade: revisão técnica; validação dos integrantes pendente.

## DEF-06 Data inválida na API causa exceção em vez de resposta 400

Requisito: RF-04. Risco: R-07. Severidade: Alta. Prioridade: Alta.

Ambiente: Python 3.13.2, Flask, SQLite local isolado. Data: 11/11/2026. Status: Encerrado na revisão local.

Obtido antes: POST /api/tarefas com due_date=2026-02-30 propagava ValueError.

Esperado: rejeitar entradas inconsistentes, preservar isolamento e responder sem erro interno.

Correção: Capturar ValueError, encerrar conexão e retornar JSON com HTTP 400 sem persistência.

Reprodução e reteste: `test_rf04_invalid_task_does_not_persist`. Linha de base: commit a0df9e6a2dd69687bc88222fca707bdc6f877583. Correção publicada: commit 33d441c7f6dc4599da735727f232c5c1aa5d41f3. Logs consolidados em `11_METRICAS_E_QUALIDADE/evidencias/testes.xml`.

Responsabilidade: revisão técnica; validação dos integrantes pendente.

## DEF-07 API recebe JSON ou credenciais de tipos inválidos

Requisito: RF-02. Risco: R-03. Severidade: Média. Prioridade: Alta. Status: corrigido e retestado local e remotamente; issue #6 encerrada após publicação.

Reprodução: enviar POST /api/auth/login com JSON [1], um escalar ou e-mail/senha não textuais. Antes, havia AttributeError ou erro interno. Esperado: HTTP 400 com erro JSON.

Correção: json_payload_error verifica o contrato antes do acesso a campos. O ciclo TDD novo registrou 17 falhas e três aprovações no RED, seguido de 20 aprovações no GREEN e no REFACTOR. Commits reais e logs estão em evidencias/tdd_json da pasta 12.

Reteste: test_tdd_validacao_json.py e suíte ampliada. Correção publicada no commit 4acc9d5d7c1d065e152ded6c19699e7c94057f49. A conclusão da nova execução remota é acompanhada separadamente.

## DEF-08 Hash divergente do RNF-02 original

Requisito: RNF-02. Risco: R-01. Severidade: Média. Prioridade: Alta. Status: corrigido e retestado local e remotamente; issue #7 encerrada após publicação.

Antes: o cadastro usava scrypt por padrão, enquanto RNF-02 especificava PBKDF2-SHA256. A divergência é de requisito, sem declarar scrypt inseguro. Esperado: novos cadastros e seed em PBKDF2-SHA256 e compatibilidade com dados existentes.

Correção: método explícito no cadastro e seed, com atualização transparente do hash antigo após autenticação válida, preservando a senha. Reteste: test_hash_requisito.py cobre seed e migração por login web/API; o cadastro exige PBKDF2 no teste RNF-02. Commit: 4acc9d5d7c1d065e152ded6c19699e7c94057f49.

## Vínculos e reteste remoto

- DEF-03: https://github.com/joaoboconcelo/edutask-tqs-p2/issues/1
- DEF-04: https://github.com/joaoboconcelo/edutask-tqs-p2/issues/2
- DEF-05: https://github.com/joaoboconcelo/edutask-tqs-p2/issues/3
- DEF-06: https://github.com/joaoboconcelo/edutask-tqs-p2/issues/4

Suíte publicada aprovada: https://github.com/joaoboconcelo/edutask-tqs-p2/actions/runs/43094289919 . Os defeitos são registros da revisão de 11/11/2026, sem retrodatação.

- DEF-07: https://github.com/joaoboconcelo/edutask-tqs-p2/issues/6
- DEF-08: https://github.com/joaoboconcelo/edutask-tqs-p2/issues/7
