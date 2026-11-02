# PRODUTO P13 - APRESENTAÇÃO FINAL E ROTEIRO DE DEMONSTRAÇÃO
**Projeto:** EduTask Web v1.0.0-p2  
**Disciplina:** Testes e Qualidade de Software | **UNISAGRADO 2026**  
**Docente:** Prof. Dr. Elvio Gilberto da Silva  
**Tempo Previsto:** 12 a 15 minutos de exposição + 5 minutos de arguição da banca.  

---

## 1. Divisão da Apresentação entre os Integrantes

| Bloco | Conteúdo Abordado | Orador Responsável | Tempo Estimado |
| :---: | :--- | :--- | :---: |
| **Parte 1** | Abertura, identificação do sistema EduTask, objetivos, escopo e matriz de riscos priorizados. | **Gabriel Henrique Moreira** | ~ 4 minutos |
| **Parte 2** | Demonstração dos testes manuais, técnica aplicada (BVA/EP), relato do defeito DEF-01 e evidências. | **Lucas Braga** | ~ 4 minutos |
| **Parte 3** | Demonstração prática dos testes automatizados (Pytest e Selenium E2E), ciclo TDD e pipeline CI/CD. | **João Lucas Boconcelo** | ~ 4 minutos |
| **Parte 4** | Apresentação dos gráficos de métricas, prontidão para uso, melhorias contínuas e encerramento. | **Gabriel / Todos** | ~ 2 minutos |

---

## 2. Estrutura dos Slides da Apresentação (Slide a Slide)

* **Slide 1: Capa Oficial**
  * Título: Projeto Integrado P2 - Planejamento, Execução e Avaliação da Qualidade de Software
  * Sistema: EduTask Web (Gestão Acadêmica e Atividades)
  * Instituição: UNISAGRADO - Ciência da Computação - Turma A
  * Docente: Prof. Dr. Elvio Gilberto da Silva
  * Integrantes: Gabriel Henrique Moreira, João Lucas de Antonio Boconcelo, Lucas Braga

* **Slide 2: Contextualização e Problema Orientador**
  * O desafio da gestão de entregas acadêmicas para estudantes de computação.
  * Problema orientador: Como garantir, com evidências técnicas auditáveis, que o sistema atende aos requisitos funcionais e de segurança antes de ser disponibilizado?

* **Slide 3: Arquitetura do Sistema-Alvo**
  * Stack Tecnológica: Python 3.13, Flask 3.1, SQLite 3, Bootstrap 5.3.
  * 4 Fluxos Funcionais Centrais: Autenticação, Disciplinas, Tarefas e Dashboard de Métricas.

* **Slide 4: Escopo, Requisitos e Matriz de Riscos**
  * Apresentação dos 8 requisitos (6 RF e 2 RNF).
  * 8 riscos avaliados por probabilidade e impacto (destaque para armazenamento seguro de senhas e integridade referencial).

* **Slide 5: Planejamento e Técnicas de Projeto de Testes**
  * Aplicação rigorosa de Particionamento de Equivalência e Análise de Valor Limite.
  * Estratégia de pirâmide de testes: Unidade, Integração e Ponta a Ponta (E2E).

* **Slide 6: Execução Manual e Gestão de Defeitos**
  * Execução dos 24 casos de teste manuais.
  * Estudo de caso do defeito **DEF-01** (Validação de política de senha forte) e **DEF-02** (Trava de carga horária inferior a 15h).
  * Ciclo de vida no GitHub Issues e reteste com sucesso.

* **Slide 7: Demonstração ao Vivo: Automação Multinível**
  * **Nível 1 (Unitário):** 8 testes com Pytest executando em menos de 0.5s.
  * **Nível 2 (API/Integração):** 6 testes de contrato e regras de negócio com validação de status HTTP 200, 201, 401 e 409.
  * **Nível 3 (Sistema/Selenium):** 4 fluxos E2E no navegador simulando a jornada real do aluno.

* **Slide 8: Prática de TDD (Red - Green - Refactor)**
  * Criação da regra de cálculo automático de score de urgência (`calculate_task_urgency`).
  * Evidência do ciclo: Falha inicial intencional -> Implementação mínima aprovada -> Refatoração com Clean Code e tipagem estática.

* **Slide 9: Pipeline de Integração Contínua (CI/CD)**
  * Fluxo no GitHub Actions (`.github/workflows/ci.yml`).
  * Demonstração de execução bem-sucedida e bloqueio automático de commits com regressão.

* **Slide 10: Painel de Indicadores e Métricas de Qualidade**
  * Apresentação dos gráficos gerados: 100% de execução, 100% de aprovação final, 100% de cobertura de requisitos e 0% de taxa de reabertura de bugs.
  * Análise estática com Flake8 comprovando conformidade do código.

* **Slide 11: Testes de Aceitação (UAT) e Não-Funcionais**
  * Validação com foco no estudante (100% dos 4 cenários aceitos).
  * Resposta média de 28,4ms na UI e 18,5ms na API; proteção por hash criptográfico PBKDF2/SHA256.

* **Slide 12: Conclusão e Plano de Melhoria Contínua**
  * Parecer de qualidade: O sistema EduTask Web v1.0.0 está **aprovado e pronto para uso acadêmico**.
  * Ações futuras priorizadas: Paginação, notificações automáticas por e-mail e migração para PostgreSQL.

---

## 3. Roteiro para Demonstração Prática e Vídeo de Contingência

### 3.1 Procedimento Passo a Passo da Demonstração (Ao Vivo / Gravada)
1. **Passo 1 (Subir a Aplicação):**
   Abrir o terminal, navegar até `01_SISTEMA_ALVO` e executar `python run.py`. Mostrar a inicialização limpa na porta 5000.
2. **Passo 2 (Execução dos Testes Unitários):**
   Abrir novo terminal, navegar até `07_AUTOMACAO_UNITARIA` e rodar `pytest -v test_unitarios.py`. Destacar os 8 testes verdes passando em menos de 1 segundo.
3. **Passo 3 (Execução dos Testes de Integração de API):**
   Navegar até `08_INTEGRACAO_API` e rodar `pytest -v test_api_integracao.py`. Mostrar a validação dos contratos HTTP.
4. **Passo 4 (Demonstração do Selenium E2E):**
   Navegar até `09_SISTEMA_INTERFACE` e executar `python test_selenium_e2e.py`. Explicar que a automação executa o login, cadastra uma disciplina, cria uma tarefa e valida o progresso no painel com esperas explícitas.
5. **Passo 5 (Apresentação do Pipeline GitHub Actions):**
   Exibir na tela a aba "Actions" do repositório demonstrando o pipeline com ícone verde em todas as etapas.

### 3.2 Plano de Contingência para Falha de Rede ou Equipamento
* Todas as demonstrações são executáveis **100% offline** em `localhost`.
* Em caso de queda de energia ou indisponibilidade de internet no projetor, o arquivo de vídeo curto (`video_contingencia_demonstracao.mp4` ou link offline) e as capturas de tela contidas na pasta de backup garantem a comprovação de todos os critérios da avaliação.
