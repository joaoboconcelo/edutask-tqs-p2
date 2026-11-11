# PRODUTO P02 - DOCUMENTO DE REQUISITOS, ESCOPO E RISCOS
**Projeto:** EduTask Web v1.0.1-p2
**Disciplina:** Testes e Qualidade de Software | **UNISAGRADO 2026**
**Docente:** Prof. Dr. Elvio Gilberto da Silva
**Equipe:** Gabriel Henrique Moreira, João Lucas de Antonio Boconcelo, Lucas Braga

---

## 1. Delimitação do Escopo

### 1.1 Escopo Incluído
O escopo do projeto contempla os seguintes módulos e funcionalidades do sistema **EduTask Web**:
* **Módulo de Autenticação e Usuários:** Cadastro de novos estudantes, validação de políticas de senha forte e formato de e-mail institucional, login com criação de sessão autenticada e logout.
* **Módulo de Gestão de Disciplinas:** Cadastro, consulta e exclusão de disciplinas com regras de código formatado (ex: `CC-TQS01`), professor responsável e validação de carga horária entre 15h e 400h.
* **Módulo de Gestão de Tarefas Acadêmicas:** Criação, edição, exclusão e alteração de status (`Pendente`, `Em Andamento`, `Concluída`) de atividades, com associação a disciplinas, prioridade (`Baixa`, `Média`, `Alta`) e data limite.
* **Módulo de Urgência e Prazos:** Cálculo automatizado do nível de urgência (`Crítica/Em Atraso`, `Alta`, `Média`, `Normal`) com base na proximidade da data limite.
* **Módulo de Dashboard e Filtros:** Painel com taxa percentual de conclusão de tarefas e filtros dinâmicos combinados por status, prioridade e pesquisa textual.
* **Módulo de API RESTful:** Endpoints JSON para autenticação, manipulação de disciplinas e tarefas, e extração de métricas de uso.

### 1.2 Escopo Excluído (Fora do Escopo)
Para garantir a viabilidade e foco na qualidade, ficam expressamente fora do escopo:
* Integração com sistemas de pagamentos de mensalidades acadêmicas.
* Envio real de e-mails via servidor SMTP externo (simulado via interface).
* Suporte a múltiplos idiomas (sistema exclusivamente em português do Brasil).
* Módulo de fórum ou chat em tempo real entre alunos.
* Aplicativo mobile nativo (iOS / Android).

---

## 2. Catálogo Oficial de Requisitos (Apêndice B)

| ID | Descrição Verificável | Tipo | Prioridade | Critério de Aceitação (BDD / Gherkin) |
| :---: | :--- | :---: | :---: | :--- |
| **RF-01** | O sistema deve permitir o cadastro de novos usuários com nome, e-mail válido e senha segura (mínimo 8 caracteres, 1 maiúscula, 1 número e 1 caractere especial). | Funcional | Alta | **Dado** que o usuário preenche o formulário de cadastro com dados válidos e senha forte,<br>**Quando** submeter o formulário,<br>**Então** o sistema grava o usuário com senha criptografada e redireciona para a tela de login com mensagem de sucesso. |
| **RF-02** | O sistema deve autenticar o usuário validando as credenciais cadastradas e impedindo o acesso a páginas privadas sem sessão ativa. | Funcional | Alta | **Dado** que o usuário informa e-mail e senha cadastrados,<br>**Quando** clicar em "Entrar",<br>**Então** o sistema inicia a sessão de navegação e exibe o Dashboard principal. Caso as credenciais estejam incorretas, exibe mensagem de erro sem expor detalhes internos. |
| **RF-03** | O sistema deve permitir o cadastro de disciplinas com código único formatado (`[A-Z]{2,4}-[A-Z0-9]{2,6}`) e carga horária entre 15h e 400h. | Funcional | Alta | **Dado** que o usuário preenche código da disciplina no formato válido e carga horária entre 15h e 400h,<br>**Quando** salvar a disciplina,<br>**Então** o sistema insere o registro no banco. Se o código já existir, rejeita a inserção informando duplicidade. |
| **RF-04** | O sistema deve permitir a criação de atividades acadêmicas vinculadas a uma disciplina existente, exigindo título, data limite de entrega e prioridade. | Funcional | Alta | **Dado** que o usuário seleciona uma disciplina e preenche título (mín. 3 caracteres) e data limite,<br>**Quando** clicar em "Salvar Atividade",<br>**Então** a tarefa é criada com status inicial "Pendente" e listada nas consultas. |
| **RF-05** | O sistema deve permitir a atualização do status da tarefa (`Pendente`, `Em Andamento`, `Concluída`) e recalcular automaticamente a taxa percentual de conclusão no painel. | Funcional | Média | **Dado** que uma tarefa existente está com status "Pendente",<br>**Quando** o usuário alterar seu status para "Concluída",<br>**Então** a alteração é persistida e a taxa de conclusão no Dashboard é atualizada imediatamente. |
| **RF-06** | O sistema deve disponibilizar busca textual e filtros dinâmicos de tarefas combináveis por status e prioridade. | Funcional | Média | **Dado** que existem múltiplas tarefas cadastradas,<br>**Quando** o usuário selecionar o filtro de status "Pendente" e prioridade "Alta",<br>**Então** apenas as tarefas que satisfazem simultaneamente ambos os critérios devem ser exibidas. |
| **RNF-01** | **Desempenho e Tempo de Resposta:** As operações de consulta e retorno da API REST devem responder em tempo inferior a 500 milissegundos em ambiente local controlado. | Não Funcional | Alta | **Dado** que o servidor está em execução sob carga padrão de testes,<br>**Quando** for realizada uma requisição `GET /api/tarefas` ou `GET /api/metricas`,<br>**Então** o tempo de resposta medido deve ser estritamente menor que 500ms. |
| **RNF-02** | **Segurança e Proteção de Senhas:** Todas as senhas dos usuários devem ser armazenadas exclusivamente em formato de hash criptográfico seguro (scrypt ou PBKDF2-SHA256), sem jamais persistir senhas em texto puro. | Não Funcional | Alta | **Dado** que um usuário efetua seu cadastro,<br>**Quando** o registro for gravado no banco SQLite,<br>**Então** a coluna `password_hash` deve conter um hash criptográfico válido e a senha em texto puro não deve ser identificável. |

---

## 3. Matriz de Avaliação e Priorização de Riscos (Apêndice C)

| ID | Descrição do Risco | Probabilidade | Impacto | Prioridade | Resposta / Estratégia de Teste Planejada |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **R-01** | **Vazamento ou armazenamento inseguro de senhas em texto plano no banco de dados.** | Baixo | Alto | **Alta** | Teste de segurança verificando inspeção direta do banco de dados SQLite e validação do uso do algoritmo Werkzeug Security (hash scrypt ou PBKDF2/SHA256). |
| **R-02** | **Acesso indevido a rotas e dados privados sem autenticação prévia de sessão.** | Médio | Alto | **Alta** | Testes de controle de acesso acessando diretamente as URLs `/`, `/disciplinas` e `/tarefas` em modo anônimo e verificando redirecionamento forçado para `/login`. |
| **R-03** | **Injeção de códigos ou dados inconsistentes em campos de cadastro (ex: e-mails malformados e senhas fracas).** | Alto | Médio | **Alta** | Testes unitários e manuais com técnicas de Particionamento de Equivalência e Análise de Valor Limite cobrindo entradas inválidas, vazias e caracteres especiais. |
| **R-04** | **Duplicidade de códigos de disciplinas gerando ambiguidade no histórico escolar.** | Médio | Médio | **Média** | Testes funcionais e de API tentando cadastrar o mesmo código de disciplina duas vezes, validando o código de erro HTTP 409 (Conflict). |
| **R-05** | **Inconsistência de integridade referencial ao excluir disciplina que possui tarefas dependentes.** | Médio | Alto | **Alta** | Testes funcionais e de regressão tentando excluir uma disciplina com tarefas ativas, validando o bloqueio e mensagem informativa ao usuário. |
| **R-06** | **Cálculo errôneo da taxa de conclusão no Dashboard quando o total de tarefas for igual a zero (Divisão por zero).** | Médio | Alto | **Alta** | Teste unitário e de fronteira executando `calculate_completion_rate(0, 0)` garantindo retorno de 0.0% sem lançamento de exceção não tratada. |
| **R-07** | **Inconsistência no cálculo de urgência de tarefas com prazos vencidos ou datas malformadas.** | Médio | Médio | **Média** | Testes no serviço de urgência com datas no passado, hoje e futuro distante, verificando a atribuição precisa do score e nível de alerta. |
| **R-08** | **Degradação de desempenho ou lentidão nas consultas da API REST.** | Baixo | Médio | **Baixa** | Testes não-funcionais com medições repetidas de tempo de resposta em milissegundos para os endpoints principais. |
## Esclarecimentos da revisão de 11/11/2026

RF-05 continua sendo atualização de status e taxa de conclusão. O cálculo de urgência é regra complementar de RF-04, mitigando R-07: <=0 dias =100; 1-2=75; 3-7=50; >7=25. Datas vencidas são aceitas com aviso na interface. A API exige sessão, e tarefas, disciplinas e indicadores são restritos ao usuário autenticado. Códigos de disciplinas permanecem únicos globalmente. RNF-02 é atualizado nesta revisão para aceitar scrypt, padrão efetivamente usado, ou PBKDF2-SHA256; a validação dessa alteração de requisito cabe ao grupo/professor.
