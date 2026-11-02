# EduTask Web - Sistema de Gestão Acadêmica e Atividades

## 1. Identificação do Projeto
* **Instituição:** UNISAGRADO - Bauru/SP
* **Curso:** Ciência da Computação
* **Disciplina:** Testes e Qualidade de Software (P2)
* **Professor:** Prof. Dr. Elvio Gilberto da Silva
* **Integrantes da Equipe:**
  * Gabriel Henrique Moreira
  * João Lucas de Antonio Boconcelo
  * Lucas Braga
* **Versão do Sistema:** 1.0.0-p2

---

## 2. Tecnologias Utilizadas
* **Linguagem:** Python 3.13+
* **Framework Web:** Flask 3.1+
* **Banco de Dados:** SQLite 3 (embutido)
* **Segurança / Criptografia:** Werkzeug Security (hash PBKDF2/SHA256)
* **Frontend:** HTML5, CSS3, Bootstrap 5.3 (CDN), Bootstrap Icons
* **Testes & Qualidade:** Pytest, Selenium WebDriver, Postman / Requests, Flake8

---

## 3. Instruções de Instalação e Execução

### 3.1 Pré-requisitos
* Python 3.10 ou superior instalado.
* Navegador Google Chrome ou Microsoft Edge instalado.

### 3.2 Instalação das dependências
Abra o terminal na pasta raiz do projeto ou dentro desta pasta e execute:
```bash
pip install -r requirements.txt
```

### 3.3 Inicialização do Servidor Web Local
Para rodar a aplicação web localmente:
```bash
python run.py
```
O servidor estará disponível no endereço:
**`http://127.0.0.1:5000`**

### 3.4 Credenciais Fictícias de Demonstração
* **E-mail:** `aluno@unisagrado.edu.br`
* **Senha:** `Senha@123`
*(Novos usuários também podem ser cadastrados livremente pela tela de Registro).*

---

## 4. Estrutura de Fluxos Funcionais Atendidos
1. **Fluxo 1 (Autenticação e Perfil):** Cadastro com validações rigorosas de e-mail e força de senha; login com sessão autenticada; logout seguro.
2. **Fluxo 2 (Gestão de Disciplinas):** Cadastro de disciplinas com código formatado (ex: `CC-TQS01`), professor e carga horária; listagem e exclusão com integridade referencial.
3. **Fluxo 3 (Gestão de Tarefas):** Cadastro de atividades acadêmicas com data limite de entrega, prioridade (Baixa, Média, Alta) e descrição; atualização dinâmica de status.
4. **Fluxo 4 (Dashboard e Filtros):** Painel gerencial com cálculo automático de taxa percentual de conclusão e filtros combinados de status, prioridade e busca textual.
