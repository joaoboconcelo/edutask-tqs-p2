# PRODUTO P04 - CATÁLOGO DE CASOS DE TESTE (APÊNDICE E)
**Projeto:** EduTask Web v1.0.1-p2
**Disciplina:** Testes e Qualidade de Software | **UNISAGRADO 2026**
**Docente:** Prof. Dr. Elvio Gilberto da Silva
**Equipe:** Gabriel Henrique Moreira, João Lucas de Antonio Boconcelo, Lucas Braga

---

### Resumo das Técnicas Aplicadas
O catálogo contém **24 casos de teste manuais** estruturados de forma independente e reproduzível, abrangendo:
* **Técnicas:** Particionamento de Equivalência (EP), Análise de Valor Limite (BVA), Tabela de Decisão (TD) e Teste de Transição de Estados (ST).
* **Cenários:** Casos positivos, negativos, de limite, de exceção e fluxos alternativos.
* **Rastreabilidade:** Cada caso está vinculado diretamente a um requisito funcional (RF) ou não funcional (RNF) e a um risco identificado (R).

---

## Casos de Teste Detalhados (CT-001 a CT-024)

### CT-001: Cadastro de usuário com dados válidos e senha forte
* **Requisito Relacionado:** RF-01 | **Risco:** R-03
* **Nível/Tipo:** Sistema / Funcional Positivo
* **Técnica Aplicada:** Particionamento de Equivalência (Classe Válida)
* **Prioridade:** Alta
* **Pré-condições:** O sistema está rodando e a página de registro `/register` está aberta. O e-mail informado não deve existir no banco.
* **Dados de Entrada:** Nome: "Carlos Silva", E-mail: "carlos.silva@unisagrado.edu.br", Senha: "SenhaForte@2026", Confirmar: "SenhaForte@2026"
* **Passos Numerados:**
  1. Acessar a tela `/register`.
  2. Preencher os campos Nome, E-mail, Senha e Confirmar Senha com os dados de entrada.
  3. Clicar no botão "Cadastrar".
* **Resultado Esperado:** O sistema grava o usuário no banco de dados, exibe a mensagem de sucesso "Cadastro realizado com sucesso! Efetue login para continuar." e redireciona para `/login`.
* **Candidato à Automação:** Sim (Fluxo crítico e repetitivo em testes de regressão).
* **Responsável:** Lucas Braga

---

### CT-002: Cadastro de usuário com e-mail em formato inválido
* **Requisito Relacionado:** RF-01 | **Risco:** R-03
* **Nível/Tipo:** Sistema / Funcional Negativo
* **Técnica Aplicada:** Particionamento de Equivalência (Classe Inválida)
* **Prioridade:** Alta
* **Pré-condições:** Página `/register` aberta.
* **Dados de Entrada:** Nome: "Teste Invalido", E-mail: "email_sem_arroba.com", Senha: "SenhaForte@2026", Confirmar: "SenhaForte@2026"
* **Passos Numerados:**
  1. Acessar `/register`.
  2. Preencher os campos com o e-mail malformado.
  3. Clicar no botão "Cadastrar".
* **Resultado Esperado:** O sistema rejeita o cadastro, permanece na página de registro e exibe a mensagem de alerta "Formato de e-mail inválido.".
* **Candidato à Automação:** Sim (Validação unitária e de interface).
* **Responsável:** Lucas Braga

---

### CT-003: Cadastro com senha de 7 caracteres (Limite inferior inválido)
* **Requisito Relacionado:** RF-01 | **Risco:** R-03
* **Nível/Tipo:** Unidade/Sistema / Limite Negativo
* **Técnica Aplicada:** Análise de Valor Limite (BVA - Valor imediatamente abaixo do mínimo de 8)
* **Prioridade:** Alta
* **Pré-condições:** Página `/register` aberta.
* **Dados de Entrada:** Nome: "Usuario Limite", E-mail: "limite7@unisagrado.edu.br", Senha: "Abc@123" (7 caracteres), Confirmar: "Abc@123"
* **Passos Numerados:**
  1. Preencher os dados no formulário de cadastro com a senha de 7 caracteres.
  2. Submeter o formulário.
* **Resultado Esperado:** O sistema bloqueia a submissão e exibe o erro "A senha deve conter no mínimo 8 caracteres.".
* **Candidato à Automação:** Sim (Coberto por teste unitário em `validate_password_strength`).
* **Responsável:** João Lucas de Antonio Boconcelo

---

### CT-004: Cadastro com senha sem caractere especial
* **Requisito Relacionado:** RF-01 | **Risco:** R-03
* **Nível/Tipo:** Sistema / Funcional Negativo
* **Técnica Aplicada:** Particionamento de Equivalência (Critério de complexidade ausente)
* **Prioridade:** Média
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** Nome: "Usuario Sem Especial", E-mail: "semespecial@unisagrado.edu.br", Senha: "SenhaForte2026", Confirmar: "SenhaForte2026"
* **Passos Numerados:**
  1. Preencher os dados com a senha contendo maiúsculas, minúsculas e números, porém sem caracteres especiais.
  2. Clicar em "Cadastrar".
* **Resultado Esperado:** O sistema rejeita o cadastro exibindo a mensagem "A senha deve conter pelo menos um caractere especial (@$!%*?&#...).".
* **Candidato à Automação:** Sim.
* **Responsável:** Lucas Braga

---

### CT-005: Cadastro com e-mail já existente no banco de dados
* **Requisito Relacionado:** RF-01 | **Risco:** R-03
* **Nível/Tipo:** Sistema / Exceção
* **Técnica Aplicada:** Particionamento de Equivalência (Restrição de unicidade)
* **Prioridade:** Alta
* **Pré-condições:** O e-mail `aluno@unisagrado.edu.br` já deve estar registrado no banco.
* **Dados de Entrada:** Nome: "Novo Aluno", E-mail: "aluno@unisagrado.edu.br", Senha: "SenhaForte@2026", Confirmar: "SenhaForte@2026"
* **Passos Numerados:**
  1. Acessar `/register`.
  2. Informar o e-mail institucional duplicado.
  3. Clicar em "Cadastrar".
* **Resultado Esperado:** O sistema não realiza nova inserção e exibe a mensagem de aviso "Este e-mail já está cadastrado no sistema.".
* **Candidato à Automação:** Sim.
* **Responsável:** Gabriel Henrique Moreira

---

### CT-006: Cadastro com senhas divergentes na confirmação
* **Requisito Relacionado:** RF-01 | **Risco:** R-03
* **Nível/Tipo:** Sistema / Funcional Alternativo Negativo
* **Técnica Aplicada:** Particionamento de Equivalência
* **Prioridade:** Média
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** Nome: "Usuario Divergente", E-mail: "divergente@unisagrado.edu.br", Senha: "SenhaForte@1", Confirmar: "SenhaForte@2"
* **Passos Numerados:**
  1. Informar senhas diferentes nos dois campos.
  2. Submeter formulário.
* **Resultado Esperado:** O sistema recusa o cadastro informando "As senhas digitadas não coincidem.".
* **Candidato à Automação:** Sim.
* **Responsável:** Lucas Braga

---

### CT-007: Autenticação de usuário com credenciais válidas
* **Requisito Relacionado:** RF-02 | **Risco:** R-02
* **Nível/Tipo:** Sistema / Funcional Positivo
* **Técnica Aplicada:** Fluxo Principal (Caminho Feliz)
* **Prioridade:** Alta
* **Pré-condições:** Usuário `aluno@unisagrado.edu.br` ativo com senha `Senha@123`.
* **Dados de Entrada:** E-mail: "aluno@unisagrado.edu.br", Senha: "Senha@123"
* **Passos Numerados:**
  1. Acessar a tela de login `/login`.
  2. Informar e-mail e senha cadastrados.
  3. Clicar em "Entrar".
* **Resultado Esperado:** A sessão é criada com sucesso, o usuário é redirecionado ao Dashboard (`/`) e visualiza a mensagem de boas-vindas com o seu nome e opções da barra de navegação.
* **Candidato à Automação:** Sim (Automatizado com Selenium e API).
* **Responsável:** João Lucas de Antonio Boconcelo

---

### CT-008: Autenticação com senha incorreta
* **Requisito Relacionado:** RF-02 | **Risco:** R-02
* **Nível/Tipo:** Sistema / Funcional Negativo
* **Técnica Aplicada:** Particionamento de Equivalência
* **Prioridade:** Alta
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** E-mail: "aluno@unisagrado.edu.br", Senha: "SenhaIncorreta@99"
* **Passos Numerados:**
  1. Acessar `/login`.
  2. Informar a senha errada.
  3. Clicar em "Entrar".
* **Resultado Esperado:** O sistema rejeita o acesso e apresenta "Credenciais inválidas. Verifique seu e-mail e senha.". O usuário permanece em `/login`.
* **Candidato à Automação:** Sim.
* **Responsável:** Lucas Braga

---

### CT-009: Autenticação com e-mail não existente
* **Requisito Relacionado:** RF-02 | **Risco:** R-02
* **Nível/Tipo:** Sistema / Funcional Negativo
* **Técnica Aplicada:** Particionamento de Equivalência
* **Prioridade:** Média
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** E-mail: "fantasma@unisagrado.edu.br", Senha: "QualquerSenha@123"
* **Passos Numerados:**
  1. Informar e-mail não cadastrado.
  2. Clicar em "Entrar".
* **Resultado Esperado:** O sistema apresenta a mensagem genérica "Credenciais inválidas. Verifique seu e-mail e senha.", sem revelar se o e-mail existe ou não.
* **Candidato à Automação:** Sim.
* **Responsável:** Lucas Braga

---

### CT-010: Tentativa de acesso direto a rotas restritas sem sessão autenticada
* **Requisito Relacionado:** RF-02, RNF-02 | **Risco:** R-02
* **Nível/Tipo:** Segurança / Sistema
* **Técnica Aplicada:** Teste de Controle de Acesso / Exceção
* **Prioridade:** Alta
* **Pré-condições:** O navegador deve estar sem cookies de sessão (modo anônimo ou após logout).
* **Dados de Entrada:** URL direta: `http://127.0.0.1:5000/tarefas`
* **Passos Numerados:**
  1. Abrir navegador em janela anônima.
  2. Digitar diretamente a URL `/tarefas` na barra de endereços e pressionar Enter.
* **Resultado Esperado:** O sistema intercepta o acesso não autenticado, impede a visualização da tela de tarefas e redireciona o usuário para `/login` com a mensagem "Faça login para acessar suas tarefas.".
* **Candidato à Automação:** Sim (Coberto em teste de integração/API e Selenium).
* **Responsável:** João Lucas de Antonio Boconcelo

---

### CT-011: Cadastro de disciplina com dados válidos e código padrão
* **Requisito Relacionado:** RF-03 | **Risco:** R-04
* **Nível/Tipo:** Sistema / Funcional Positivo
* **Técnica Aplicada:** Particionamento de Equivalência (Classe Válida)
* **Prioridade:** Alta
* **Pré-condições:** Usuário autenticado.
* **Dados de Entrada:** Código: "CC-ES03", Nome: "Engenharia de Software", Professor: "Profa. Dra. Maria Cristina", Carga Horária: 80
* **Passos Numerados:**
  1. Acessar o menu "Disciplinas" e clicar em "Cadastrar Nova Disciplina".
  2. Preencher os dados informados.
  3. Clicar em "Salvar Disciplina".
* **Resultado Esperado:** O registro é inserido no banco, o sistema redireciona para a lista `/disciplinas` com mensagem de sucesso e a nova matéria aparece listada na tabela.
* **Candidato à Automação:** Sim (Automatizado com Selenium).
* **Responsável:** João Lucas de Antonio Boconcelo

---

### CT-012: Cadastro de disciplina com código fora do padrão formatado
* **Requisito Relacionado:** RF-03 | **Risco:** R-03
* **Nível/Tipo:** Sistema / Funcional Negativo
* **Técnica Aplicada:** Particionamento de Equivalência (Expressão Regular Inválida)
* **Prioridade:** Média
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** Código: "CODIGOERRADO123", Nome: "Compiladores", Professor: "Prof. Dr. Silva", Carga Horária: 60
* **Passos Numerados:**
  1. Preencher o formulário com código sem hífen ou formato irregular.
  2. Clicar em "Salvar Disciplina".
* **Resultado Esperado:** O sistema rejeita o cadastro e informa: "Código de disciplina inválido. Formato esperado: CC-TQS01, ENG-101 (2 a 4 letras, hífen e 2 a 6 alfanuméricos).".
* **Candidato à Automação:** Sim (Unitário e Sistema).
* **Responsável:** Lucas Braga

---

### CT-013: Cadastro de disciplina com carga horária no limite inferior válido (15h)
* **Requisito Relacionado:** RF-03 | **Risco:** R-03
* **Nível/Tipo:** Sistema / Limite Positivo
* **Técnica Aplicada:** Análise de Valor Limite (BVA - Limite Mínimo Permitido)
* **Prioridade:** Média
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** Código: "CC-TOP15", Nome: "Tópicos Especiais I", Professor: "Prof. Especialista", Carga Horária: 15
* **Passos Numerados:**
  1. Preencher o formulário informando exatamente 15 horas de carga horária.
  2. Submeter formulário.
* **Resultado Esperado:** A disciplina é cadastrada com sucesso com carga horária registrada de 15h.
* **Candidato à Automação:** Sim.
* **Responsável:** João Lucas de Antonio Boconcelo

---

### CT-014: Cadastro de disciplina com carga horária abaixo do limite mínimo (14h)
* **Requisito Relacionado:** RF-03 | **Risco:** R-03
* **Nível/Tipo:** Sistema / Limite Negativo
* **Técnica Aplicada:** Análise de Valor Limite (BVA - Valor imediatamente abaixo do mínimo permitido)
* **Prioridade:** Média
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** Código: "CC-SUB14", Nome: "Seminário Curto", Professor: "Prof. Teste", Carga Horária: 14
* **Passos Numerados:**
  1. Preencher o formulário com 14 horas.
  2. Submeter formulário.
* **Resultado Esperado:** O cadastro é bloqueado com a mensagem "A carga horária deve ser um valor numérico entre 15 e 400 horas.".
* **Candidato à Automação:** Sim.
* **Responsável:** Lucas Braga

---

### CT-015: Cadastro de disciplina com carga horária no limite superior válido (400h)
* **Requisito Relacionado:** RF-03 | **Risco:** R-03
* **Nível/Tipo:** Sistema / Limite Positivo
* **Técnica Aplicada:** Análise de Valor Limite (BVA - Limite Máximo Permitido)
* **Prioridade:** Média
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** Código: "CC-EST400", Nome: "Estágio Supervisionado", Professor: "Prof. Coordenador", Carga Horária: 400
* **Passos Numerados:**
  1. Preencher com exatamente 400 horas.
  2. Submeter formulário.
* **Resultado Esperado:** Cadastro concluído com sucesso e exibido com 400h na listagem.
* **Candidato à Automação:** Sim.
* **Responsável:** João Lucas de Antonio Boconcelo

---

### CT-016: Cadastro de disciplina com carga horária acima do limite máximo (401h)
* **Requisito Relacionado:** RF-03 | **Risco:** R-03
* **Nível/Tipo:** Sistema / Limite Negativo
* **Técnica Aplicada:** Análise de Valor Limite (BVA - Valor imediatamente acima do máximo permitido)
* **Prioridade:** Média
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** Código: "CC-EXT401", Nome: "Matéria Extensa", Professor: "Prof. Teste", Carga Horária: 401
* **Passos Numerados:**
  1. Preencher o formulário com 401 horas.
  2. Submeter formulário.
* **Resultado Esperado:** O sistema bloqueia a gravação e apresenta o erro de faixa válida entre 15 e 400 horas.
* **Candidato à Automação:** Sim.
* **Responsável:** Lucas Braga

---

### CT-017: Tentativa de cadastrar disciplina com código duplicado
* **Requisito Relacionado:** RF-03 | **Risco:** R-04
* **Nível/Tipo:** Sistema / Exceção
* **Técnica Aplicada:** Particionamento de Equivalência (Restrição de Chave Única)
* **Prioridade:** Alta
* **Pré-condições:** Disciplina com código `CC-TQS01` já existente no banco de dados.
* **Dados de Entrada:** Código: "CC-TQS01", Nome: "Segunda Turma TQS", Professor: "Outro Docente", Carga Horária: 80
* **Passos Numerados:**
  1. Acessar `/disciplinas/nova`.
  2. Inserir o código `CC-TQS01` já existente.
  3. Clicar em "Salvar Disciplina".
* **Resultado Esperado:** O sistema bloqueia a duplicidade e emite o aviso "Já existe uma disciplina cadastrada com o código CC-TQS01.".
* **Candidato à Automação:** Sim.
* **Responsável:** Gabriel Henrique Moreira

---

### CT-018: Tentativa de exclusão de disciplina com tarefas vinculadas
* **Requisito Relacionado:** RF-03 | **Risco:** R-05
* **Nível/Tipo:** Sistema / Integridade Relacional e Exceção
* **Técnica Aplicada:** Validação de Regra de Negócio / Integridade Estrutural
* **Prioridade:** Alta
* **Pré-condições:** A disciplina `CC-TQS01` possui atividades acadêmicas cadastradas e associadas a ela.
* **Passos Numerados:**
  1. Acessar a lista `/disciplinas`.
  2. Localizar a linha da disciplina `CC-TQS01`.
  3. Clicar no botão "Excluir" e confirmar o modal.
* **Resultado Esperado:** O sistema impede a exclusão para não gerar registros órfãos e exibe o alerta "Não é possível excluir disciplina que possui tarefas vinculadas.".
* **Candidato à Automação:** Sim.
* **Responsável:** Gabriel Henrique Moreira

---

### CT-019: Criação de atividade com dados válidos e data futura
* **Requisito Relacionado:** RF-04 | **Risco:** R-07
* **Nível/Tipo:** Sistema / Funcional Positivo
* **Técnica Aplicada:** Fluxo Principal (Caminho Feliz)
* **Prioridade:** Alta
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** Título: "Implementação do Pipeline CI/CD", Descrição: "Configurar actions para build e testes automáticos", Prazo: "2026-12-10", Prioridade: "Alta", Disciplina: `CC-TQS01`
* **Passos Numerados:**
  1. Acessar "Tarefas" -> "Cadastrar Nova Tarefa".
  2. Preencher título, descrição, selecionar disciplina, prioridade Alta e data limite.
  3. Clicar em "Salvar Atividade".
* **Resultado Esperado:** A tarefa é registrada com sucesso com status inicial "Pendente", nível de urgência calculado automaticamente e exibida na listagem.
* **Candidato à Automação:** Sim (Automatizado com Selenium).
* **Responsável:** João Lucas de Antonio Boconcelo

---

### CT-020: Criação de atividade com título de 2 caracteres (Limite inferior inválido)
* **Requisito Relacionado:** RF-04 | **Risco:** R-03
* **Nível/Tipo:** Sistema / Limite Negativo
* **Técnica Aplicada:** Análise de Valor Limite (BVA - Valor abaixo do mínimo de 3 caracteres)
* **Prioridade:** Média
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** Título: "AB" (2 caracteres), Prazo: "2026-11-30", Disciplina: Selecionada
* **Passos Numerados:**
  1. Informar título com apenas 2 caracteres.
  2. Clicar em "Salvar Atividade".
* **Resultado Esperado:** O sistema barra a operação e exibe "O título da tarefa deve ter no mínimo 3 caracteres.".
* **Candidato à Automação:** Sim.
* **Responsável:** Lucas Braga

---

### CT-021: Criação de atividade sem informar data limite de entrega
* **Requisito Relacionado:** RF-04 | **Risco:** R-07
* **Nível/Tipo:** Sistema / Funcional Negativo
* **Técnica Aplicada:** Particionamento de Equivalência (Campo Obrigatório Ausente)
* **Prioridade:** Alta
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** Título: "Atividade Sem Data", Prazo: Vazio `""`, Disciplina: Selecionada
* **Passos Numerados:**
  1. Preencher título e disciplina, deixando o campo de data vazio.
  2. Submeter formulário.
* **Resultado Esperado:** O sistema exige o preenchimento da data limite informando "A data limite de entrega é obrigatória.".
* **Candidato à Automação:** Sim.
* **Responsável:** Lucas Braga

---

### CT-022: Atualização de status da tarefa e recálculo da taxa de conclusão no Dashboard
* **Requisito Relacionado:** RF-05, R-06 | **Risco:** R-06
* **Nível/Tipo:** Sistema / Transição de Estados
* **Técnica Aplicada:** Teste de Transição de Estados (Pendente -> Concluída)
* **Prioridade:** Alta
* **Pré-condições:** Uma tarefa está em estado "Pendente" e a taxa de conclusão atual está visível no Dashboard.
* **Passos Numerados:**
  1. Acessar a tela de `/tarefas`.
  2. Localizar a tarefa, selecionar a opção "Concluída" no dropdown de status e clicar no botão salvar.
  3. Navegar até o Dashboard (`/`).
* **Resultado Esperado:** O status da tarefa muda para "Concluída", a contagem de tarefas concluídas aumenta em +1 e a barra de progresso exibe a nova taxa percentual calculada corretamente.
* **Candidato à Automação:** Sim (Automatizado com Selenium).
* **Responsável:** João Lucas de Antonio Boconcelo

---

### CT-023: Filtragem combinada por status "Pendente" e prioridade "Alta"
* **Requisito Relacionado:** RF-06 | **Risco:** R-08
* **Nível/Tipo:** Sistema / Tabela de Decisão
* **Técnica Aplicada:** Tabela de Decisão (Combinação de Filtros)
* **Prioridade:** Média
* **Pré-condições:** Existem tarefas com diferentes status e prioridades cadastradas.
* **Passos Numerados:**
  1. Acessar `/tarefas`.
  2. No filtro de Status selecionar "Pendente".
  3. No filtro de Prioridade selecionar "Alta".
  4. Clicar no botão "Filtrar".
* **Resultado Esperado:** Todas as tarefas exibidas na tabela devem obrigatoriamente possuir status "Pendente" E prioridade "Alta". Nenhuma tarefa concluída ou de baixa prioridade deve aparecer.
* **Candidato à Automação:** Sim.
* **Responsável:** Gabriel Henrique Moreira

---

### CT-024: Busca textual por termo inexistente
* **Requisito Relacionado:** RF-06 | **Risco:** R-08
* **Nível/Tipo:** Sistema / Funcional Alternativo
* **Técnica Aplicada:** Particionamento de Equivalência (Busca sem correspondência)
* **Prioridade:** Baixa
* **Pré-condições:** Aplicação e banco fictício inicializados; para CT-011 em diante, usuário de demonstração autenticado. Restabelecer a base entre cenários.
* **Dados de Entrada:** Termo de busca: `XYZ999TERMOINEXISTENTE`
* **Passos Numerados:**
  1. Digitar o termo inexistente no campo "Buscar por Palavra-Chave".
  2. Clicar em "Filtrar".
* **Resultado Esperado:** A tabela não deve quebrar nem disparar erro 500; deve exibir uma linha informativa com a mensagem amigável: "Nenhuma atividade encontrada para os critérios selecionados.".
* **Candidato à Automação:** Sim.
* **Responsável:** Lucas Braga
