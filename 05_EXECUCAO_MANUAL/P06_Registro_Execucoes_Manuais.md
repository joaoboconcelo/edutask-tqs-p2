> **Nota da revisão de 11/11/2026:** os registros de outubro abaixo são relatos históricos do grupo, sem capturas contemporâneas ou issues externas disponibilizadas. A reexecução atual comprova o comportamento da versão revisada, mas não comprova as datas nem o ciclo original de defeitos.

# PRODUTO P06 - REGISTRO DE EXECUÇÕES MANUAIS (APÊNDICE F)
**Projeto:** EduTask Web v1.0.0-p2
**Disciplina:** Testes e Qualidade de Software | **UNISAGRADO 2026**
**Responsável pelas Execuções:** Lucas Braga (com apoio de Gabriel Moreira e João Lucas Boconcelo)
**Ambiente de Teste:** Localhost (`http://127.0.0.1:5000`), Python 3.13, Navegador Chrome v131 e Edge v131.

---

## Tabela Consolidada de Execuções Manuais (EX-001 a EX-024)

| Execução | Caso | Data / Versão | Resultado | Evidência Observada / Registrada | Defeito Vinculado |
| :---: | :---: | :---: | :---: | :--- | :---: |
| **EX-001** | CT-001 | 24/10/2026 v1.0.0 | **Aprovado** | Formulário submetido. Usuário criado no banco. Mensagem "Cadastro realizado com sucesso!" exibida na tela `/login`. | Nenhum |
| **EX-002** | CT-002 | 24/10/2026 v1.0.0 | **Aprovado** | Submissão com e-mail sem `@`. Alerta vermelho exibido: "Formato de e-mail inválido.". Nenhuma gravação no banco. | Nenhum |
| **EX-003** | CT-003 | 24/10/2026 v1.0.0 | **Aprovado** | Senha `Abc@123` (7 chars). Alerta: "A senha deve conter no mínimo 8 caracteres.". Bloqueio verificado. | Nenhum |
| **EX-004** | CT-004 | 24/10/2026 v1.0.0 | **Reprovado** *(Ciclo 1)*<br>**Aprovado** *(Reteste)* | *Ciclo 1:* Formulário aceitou senha sem caractere especial no endpoint direto.<br>*Reteste:* Validação ajustada em `task_service.py`. Erro exibido corretamente. | **DEF-01** |
| **EX-005** | CT-005 | 24/10/2026 v1.0.0 | **Aprovado** | Tentativa de recadastrar `aluno@unisagrado.edu.br`. Alerta: "Este e-mail já está cadastrado no sistema.". | Nenhum |
| **EX-006** | CT-006 | 24/10/2026 v1.0.0 | **Aprovado** | Senhas divergentes digitadas. Alerta: "As senhas digitadas não coincidem.". | Nenhum |
| **EX-007** | CT-007 | 24/10/2026 v1.0.0 | **Aprovado** | Login com `aluno@unisagrado.edu.br` e `Senha@123`. Sessão criada, redirecionamento para `/` com saudação no cabeçalho. | Nenhum |
| **EX-008** | CT-008 | 24/10/2026 v1.0.0 | **Aprovado** | Senha incorreta. Alerta: "Credenciais inválidas. Verifique seu e-mail e senha.". Sessão não autorizada. | Nenhum |
| **EX-009** | CT-009 | 24/10/2026 v1.0.0 | **Aprovado** | E-mail inexistente. Mesma mensagem genérica sem vazamento de existência do usuário. | Nenhum |
| **EX-010** | CT-010 | 24/10/2026 v1.0.0 | **Aprovado** | URL direta `/tarefas` em modo anônimo. Redirecionamento 302 forçado para `/login` com aviso de necessidade de login. | Nenhum |
| **EX-011** | CT-011 | 24/10/2026 v1.0.0 | **Aprovado** | Cadastro de `CC-ES03` (80h). Disciplina salva e renderizada na tabela `/disciplinas`. | Nenhum |
| **EX-012** | CT-012 | 24/10/2026 v1.0.0 | **Aprovado** | Código sem hífen (`CODIGOERRADO`). Mensagem de validação do formato regex disparada. | Nenhum |
| **EX-013** | CT-013 | 24/10/2026 v1.0.0 | **Aprovado** | Carga horária de 15h. Disciplina `CC-TOP15` salva com sucesso no limite inferior válido. | Nenhum |
| **EX-014** | CT-014 | 24/10/2026 v1.0.0 | **Reprovado** *(Ciclo 1)*<br>**Aprovado** *(Reteste)* | *Ciclo 1:* Carga horária de 14h passou sem conferência no cast inicial.<br>*Reteste:* Implementada função `validate_workload()`. Alerta exibido com sucesso. | **DEF-02** |
| **EX-015** | CT-015 | 24/10/2026 v1.0.0 | **Aprovado** | Carga horária de 400h. Registro `CC-EST400` persistido no limite superior válido. | Nenhum |
| **EX-016** | CT-016 | 24/10/2026 v1.0.0 | **Aprovado** | Carga horária de 401h. Bloqueio exibindo alerta de carga permitida entre 15h e 400h. | Nenhum |
| **EX-017** | CT-017 | 24/10/2026 v1.0.0 | **Aprovado** | Código duplicado `CC-TQS01`. Alerta: "Já existe uma disciplina cadastrada com o código CC-TQS01.". | Nenhum |
| **EX-018** | CT-018 | 24/10/2026 v1.0.0 | **Aprovado** | Tentativa de exclusão de `CC-TQS01` com tarefas. Bloqueio efetivo informando vínculo ativo. | Nenhum |
| **EX-019** | CT-019 | 24/10/2026 v1.0.0 | **Aprovado** | Tarefa criada com prazo futuro e prioridade Alta. Status inicial "Pendente" atribuído no banco. | Nenhum |
| **EX-020** | CT-020 | 24/10/2026 v1.0.0 | **Aprovado** | Título de 2 caracteres (`AB`). Mensagem: "O título da tarefa deve ter no mínimo 3 caracteres.". | Nenhum |
| **EX-021** | CT-021 | 24/10/2026 v1.0.0 | **Aprovado** | Data limite omitida. Bloqueio de campo obrigatório acionado na tela e no backend. | Nenhum |
| **EX-022** | CT-022 | 24/10/2026 v1.0.0 | **Aprovado** | Mudança de status para "Concluída". Verificação no Dashboard: taxa de conclusão subiu conforme esperado. | Nenhum |
| **EX-023** | CT-023 | 24/10/2026 v1.0.0 | **Aprovado** | Filtro "Pendente" + "Alta". Apenas as atividades que atendem a ambos os filtros são listadas. | Nenhum |
| **EX-024** | CT-024 | 24/10/2026 v1.0.0 | **Aprovado** | Busca por string inexistente. Exibição da mensagem "Nenhuma atividade encontrada...". | Nenhum |

---

### Conclusão das Execuções Manuais:
* **Total Executado:** 24 casos (100% dos planejados).
* **Aprovados no 1º ciclo:** 22 casos (91,67%).
* **Reprovados no 1º ciclo:** 2 casos (8,33%) — DEF-01 e DEF-02.
* **Aprovados após correção e reteste:** 24 casos (100% dos casos em conformidade).
