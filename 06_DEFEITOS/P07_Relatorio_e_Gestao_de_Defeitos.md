> **Nota da revisão de 11/11/2026:** os registros de outubro abaixo são relatos históricos do grupo, sem capturas contemporâneas ou issues externas disponibilizadas. A reexecução atual comprova o comportamento da versão revisada, mas não comprova as datas nem o ciclo original de defeitos.

# PRODUTO P07 - RELATÓRIO E GESTÃO DE DEFEITOS (APÊNDICE G)
**Projeto:** EduTask Web v1.0.0-p2
**Disciplina:** Testes e Qualidade de Software | **UNISAGRADO 2026**
**Ferramenta Adotada:** Padrão GitHub Issues
**Responsável pelo Registro e Acompanhamento:** Lucas Braga
**Responsável pela Correção (Dev):** João Lucas de Antonio Boconcelo

---

## 1. Visão Geral do Ciclo de Vida dos Defeitos
Todos os defeitos reportados seguiram o fluxo formal de estados:
`Novo` ➔ `Em Análise` ➔ `Em Correção` ➔ `Pronto para Reteste` ➔ `Encerrado`.

---

## 2. Registro Detalhado dos Defeitos

### [DEF-01] Falha de validação: Aceitação de senhas sem caracteres especiais no cadastro de alunos
* **Identificador da Issue:** #DEF-01
* **Requisito Relacionado:** RF-01 | **Caso de Teste Relacionado:** CT-004 / EX-004
* **Ambiente e Versão:** Google Chrome v131 / Windows 11 / EduTask v1.0.0 (commit inicial)
* **Severidade:** **Média** (Afeta requisitos de segurança da política de senhas)
* **Prioridade de Correção:** **Alta**
* **Status Final:** **Encerrado** (Corrigido e retestado com sucesso)
* **Responsável pelo Relato:** Lucas Braga
* **Responsável pela Correção:** João Lucas Boconcelo

#### Pré-condições:
Tela de cadastro `/register` acessível e banco de dados operacional.

#### Passos para Reproduzir:
1. Acessar `http://127.0.0.1:5000/register`.
2. Informar Nome: "Aluno Teste", E-mail: "aluno.teste@unisagrado.edu.br".
3. No campo Senha digitar: `SenhaForte2026` (contém maiúscula, minúscula e números, mas nenhum símbolo especial).
4. Confirmar a senha com o mesmo valor e clicar no botão "Cadastrar".

#### Resultado Obtido (Falha):
O sistema realizava o cadastro sem exigir o caractere especial, violando a regra de segurança especificada no RF-01.

#### Resultado Esperado:
O cadastro deve ser bloqueado e uma mensagem em vermelho deve ser exibida: "A senha deve conter pelo menos um caractere especial (@$!%*?&#...).".

#### Resolução e Reteste:
* **Ação Corretiva:** Implementada a checagem `any(c in "@$!%*?&#^_-+=." for c in password)` dentro da função `validate_password_strength()` em `task_service.py`.
* **Evidência do Reteste:** Execução do teste unitário e manual confirmando o bloqueio da senha sem caractere especial.
* **Conclusão:** Defeito corrigido e homologado.

---

### [DEF-02] Ausência de trava na carga horária inferior a 15 horas no cadastro de disciplinas
* **Identificador da Issue:** #DEF-02
* **Requisito Relacionado:** RF-03 | **Caso de Teste Relacionado:** CT-014 / EX-014
* **Ambiente e Versão:** Edge v131 / Windows 11 / EduTask v1.0.0
* **Severidade:** **Média** (Inconsistência cadastral em regras acadêmicas)
* **Prioridade de Correção:** **Média**
* **Status Final:** **Encerrado** (Corrigido e retestado com sucesso)
* **Responsável pelo Relato:** Lucas Braga
* **Responsável pela Correção:** João Lucas Boconcelo

#### Pré-condições:
Usuário autenticado com permissão de cadastro de disciplinas.

#### Passos para Reproduzir:
1. Acessar `/disciplinas/nova`.
2. Preencher Código: `CC-SUB14`, Nome: "Seminário Curto", Professor: "Prof. Teste".
3. No campo "Carga Horária Semestral" digitar o valor: `14`.
4. Clicar em "Salvar Disciplina".

#### Resultado Obtido (Falha):
A disciplina era aceita e gravada no banco com 14 horas de duração sem validação do limite inferior regulamentar.

#### Resultado Esperado:
O sistema deve barrar a submissão e exibir o alerta: "A carga horária deve ser um valor numérico entre 15 e 400 horas.".

#### Resolução e Reteste:
* **Ação Corretiva:** Criada a função `validate_workload(hours)` em `task_service.py` que valida a condição `15 <= val <= 400` antes de persistir no banco.
* **Evidência do Reteste:** Tentativa de inserção com 14h exibiu a mensagem de bloqueio esperada. Inserção com 15h gravou normalmente (CT-013).
* **Conclusão:** Defeito corrigido e aprovado em reteste.

---

## 3. Resumo Quantitativo de Gestão de Defeitos
* **Total de Defeitos Identificados:** 2
* **Total de Defeitos Corrigidos:** 2
* **Total de Defeitos Reabertos:** 0 (Taxa de Reabertura: 0,0%)
* **Defeitos Ativos / Pendentes:** 0 (100% de resolução)
