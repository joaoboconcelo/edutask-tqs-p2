# PRODUTO P05 - MATRIZ DE RASTREABILIDADE (APÊNDICE H)
**Projeto:** EduTask Web v1.0.1-p2 | **UNISAGRADO 2026**
**Disciplina:** Testes e Qualidade de Software
**Equipe:** Gabriel Henrique Moreira, João Lucas de Antonio Boconcelo, Lucas Braga

---

| Requisito | Risco Associado | Caso(s) de Teste | Execução(ões) | Defeito(s) Vinculado(s) | Situação Final |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **RF-01** (Cadastro de Usuário) | R-03 (Entradas inválidas) | CT-001 | EX-001 | Nenhum | Conforme / Aprovado |
| **RF-01** (Validação de E-mail) | R-03 (E-mail malformado) | CT-002 | EX-002 | Nenhum | Conforme / Aprovado |
| **RF-01** (Política de Senha - Tamanho) | R-03 (Senha curta) | CT-003 | EX-003 | Nenhum | Conforme / Aprovado |
| **RF-01** (Complexidade de Senha) | R-03 (Senha sem especial) | CT-004 | EX-004 | DEF-01 (Corrigido) | Conforme / Aprovado após reteste |
| **RF-01** (Unicidade de E-mail) | R-03 (E-mail duplicado) | CT-005 | EX-005 | Nenhum | Conforme / Aprovado |
| **RF-01** (Confirmação de Senha) | R-03 (Senhas divergentes) | CT-006 | EX-006 | Nenhum | Conforme / Aprovado |
| **RF-02** (Login Válido) | R-02 (Falha de autenticação) | CT-007 | EX-007 | Nenhum | Conforme / Aprovado |
| **RF-02** (Senha Incorreta) | R-02 (Acesso indevido) | CT-008 | EX-008 | Nenhum | Conforme / Aprovado |
| **RF-02** (Usuário Inexistente) | R-02 (Exposição de usuário) | CT-009 | EX-009 | Nenhum | Conforme / Aprovado |
| **RF-02** / **RNF-02** (Proteção de Rota) | R-02 (Acesso sem sessão) | CT-010 | EX-010 | Nenhum | Conforme / Aprovado |
| **RF-03** (Cadastro Disciplina Válida) | R-04 (Inconsistência cadastral) | CT-011 | EX-011 | Nenhum | Conforme / Aprovado |
| **RF-03** (Formato do Código Disciplina) | R-03 (Formato fora do padrão) | CT-012 | EX-012 | Nenhum | Conforme / Aprovado |
| **RF-03** (Carga Horária Limite Mínimo 15h) | R-03 (Limite inferior) | CT-013 | EX-013 | Nenhum | Conforme / Aprovado |
| **RF-03** (Carga Horária Inválida 14h) | R-03 (Limite inválido) | CT-014 | EX-014 | DEF-02 (Corrigido) | Conforme / Aprovado após reteste |
| **RF-03** (Carga Horária Limite Máximo 400h) | R-03 (Limite superior) | CT-015 | EX-015 | Nenhum | Conforme / Aprovado |
| **RF-03** (Carga Horária Excedida 401h) | R-03 (Limite superior) | CT-016 | EX-016 | Nenhum | Conforme / Aprovado |
| **RF-03** (Código de Disciplina Duplicado) | R-04 (Duplicidade cadastral) | CT-017 | EX-017 | Nenhum | Conforme / Aprovado |
| **RF-03** (Proteção contra Órfãos na Exclusão) | R-05 (Integridade referencial) | CT-018 | EX-018 | Nenhum | Conforme / Aprovado |
| **RF-04** (Criação de Tarefa Válida) | R-07 (Inconsistência de prazos) | CT-019 | EX-019 | Nenhum | Conforme / Aprovado |
| **RF-04** (Título Curto de Tarefa) | R-03 (Título inválido) | CT-020 | EX-020 | Nenhum | Conforme / Aprovado |
| **RF-04** (Data Limite Obrigatória) | R-07 (Data nula) | CT-021 | EX-021 | Nenhum | Conforme / Aprovado |
| **RF-05** (Atualização de Status e Taxa) | R-06 (Cálculo de progresso) | CT-022 | EX-022 | Nenhum | Conforme / Aprovado |
| **RF-06** (Filtro Combinado Status/Prioridade) | R-08 (Lentidão/erro de busca) | CT-023 | EX-023 | Nenhum | Conforme / Aprovado |
| **RF-06** (Busca Textual Inexistente) | R-08 (Tratamento de vazio) | CT-024 | EX-024 | Nenhum | Conforme / Aprovado |

---

## Complemento da revisão e cobertura demonstrada

Os vínculos históricos acima são preservados. Abaixo estão as verificações executáveis da revisão, incluindo os dois requisitos não funcionais.

| Requisito | Riscos | Verificação executada | Evidência |
|---|---|---|---|
| RF-01 | R-01, R-03 | CT-001 a CT-006; validações unitárias; hash após cadastro | CT-001 a CT-006 HTML/JSON; testes.xml |
| RF-02 | R-02 | CT-007 a CT-010; sessão API; isolamento entre usuários | CT-007 a CT-010 HTML/JSON; testes.xml; E2E-01 |
| RF-03 | R-03, R-04, R-05 | CT-011 a CT-018; limites, duplicidade e exclusão protegida | CT-011 a CT-018 HTML/JSON; testes.xml; E2E-02 |
| RF-04 | R-07 | CT-019 a CT-021; datas inválidas; fronteiras de urgência | CT-019 a CT-021 HTML/JSON; testes.xml; E2E-03 |
| RF-05 | R-06 | CT-022; taxa exata; inconsistência total zero | CT-022 HTML/JSON; testes.xml; E2E-04; red/green/refactor.xml |
| RF-06 | R-03, R-08 | CT-023/024; tabela de decisão dos filtros | CT-023/024 HTML/JSON; testes.xml |
| RNF-01 | R-08 | 30 requisições HTTP por rota, após aquecimento | latencias_http.csv; desempenho.json |
| RNF-02 | R-01 | Cadastro, consulta do hash e check_password_hash | test_rnf02_password_hash_and_login; testes.xml |

Cobertura por requisito: 8/8 com verificação executada. Cobertura por risco: R-01 a R-08 com vínculo explícito.
Isso não significa cobertura de todos os caminhos possíveis. A cobertura de linhas é medida separadamente em `cobertura.json`.
Cada CT-NNN tem reexecução atual em `05_EXECUCAO_MANUAL/evidencias_reexecucao/CT-NNN.json`.
