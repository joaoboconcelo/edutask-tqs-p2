# PRODUTO P03 - PLANO DE TESTES DE SOFTWARE (APÊNDICE D)
**Projeto:** EduTask Web v1.0.0-p2  
**Instituição:** UNISAGRADO - Curso de Ciência da Computação (2026)  
**Disciplina:** Testes e Qualidade de Software  
**Docente:** Prof. Dr. Elvio Gilberto da Silva  
**Equipe Responsável:** Gabriel Henrique Moreira, João Lucas de Antonio Boconcelo, Lucas Braga  

---

## 1. Identificação e Versão do Sistema
* **Nome do Sistema:** EduTask Web (Sistema de Gestão Acadêmica e Atividades)
* **Versão Avaliada:** v1.0.0-p2
* **Repositório:** `https://github.com/joaoboconcelo/edutask-tqs-p2`
* **Tipo de Aplicação:** Aplicação Web com backend Python Flask, banco SQLite e frontend responsivo Bootstrap.

---

## 2. Objetivo Geral do Teste
Validar formalmente o comportamento funcional, a confiabilidade, a segurança básica, a usabilidade e o desempenho do sistema EduTask Web. O objetivo é assegurar que todos os 8 requisitos aprovados (RF-01 a RF-06 e RNF-01 a RNF-02) sejam atendidos sem falhas críticas impeditivas, fornecendo evidências auditáveis de qualidade e sustentabilidade para a liberação final (P2).

---

## 3. Escopo e Fora do Escopo

### 3.1 Escopo dos Testes
* Fluxo 1: Autenticação, cadastro de usuário, política de senhas, criação e encerramento de sessão.
* Fluxo 2: Gestão de disciplinas (cadastro, formatação de código, integridade de carga horária e exclusão com proteção relacional).
* Fluxo 3: Gestão de atividades e tarefas (criação com prazo limite, níveis de prioridade, ciclo de status Pendente -> Em Andamento -> Concluída).
* Fluxo 4: Dashboard gerencial, cálculo dinâmico de taxa de conclusão e filtros combinados.
* Endpoints da API REST (`/api/auth/login`, `/api/disciplinas`, `/api/tarefas`, `/api/metricas`).
* Automação multinível (Unitário, API e Selenium E2E).
* Ciclo TDD para nova regra de cálculo de urgência de prazos.

### 3.2 Fora do Escopo dos Testes
* Testes destrutivos de negação de serviço (DDoS) ou estresse com milhares de requisições simultâneas em servidores remotos.
* Compatibilidade com navegadores obsoletos (Internet Explorer 11).
* Módulos financeiros, envio de SMS ou emissão de diplomas.

---

## 4. Níveis e Tipos de Teste

### 4.1 Níveis de Teste
1. **Teste Unitário:** Verificação isolada de funções e métodos de regras de negócio sem dependências externas (`validate_email`, `validate_password_strength`, `validate_discipline_code`, `calculate_completion_rate`, `calculate_task_urgency`).
2. **Teste de Integração / API:** Validação da comunicação entre endpoints HTTP, camadas de serviço e persistência no banco SQLite via Postman e Requests.
3. **Teste de Sistema / Interface (E2E):** Validação dos fluxos completos da perspectiva do usuário via interface gráfica web com automação em Selenium WebDriver.
4. **Teste de Aceitação:** Verificação de cenários de ponta a ponta baseados nas necessidades reais de estudantes e professores.

### 4.2 Tipos de Teste
* **Testes Funcionais:** Positivos, negativos, alternativos e de fronteira.
* **Testes Não-Funcionais:** Desempenho básico (tempo de resposta), Usabilidade (clareza e eficiência da UI) e Segurança básica (proteção contra injeção de dados e armazenamento com hash PBKDF2).
* **Testes de Regressão e Reteste:** Revalidação de correções de defeitos encontrados.

---

## 5. Técnicas de Projeto de Teste
* **Particionamento de Equivalência (EP):** Divisão dos domínios de entrada em classes válidas e inválidas (ex: formato de e-mail, formato de código de disciplina, faixas de carga horária).
* **Análise de Valor Limite (BVA):** Exploração sistemática dos limites extremos das partições (ex: tamanho mínimo e máximo de senha, carga horária de 14h, 15h, 400h e 401h; datas no passado, presente e futuro).
* **Tabela de Decisão:** Mapeamento de combinações de filtros de status e prioridade.
* **Teste Baseado em Riscos:** Priorização dos casos de teste de maior probabilidade e severidade de impacto (R-01 a R-08).

---

## 6. Ambiente e Ferramentas

| Ferramenta / Recurso | Versão | Finalidade no Projeto |
| :--- | :--- | :--- |
| **Python** | 3.13.2 | Interpretador da linguagem de desenvolvimento e testes |
| **Pytest** | 9.1.1 | Framework para execução e asserções de testes unitários |
| **Postman / Requests** | v2.1 / 2.34 | Criação de coleções, asserções de contrato de API e integração |
| **Selenium WebDriver** | 4.51.0 | Automação de testes de ponta a ponta (E2E) no navegador Chrome/Edge |
| **Flake8** | 7.4.1 | Análise estática de código e métricas de manutenibilidade |
| **GitHub Issues** | Web | Gestão, ciclo de vida e rastreamento de defeitos (bugs) |
| **GitHub Actions** | Workflow | Pipeline de Integração Contínua (CI/CD) |
| **Google Chrome / Edge** | Atualizados | Navegadores para execução e gravação de evidências |

---

## 7. Dados de Teste e Gestão de Massa
* **Origem dos dados:** Somente dados fictícios criados para o projeto, sem qualquer informação pessoal sensível ou dados reais de terceiros.
* **Massa Padrão Inicial:** Usuário `aluno@unisagrado.edu.br` (senha: `Senha@123`), disciplinas `CC-TQS01` e `CC-BD02`.
* **Política de Isolamento:** Os testes de integração e automação criam seus próprios dados de teste temporários com prefixos identificáveis (ex: `TEST-`) e contam com função de limpeza para evitar poluição do banco.

---

## 8. Responsabilidades da Equipe

| Integrante | Papel Principal | Atribuições Específicas |
| :--- | :--- | :--- |
| **Gabriel Henrique Moreira** | Coordenação & Gestão | Elaboração do cronograma, gestão de riscos, especificação dos casos de aceitação e consolidação do relatório final. |
| **João Lucas de Antonio Boconcelo** | Automação & Qualidade | Desenvolvimento dos scripts unitários, Selenium E2E, coleção Postman, configuração do CI/CD e ciclo TDD. |
| **Lucas Braga** | Execução & Análise Manual | Execução controlada dos 24 casos manuais, captura de evidências, abertura e acompanhamento de defeitos no GitHub Issues e testes não-funcionais. |

---

## 9. Critérios do Processo

### 9.1 Critérios de Entrada
* Código-fonte da versão estável disponibilizado no repositório.
* Ambiente local de execução operacional e banco SQLite inicializado.
* Requisitos e riscos formalizados e aprovados.

### 9.2 Critérios de Saída
* 100% dos 24 casos de teste manuais executados e com evidências anexadas.
* 100% dos testes automatizados (unitários, API e Selenium) executando com sucesso (100% pass rate).
* Todos os defeitos de severidade "Alta" ou "Crítica" corrigidos e verificados em reteste.
* Métricas e indicadores de qualidade calculados e analisados.
* Relatório final completo concluído nos formatos DOCX e PDF.

### 9.3 Critérios de Suspensão e Retomada
* **Suspensão:** Falha crítica na inicialização do servidor Flask ou corrupção irreparável do banco de dados que impeça a execução de mais de 50% dos casos de teste.
* **Retomada:** Restauração do banco limpo via script `init_db()` e correção da inconsistência do servidor.

---

## 10. Cronograma de Marcos do Projeto

| Marco | Descrição | Responsável | Status |
| :---: | :--- | :---: | :---: |
| **M0** | Alinhamento do tema, manual e formação do grupo | Todos | Concluído |
| **M1** | Seleção do sistema EduTask e elaboração do Apêndice A | Gabriel | Concluído |
| **M2** | Delimitação do escopo, requisitos (RF/RNF) e matriz de riscos | Gabriel | Concluído |
| **M3** | Especificação dos 24 casos de teste manuais por técnicas | Lucas | Concluído |
| **M4** | Execução manual inicial, coleta de evidências e registro de defeitos | Lucas | Concluído |
| **M5** | Configuração do repositório, ambiente e análise estática (Flake8) | João Lucas | Concluído |
| **M6** | Automação de testes unitários (Pytest) e integração (API Postman) | João Lucas | Concluído |
| **M7** | Automação de testes de interface (Selenium) e não-funcionais | João Lucas / Lucas | Concluído |
| **M8** | Cálculo e interpretação gráfica das 8 métricas de qualidade | Todos | Concluído |
| **M9** | Execução do ciclo TDD, pipeline GitHub Actions e plano de melhoria | João Lucas | Concluído |
| **P2** | Entrega do Drive com 17 pastas, Relatório Final e Apresentação | Todos | Concluído |

---

## 11. Riscos do Processo de Teste
* **Risco de atraso por falha de ambiente:** Mitigado pelo uso de SQLite local e dependências padronizadas no `requirements.txt`.
* **Risco de instabilidade nos testes de interface (Flaky Tests):** Mitigado pelo uso de esperas explícitas (`WebDriverWait`) do Selenium em vez de `time.sleep()`.
* **Risco de indisponibilidade de internet no dia da apresentação:** Mitigado pela preparação de execução 100% offline e gravação de vídeo de contingência.

---

## 12. Produtos e Controle de Comunicação
* **Canais de Comunicação:** Reuniões presenciais em aula, mensagens no grupo técnico e commits rastreados via Git.
* **Controle de Versão:** Versão final do plano: v1.0.0-p2 (Revisada e aprovada pelo grupo).
