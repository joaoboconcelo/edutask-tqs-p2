# PROJETO INTEGRADO P2 - TESTES E QUALIDADE DE SOFTWARE
**UNISAGRADO - Ciência da Computação (2026)**  
**Disciplina:** Testes e Qualidade de Software  
**Professor:** Prof. Dr. Elvio Gilberto da Silva  
**Turma:** Turma A  

---

## 1. Identificação dos Integrantes
| Nome Completo | Função Principal no Projeto | Turma / Curso |
| :--- | :--- | :--- |
| **Gabriel Henrique Moreira** | Coordenação e Planejamento de Testes | Ciência da Computação - Turma A |
| **João Lucas de Antonio Boconcelo** | Automação e Engenharia de Qualidade (TDD/CI) | Ciência da Computação - Turma A |
| **Lucas Braga** | Análise e Execução Manual de Testes | Ciência da Computação - Turma A |

---

## 2. Nome e Versão do Sistema
* **Nome do Sistema:** EduTask Web - Sistema de Gestão Acadêmica e Atividades
* **Versão Avaliada:** v1.0.0-p2
* **Ambiente de Operação:** Ambiente Local de Homologação / Testes (`http://127.0.0.1:5000`)

---

## 3. Link do Repositório
* **Repositório GitHub:** *(a ser preenchido com o link do repositório do grupo)*
* **Branch de Trabalho:** `main`

---

## 4. Tecnologias Utilizadas
* **Backend:** Python 3.13, Flask 3.1.3, Werkzeug
* **Banco de Dados:** SQLite 3 (embutido)
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.3 (CDN), Bootstrap Icons
* **Testes Unitários:** Pytest 9.1+ / Unittest
* **Testes de Integração e API:** Coleção Postman (v2.1) + Requests + TestClient
* **Testes de Sistema / Interface:** Selenium WebDriver 4.51 (Google Chrome / Microsoft Edge)
* **Análise Estática de Qualidade:** Flake8, Radon (complexidade ciclomática)
* **CI/CD:** GitHub Actions (`.github/workflows/ci.yml`)

---

## 5. Pré-requisitos
* Sistema Operacional: Windows 10/11 ou Linux Ubuntu 22.04+
* Python 3.10 ou superior instalado e adicionado ao `PATH`
* Navegador Google Chrome ou Microsoft Edge instalado
* Git instalado

---

## 6. Instalação
Clone ou extraia o pacote do projeto e instale as dependências:
```powershell
cd 01_SISTEMA_ALVO
python -m pip install -r requirements.txt
```

---

## 7. Configuração
A aplicação vem pré-configurada para rodar em ambiente de desenvolvimento/testes isolado. O arquivo de banco SQLite `edutask.db` é criado e inicializado automaticamente no primeiro carregamento.
* Variável de ambiente opcional: `SECRET_KEY=unisagrado-tqs-p2-secret-2026`

---

## 8. Banco e Dados
* **Mecanismo:** SQLite 3
* **Criação de Tabelas:** O método `init_db()` cria automaticamente as tabelas `users`, `disciplines` e `tasks`.
* **Carga de Dados Fictícios:** O método `seed_initial_data()` popula registros controlados (1 usuário de teste, 2 disciplinas acadêmicas e 3 tarefas com diferentes níveis de prioridade e prazos).
* **Restauração de Dados:** Para restaurar o banco ao estado inicial limpo entre execuções, basta apagar o arquivo `01_SISTEMA_ALVO/edutask.db` e reiniciar o servidor.

---

## 9. Execução do Sistema
Inicie o servidor web local executando:
```powershell
cd 01_SISTEMA_ALVO
python run.py
```
Acesse no navegador: **`http://127.0.0.1:5000`**

---

## 10. Execução dos Testes Automatizados

### 10.1 Testes Unitários
Para executar a suíte de testes unitários:
```powershell
cd 07_AUTOMACAO_UNITARIA
pytest -v test_unitarios.py
```

### 10.2 Testes de Integração e API
Para executar os testes de API automatizados:
```powershell
cd 08_INTEGRACAO_API
python test_api_integracao.py
```
*(A coleção Postman editável também está disponível em `08_INTEGRACAO_API/edutask_api_collection.json`).*

### 10.3 Testes de Sistema e Interface (Selenium)
Com a aplicação em execução na porta 5000, rode os testes E2E:
```powershell
cd 09_SISTEMA_INTERFACE
python test_selenium_e2e.py
```

---

## 11. Acesso ao Pipeline CI/CD
O arquivo de configuração do pipeline de Integração Contínua está localizado em:
* `12_TDD_CICD_MELHORIA/.github/workflows/ci.yml`
* Gatilhos configurados: `push` e `pull_request` nas branches `main` e `develop`.
* Passos automatizados: Preparação do ambiente Python, instalação de dependências, checagem de qualidade com Flake8 e execução de todos os testes unitários e de integração.

---

## 12. Localização dos Documentos e Entregáveis
* `00_IDENTIFICACAO_E_README/`: Este README, Comprovante de Entrega e Apêndice A.
* `01_SISTEMA_ALVO/`: Código-fonte completo e funcional da aplicação EduTask Web.
* `02_REQUISITOS_ESCOPO_RISCOS/`: Requisitos (RF-01 a RF-06, RNF-01 a RNF-02) e Matriz de Riscos (R-01 a R-08).
* `03_PLANO_DE_TESTES/`: Plano de testes formal (Apêndice D).
* `04_CASOS_E_RASTREABILIDADE/`: 24 Casos de teste manuais e Matriz de Rastreabilidade.
* `05_EXECUCAO_MANUAL/`: Registro detalhado das 24 execuções manuais e evidências.
* `06_DEFEITOS/`: Registro de defeitos no padrão GitHub Issues / Jira e exportação em CSV.
* `07_AUTOMACAO_UNITARIA/`: Scripts de testes unitários automatizados.
* `08_INTEGRACAO_API/`: Coleção Postman e script de teste de API.
* `09_SISTEMA_INTERFACE/`: Scripts de testes ponta a ponta com Selenium WebDriver.
* `10_ACEITACAO_NAO_FUNCIONAIS/`: 4 Cenários de Aceitação e 6 Testes Não-Funcionais.
* `11_METRICAS_E_QUALIDADE/`: Relatório das 8 métricas com gráficos e análise estática.
* `12_TDD_CICD_MELHORIA/`: Evidências do ciclo TDD (Red-Green-Refactor) e arquivo de CI/CD.
* `13_RELATORIO_FINAL/`: Relatório Final Integrado em formatos DOCX e PDF.
* `14_APRESENTACAO_E_VIDEO_CONTINGENCIA/`: Slides da apresentação (PPTX e PDF) e roteiro do vídeo.
* `15_DIARIO_DE_PARTICIPACAO/`: Diário semanal de contribuições e Declaração assinada.
* `16_BACKUP_ENTREGA/`: Cópia de segurança e checklist final de verificação.

---

## 13. Credenciais Fictícias de Demonstração
* **Usuário Padrão:** `aluno@unisagrado.edu.br`
* **Senha:** `Senha@123`
* **Perfil:** Estudante / Gestor de Atividades

---

## 14. Problemas Conhecidos
* O Selenium em modo visual requer que o navegador Google Chrome ou Edge esteja instalado no sistema operacional. Caso executado em ambiente sem display (servidores headless), utilize o parâmetro `--headless` já previsto no script.

---

## 15. Contato do Grupo
* **Gabriel Henrique Moreira** (Ciência da Computação - Turma A)
* **João Lucas de Antonio Boconcelo** (Ciência da Computação - Turma A)
* **Lucas Braga** (Ciência da Computação - Turma A)
