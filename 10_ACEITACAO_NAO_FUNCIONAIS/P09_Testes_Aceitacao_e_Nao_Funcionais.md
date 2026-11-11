# Aceitação e testes não funcionais

Revisão: 2026-11-11T18:05:55-03:00. Sistema: EduTask Web v1.0.1-p2.

## Quatro cenários de aceitação

| ID | Necessidade do estudante | Critério | Verificação técnica |
|---|---|---|---|
| UAT-01 | Cadastrar e acessar sua conta | Cadastro seguro, login e painel próprio vazio | test_uat01_student_registers_and_logs_in |
| UAT-02 | Organizar disciplinas | Salvar e consultar código e dados | test_uat02_student_organizes_disciplines |
| UAT-03 | Priorizar uma entrega próxima | Prazo em dois dias exibe Alta Urgência | test_uat03_student_sees_urgency |
| UAT-04 | Acompanhar seu progresso | Concluir tarefa aumenta contagem e percentual exato | test_uat04_student_tracks_completion |

Resultado técnico: quatro cenários aprovados na suíte e novamente conferidos pela interface. As capturas e o registro de aceitação técnica estão nesta pasta. Executor: assistente de validação técnica. Homologação humana ou assinatura do usuário não são presumidas.
Reproduzir: `python -m pytest -v 10_ACEITACAO_NAO_FUNCIONAIS`.

## Seis verificações não funcionais em três categorias

TNF-01 Desempenho da lista web: GET /tarefas. TNF-02 Desempenho da API: GET /api/tarefas e /api/metricas.
Métrica: todas as respostas abaixo de 500 ms, de acordo com RNF-01. Banco de 1 usuário, 2 disciplinas e 3 tarefas; um cliente sequencial, três aquecimentos e 30 medições por rota. Mede resposta HTTP, não renderização completa ou carga concorrente.

| Rota | Amostras | Média ms | P95 ms | Máximo ms | Critério <500 ms |
|---|---|---|---|---|---|
| /api/metricas | 30 | 4.572 | 5.146 | 5.250 | Atende |
| /api/tarefas | 30 | 4.206 | 4.147 | 26.937 | Atende |
| /tarefas | 30 | 4.157 | 4.578 | 5.488 | Atende |

Fonte: `11_METRICAS_E_QUALIDADE/evidencias/latencias_http.csv` e `desempenho.json`. Reproduzir: `python tools/medir_qualidade.py`.

TNF-03 Usabilidade por inspeção de navegação: quatro fluxos Selenium com controles identificáveis e capturas E2E-01 a E2E-04. Critério: completar os fluxos sem rotas inexistentes e encontrar os resultados nas telas correspondentes. Resultado: quatro fluxos aprovados. Não equivale a estudo de usabilidade com participantes.

TNF-04 Usabilidade por feedback: CT-002, CT-003, CT-004, CT-008, CT-014, CT-020 e CT-021 verificam mensagens específicas na resposta HTML; o template utiliza role=alert. Resultado: verificações aprovadas. Limitação: contraste, leitores de tela e compreensão por usuários não foram avaliados.

TNF-05 Segurança de armazenamento: cadastro real em banco temporário, hash PBKDF2-SHA256 exigido por RNF-02, senha original ausente e check_password_hash positivo. Evidência: test_rnf02_password_hash_and_login em testes.xml. Atende ao requisito original RNF-02. Hashes antigos são migrados após login válido; o teste cobre os caminhos web e API.

TNF-06 Segurança de acesso e entradas: API sem sessão retorna 401, páginas privadas redirecionam, usuário não acessa registros alheios, tentativa de SQL injection não autentica nem altera a base. Evidência: test_r02_api_requires_session, test_r02_users_cannot_read_or_modify_each_others_records e test_r03_sql_injection_does_not_authenticate_or_delete. Resultado: aprovado.

Limites de segurança: não há ensaio de invasão completo, proteção CSRF dedicada ou ensaio de carga. Parecer restrito ao ambiente acadêmico local; não se declara prontidão para produção pública.
