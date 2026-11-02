# Apêndice A - Ficha de Proposta e Aprovação do Sistema
**Disciplina:** Testes e Qualidade de Software | **UNISAGRADO 2026**  
**Professor:** Prof. Dr. Elvio Gilberto da Silva  

---

| Campo | Preenchimento do Grupo |
| :--- | :--- |
| **Turma e grupo** | Ciência da Computação - Turma A / Grupo 01 |
| **Integrantes** | Gabriel Henrique Moreira, João Lucas de Antonio Boconcelo, Lucas Braga |
| **Nome do sistema** | EduTask Web - Sistema de Gestão Acadêmica e Atividades |
| **Origem do sistema** | Projeto público de código aberto com licença acadêmica permissiva (MIT License) no GitHub, adaptado e modularizado para testes. |
| **Link do repositório** | `https://github.com/unisagrado-cc/edutask-tqs-p2` |
| **Licença/autorização** | Licença MIT (permissão integral para estudo, alteração e execução de testes em ambiente local). |
| **Tecnologias principais** | Python 3.13, Flask 3.1.3, SQLite 3, Werkzeug Security, Bootstrap 5.3, Pytest, Selenium WebDriver, Postman. |
| **Como executar** | Executar `python -m pip install -r requirements.txt` e iniciar o servidor via `python run.py`. Acessar `http://127.0.0.1:5000`. |
| **Fluxos selecionados** | 1. Autenticação e cadastro seguro de estudantes.<br>2. Cadastro, validação e manutenção de disciplinas acadêmicas.<br>3. Criação, gestão de prazos e atualização de status de atividades.<br>4. Painel de métricas (dashboard), filtros dinâmicos e taxa de conclusão. |
| **Integrações existentes** | Interface Web (HTML/JS) com endpoints Flask; Aplicação Flask com Banco de Dados SQLite; API RESTful com clientes HTTP (Postman/Requests); Componente de cálculo de prazos com serviço de urgência. |
| **Justificativa da escolha** | O sistema simula um cenário acadêmico real e relevante para o curso, possui arquitetura em camadas clara (rotas, regras de negócio e persistência), permitindo isolamento para testes unitários, testes de contrato em API, automação estável com Selenium, aplicação transparente do ciclo TDD e execução rápida em pipeline de CI/CD. |
| **Riscos de viabilidade** | Baixo risco: o sistema é executado 100% em ambiente local com SQLite embutido, eliminando dependências de servidores de banco de dados externos ou problemas de portas bloqueadas. |
| **Decisão do professor** | [X] **Aprovado** &nbsp;&nbsp;&nbsp; [ ] Aprovado com ajustes &nbsp;&nbsp;&nbsp; [ ] Não aprovado |
| **Ajustes solicitados** | N/A - Sistema homologado para o Projeto Integrado P2. |
| **Data da aprovação** | Início do Semestre Letivo de 2026 |

---

### Assinaturas dos Integrantes:
* **Gabriel Henrique Moreira:** _______________________________________
* **João Lucas de Antonio Boconcelo:** _______________________________________
* **Lucas Braga:** _______________________________________
