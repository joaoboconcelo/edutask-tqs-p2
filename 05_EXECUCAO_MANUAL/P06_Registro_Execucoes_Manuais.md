# Registro atual de inspeção pela interface

Data: 11/11/2026. Versão: v1.0.1-p2. Ambiente: instância descartável em http://127.0.0.1:5011, SQLite separado da demonstração.
Executor: assistente de validação técnica, por solicitação do grupo. Método: navegação e preenchimento interativo dos formulários, leitura das mensagens e dos dados visíveis. Não se atribui a execução a um integrante nem se presume homologação humana.

Os 24 critérios funcionais foram atendidos. Em quatro casos, a validação nativa do navegador impediu o envio; isso está registrado sem substituir a observação pela mensagem esperada do backend.

| Execução | Caso | Resultado observado | Captura |
|---|---|---|---|
| EX-I-001 | CT-001 | Cadastro aceito e redirecionado ao login com mensagem de sucesso. | evidencias_interface/CT-001.png |
| EX-I-002 | CT-002 | O navegador bloqueou o envio: e-mail sem @. Validação nativa, anterior ao backend. | evidencias_interface/CT-002.png |
| EX-I-003 | CT-003 | Senha de sete caracteres rejeitada com mensagem específica. | evidencias_interface/CT-003.png |
| EX-I-004 | CT-004 | Senha sem símbolo rejeitada pelo backend. | evidencias_interface/CT-004.png |
| EX-I-005 | CT-005 | Cadastro duplicado rejeitado com aviso de e-mail existente. | evidencias_interface/CT-005.png |
| EX-I-006 | CT-006 | Confirmação divergente rejeitada. | evidencias_interface/CT-006.png |
| EX-I-007 | CT-007 | Login válido abriu o painel com três tarefas e taxa inicial de 33,33%. | evidencias_interface/CT-007.png |
| EX-I-008 | CT-008 | Senha incorreta rejeitada sem acesso ao painel. | evidencias_interface/CT-008.png |
| EX-I-009 | CT-009 | Usuário inexistente recebeu a mesma mensagem genérica do erro de senha. | evidencias_interface/CT-009.png |
| EX-I-010 | CT-010 | Acesso direto à rota privada redirecionou ao login. | evidencias_interface/CT-010.png |
| EX-I-011 | CT-011 | Disciplina CC-ES03 persistida e exibida com 80h. | evidencias_interface/CT-011.png |
| EX-I-012 | CT-012 | Código sem hífen rejeitado com orientação do formato. | evidencias_interface/CT-012.png |
| EX-I-013 | CT-013 | Carga mínima de 15h aceita e exibida na lista. | evidencias_interface/CT-013.png |
| EX-I-014 | CT-014 | O navegador bloqueou 14h e exibiu: O valor deve ser maior ou igual a 15. | evidencias_interface/CT-014.png |
| EX-I-015 | CT-015 | Carga máxima de 400h aceita e exibida. | evidencias_interface/CT-015.png |
| EX-I-016 | CT-016 | O navegador bloqueou 401h e exibiu: O valor deve ser menor ou igual a 400. | evidencias_interface/CT-016.png |
| EX-I-017 | CT-017 | Código CC-TQS01 duplicado rejeitado. | evidencias_interface/CT-017.png |
| EX-I-018 | CT-018 | Exclusão da disciplina CC-TQS01 bloqueada; registro permaneceu na lista. | evidencias_interface/CT-018.png |
| EX-I-019 | CT-019 | Tarefa criada com prazo 30/11/2026, prioridade Alta e status Pendente. | evidencias_interface/CT-019.png |
| EX-I-020 | CT-020 | Título AB rejeitado com mensagem de tamanho mínimo. | evidencias_interface/CT-020.png |
| EX-I-021 | CT-021 | Envio bloqueado pelo navegador porque a data obrigatória está vazia; valueMissing=true. | evidencias_interface/CT-021.png |
| EX-I-022 | CT-022 | Após concluir a tarefa, painel exibiu 2 concluídas de 4 tarefas: 50,0%. | evidencias_interface/CT-022.png |
| EX-I-023 | CT-023 | Filtro Pendente + Alta exibiu apenas o alvo; excluiu tarefas concluídas e de prioridade Média. | evidencias_interface/CT-023.png |
| EX-I-024 | CT-024 | Busca por termo inexistente exibiu estado vazio sem erro. | evidencias_interface/CT-024.png |

Cada captura tem snapshot textual e metadados JSON associados. O registro consolidado contém também os quatro cenários de aceitação técnica, cujas capturas ficam na pasta 10.
As verificações automatizadas do mesmo catálogo, com banco por cenário, ficam em evidencias_reexecucao e não são contadas como execuções humanas.
