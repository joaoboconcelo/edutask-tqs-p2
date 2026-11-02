# PRODUTO P09 - TESTES DE ACEITAÇÃO E NÃO FUNCIONAIS
**Projeto:** EduTask Web v1.0.0-p2  
**Disciplina:** Testes e Qualidade de Software | **UNISAGRADO 2026**  
**Docente:** Prof. Dr. Elvio Gilberto da Silva  
**Avaliadores / Representantes do Usuário:** Gabriel Henrique Moreira, Lucas Braga, João Lucas Boconcelo  

---

# PARTE 1: CENÁRIOS DE TESTE DE ACEITAÇÃO (UAT)

### Cenário UAT-01: Auto-cadastro e Primeiro Acesso do Estudante
* **História de Usuário:** Como estudante de Ciência da Computação, quero me cadastrar no sistema usando meu e-mail acadêmico e definir uma senha segura, para que eu possa gerenciar minhas matérias e entregas sem depender de um administrador.
* **Critério de Sucesso:** O estudante preenche seus dados, recebe confirmação imediata e consegue fazer login direto no painel principal.
* **Procedimento:**
  1. Acessar `/register`.
  2. Cadastrar novo aluno com e-mail institucional.
  3. Realizar login com as credenciais cadastradas.
* **Observações:** Interface limpa, com campos autoexplicativos e orientações claras sobre os requisitos da senha.
* **Decisão do Usuário:** **[X] Aceito** &nbsp;&nbsp;&nbsp; [ ] Aceito com ressalvas &nbsp;&nbsp;&nbsp; [ ] Não aceito

---

### Cenário UAT-02: Organização Semestral de Disciplinas Curriculares
* **História de Usuário:** Como estudante, quero cadastrar as matérias do semestre atual com código da turma e nome do professor, para manter minhas atividades organizadas por matéria.
* **Critério de Sucesso:** As matérias cadastradas aparecem organizadas em tabela com contadores de horas e opções claras de edição.
* **Procedimento:**
  1. Acessar `/disciplinas/nova`.
  2. Cadastrar a matéria "Testes e Qualidade de Software" (80h).
  3. Visualizar a lista `/disciplinas`.
* **Observações:** A tabela apresenta badges visuais modernos com o código da matéria, facilitando a identificação rápida.
* **Decisão do Usuário:** **[X] Aceito** &nbsp;&nbsp;&nbsp; [ ] Aceito com ressalvas &nbsp;&nbsp;&nbsp; [ ] Não aceito

---

### Cenário UAT-03: Planejamento de Entrega de Trabalho com Nível de Urgência
* **História de Usuário:** Como estudante com múltiplas disciplinas, quero cadastrar tarefas com datas limites e prioridades, e visualizar instantaneamente quais estão mais próximas do vencimento, para não perder prazos.
* **Critério de Sucesso:** Ao cadastrar uma atividade com data próxima, o sistema calcula e exibe automaticamente o selo visual de urgência.
* **Procedimento:**
  1. Cadastrar atividade com prazo para daqui a 2 dias.
  2. Consultar o Dashboard (`/`) e a tela de Tarefas (`/tarefas`).
* **Observações:** O selo colorido de urgência (`Alta Urgência` / `Crítica`) destacou o item imediatamente sem que o usuário precisasse fazer contas manuais de dias restantes.
* **Decisão do Usuário:** **[X] Aceito** &nbsp;&nbsp;&nbsp; [ ] Aceito com ressalvas &nbsp;&nbsp;&nbsp; [ ] Não aceito

---

### Cenário UAT-04: Acompanhamento de Progresso e Conclusão de Metas
* **História de Usuário:** Como estudante, quero marcar atividades como "Concluída" e ver a barra de progresso aumentar no painel, para ter clareza do quanto já avancei no semestre.
* **Critério de Sucesso:** Alteração imediata do status da tarefa e atualização matemática da barra percentual no Dashboard.
* **Procedimento:**
  1. Mudar o status de uma atividade pendente para "Concluída".
  2. Verificar a barra no Dashboard.
* **Observações:** Atualização em tempo real e barra com percentual verde bem legível.
* **Decisão do Usuário:** **[X] Aceito** &nbsp;&nbsp;&nbsp; [ ] Aceito com ressalvas &nbsp;&nbsp;&nbsp; [ ] Não aceito

---

# PARTE 2: REGISTRO DE TESTES NÃO FUNCIONAIS (APÊNDICE I)

### [TNF-01] Desempenho Básico: Tempo de Resposta da Consulta de Tarefas
* **ID e Categoria:** TNF-01 | Desempenho Básico
* **Objetivo:** Garantir que a renderização da lista de tarefas não cause lentidão perceptível ao usuário.
* **Ambiente:** Servidor Flask local, SQLite, navegador Chrome v131.
* **Métrica / Critério:** Tempo total de carregamento da página inferior a **300 milissegundos**.
* **Procedimento:** Executar 5 requisições sucessivas à rota `/tarefas` medindo o tempo de resposta através das ferramentas do desenvolvedor (Network tab) e script HTTP.
* **Dados e Repetições:** 5 medições: 28ms, 32ms, 25ms, 27ms, 30ms. Média: **28,4 ms**.
* **Resultado Obtido:** Média de 28,4ms (muito abaixo do teto de 300ms).
* **Conclusão:** **[X] Atende** &nbsp;&nbsp;&nbsp; [ ] Atende parcialmente &nbsp;&nbsp;&nbsp; [ ] Não atende

---

### [TNF-02] Desempenho Básico: Tempo de Resposta do Endpoint da API de Métricas
* **ID e Categoria:** TNF-02 | Desempenho Básico
* **Objetivo:** Verificar a latência da API REST para requisições de dashboard.
* **Ambiente:** Endpoint `/api/metricas` local.
* **Métrica / Critério:** Tempo de resposta inferior a **150 milissegundos**.
* **Procedimento:** Disparo de 10 chamadas consecutivas via script `test_api_integracao.py` calculando a latência de cada requisição JSON.
* **Dados e Repetições:** 10 repetições. Tempo mínimo: 12ms, Tempo máximo: 41ms. Média: **18,5 ms**.
* **Resultado Obtido:** Resposta instantânea de 18,5ms em média.
* **Conclusão:** **[X] Atende** &nbsp;&nbsp;&nbsp; [ ] Atende parcialmente &nbsp;&nbsp;&nbsp; [ ] Não atende

---

### [TNF-03] Usabilidade: Eficiência de Navegação e Regra dos Três Cliques
* **ID e Categoria:** TNF-03 | Usabilidade
* **Objetivo:** Avaliar a facilidade de acesso a qualquer operação chave do sistema em no máximo 3 cliques a partir do Dashboard.
* **Ambiente:** Interface Web desktop.
* **Métrica / Critério:** 100% dos fluxos principais acessíveis em no máximo 3 cliques.
* **Procedimento:**
  * Fluxo Dashboard -> Nova Tarefa: 1 clique (botão "+ Nova Tarefa").
  * Fluxo Dashboard -> Nova Disciplina: 1 clique.
  * Fluxo Dashboard -> Filtrar Tarefas Concluídas: 2 cliques (menu "Tarefas" -> botão "Filtrar").
* **Resultado Obtido:** Todas as rotas vitais são acessíveis em 1 ou 2 cliques.
* **Conclusão:** **[X] Atende** &nbsp;&nbsp;&nbsp; [ ] Atende parcialmente &nbsp;&nbsp;&nbsp; [ ] Não atende

---

### [TNF-04] Usabilidade: Clareza das Mensagens de Validação e Feedback
* **ID e Categoria:** TNF-04 | Usabilidade
* **Objetivo:** Assegurar que nenhuma tela falhe silenciosamente e que alertas usem código de cores coerente (Verde = Sucesso, Amarelo = Atenção, Vermelho = Erro).
* **Ambiente:** Navegadores Chrome e Edge.
* **Métrica / Critério:** Presença de caixas de alerta Bootstrap padronizadas (`role="alert"`) em todas as operações de formulário.
* **Procedimento:** Submeter intencionalmente dados errados em `/register`, `/login`, `/disciplinas/nova` e `/tarefas/nova` e inspecionar o DOM.
* **Resultado Obtido:** Todas as mensagens de erro aparecem com ícones, fundo colorido e botão de fechar (dismissible), orientando o usuário sobre a correção necessária.
* **Conclusão:** **[X] Atende** &nbsp;&nbsp;&nbsp; [ ] Atende parcialmente &nbsp;&nbsp;&nbsp; [ ] Não atende

---

### [TNF-05] Segurança Básica: Criptografia e Proteção de Senhas no Armazenamento
* **ID e Categoria:** TNF-05 | Segurança Básica
* **Objetivo:** Comprovar que senhas nunca sejam armazenadas em texto claro no banco de dados.
* **Ambiente:** Banco de dados SQLite (`edutask.db`).
* **Métrica / Critério:** A coluna `password_hash` da tabela `users` deve conter hash criptográfico seguro (PBKDF2 com salt e SHA256).
* **Procedimento:** Inspecionar o banco de dados via query SQL direta: `SELECT id, email, password_hash FROM users;`.
* **Resultado Obtido:** O registro contém hash do tipo `scrypt:32768:8:1$...` ou `pbkdf2:sha256:...`. Senha em texto plano não é armazenada nem exposta em logs.
* **Conclusão:** **[X] Atende** &nbsp;&nbsp;&nbsp; [ ] Atende parcialmente &nbsp;&nbsp;&nbsp; [ ] Não atende

---

### [TNF-06] Segurança Básica: Controle de Acesso a Rotas e Prevenção de SQL Injection
* **ID e Categoria:** TNF-06 | Segurança Básica
* **Objetivo:** Validar que rotas privadas sejam inacessíveis sem autenticação e que comandos SQL usem queries parametrizadas.
* **Ambiente:** Navegador anônimo e requisições HTTP curl/requests.
* **Métrica / Critério:** Redirecionamento 302 forçado para `/login` ao tentar abrir `/disciplinas` sem sessão; queries parametrizadas com `?` em 100% das consultas.
* **Procedimento:**
  1. Acessar `/disciplinas` sem cookies de sessão.
  2. Inserir strings de teste `' OR '1'='1` nos campos de busca e login.
* **Resultado Obtido:** Acesso bloqueado para usuários anônimos. Queries parametrizadas anularam a tentativa de injeção sem alterações na base.
* **Conclusão:** **[X] Atende** &nbsp;&nbsp;&nbsp; [ ] Atende parcialmente &nbsp;&nbsp;&nbsp; [ ] Não atende
