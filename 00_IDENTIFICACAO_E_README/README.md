# EduTask Web Projeto Integrado P2

UNISAGRADO, Ciência da Computação, Turma A. Professor: Prof. Dr. Elvio Gilberto da Silva.
Integrantes: Gabriel Henrique Moreira, João Lucas de Antonio Boconcelo e Lucas Braga.

## Sistema e versão

EduTask Web v1.0.1-p2, revisão de 11/11/2026; versão documental sem tag Git publicada. Aplicação acadêmica local de disciplinas e tarefas.
Repositório: https://github.com/joaoboconcelo/edutask-tqs-p2 . Revisão publicada no commit 33d441c7f6dc4599da735727f232c5c1aa5d41f3; atualizações documentais posteriores constam do histórico.

## Tecnologias e pré requisitos

Python 3.10+, Flask, Werkzeug, SQLite, Jinja2, Bootstrap, pytest e Selenium. Chrome instalado para E2E e driver compatível; Selenium Manager pode precisar de rede na primeira execução.
O servidor e os testes de API são locais. Bootstrap e ícones usam CDN; não se promete interface estilizada totalmente offline.

## Instalação e configuração

Da raiz da entrega, preferencialmente em ambiente virtual:
```powershell
python -m venv .venv
.venv/Scripts/Activate.ps1
python -m pip install -r 01_SISTEMA_ALVO/requirements.txt
```

SECRET_KEY pode ser configurada no ambiente; o valor padrão serve apenas ao laboratório. Não expor o servidor de desenvolvimento na internet.

## Banco e dados

SQLite de demonstração em `01_SISTEMA_ALVO/edutask.db`, criado automaticamente com um usuário, duas disciplinas e três tarefas.
Cada teste usa banco temporário por configuração DATABASE; não altera o banco de demonstração. Não apagar a base para rodar os testes.
Para reinicializar apenas a demonstração, parar o servidor, remover esse arquivo específico e reiniciar. As datas de seed são fixas; urgência na interface acompanha a data atual.

## Execução

```powershell
python 01_SISTEMA_ALVO/run.py
```
Acesso: http://127.0.0.1:5000 . Credenciais fictícias: `aluno@unisagrado.edu.br` / `Senha@123`.

## Testes

Da raiz:
```powershell
python -m pytest -v 07_AUTOMACAO_UNITARIA
python -m pytest -v 08_INTEGRACAO_API
python -m pytest -v 05_EXECUCAO_MANUAL/test_reexecucao_catalogo.py 10_ACEITACAO_NAO_FUNCIONAIS
python -m pytest -v 09_SISTEMA_INTERFACE
python -m flake8 01_SISTEMA_ALVO/edutask --config=01_SISTEMA_ALVO/.flake8
python 11_METRICAS_E_QUALIDADE/medir_qualidade.py
python 12_TDD_CICD_MELHORIA/verificar_pipeline.py
```

Selenium inicia seu próprio servidor local em porta livre; não requer servidor na porta 5000. Se necessário, definir CHROMEDRIVER como caminho do executável compatível e CHROME_BINARY como caminho do Chrome.
Resultado consolidado desta revisão: 98/145 cenários; logs e ambiente na pasta 11. Parametrizações são contadas como cenários.

## API e Postman

Importar `08_INTEGRACAO_API/edutask_api_collection.postman_collection.json` e `edutask_environment.postman_environment.json`.
Executar login válido primeiro e manter cookies na mesma sessão; demais endpoints exigem autenticação. Os testes Python usam Flask test client integrado ao SQLite, não requests de rede.
As medições de latência usam requests e HTTP real separadamente. Em 26/11/2026 a coleção foi executada com Newman 6.2.1 (Node.js 26.13.1) contra uma instância local com banco temporário: 6 requisições e 12 asserções aprovadas, nenhuma falha, tempo médio de resposta de 153 ms. Relatórios em `08_INTEGRACAO_API/evidencias_newman/` (texto, JSON e JUnit). Para reproduzir, com o servidor de inspeção ativo (`python 05_EXECUCAO_MANUAL/servidor_validacao_interativa.py`, porta 5011):
```powershell
npx newman@6.2.1 run 08_INTEGRACAO_API/edutask_api_collection.postman_collection.json -e 08_INTEGRACAO_API/edutask_environment.postman_environment.json --env-var base_url=http://127.0.0.1:5011
```

## Pipeline

Arquivo canônico: `.github/workflows/ci.yml`. Instala dependências, executa linter bloqueante e os testes e preserva artefatos.
Execução aprovada em main: https://github.com/joaoboconcelo/edutask-tqs-p2/actions/runs/43094289919 . Falha controlada: https://github.com/joaoboconcelo/edutask-tqs-p2/actions/runs/43094396473 . Correção aprovada: https://github.com/joaoboconcelo/edutask-tqs-p2/actions/runs/43094602358 . O PR #5 foi encerrado sem merge. Logs na pasta 12.

## Documentos e evidências

00 identificação e instruções; 01 sistema; 02 requisitos e riscos; 03 plano; 04 catálogo e matriz; 05 relatos manuais e reexecução automatizada; 06 defeitos históricos e confirmados; 07 unidade; 08 integração/Postman; 09 Selenium e capturas; 10 aceitação e não funcionais; 11 métricas, planilha e dados brutos; 12 TDD e CI; 13 relatório DOCX/PDF; 14 dispensa de apresentação/vídeo; 15 diário para conferência; 16 backup e checklist.

Relatório atual: `13_RELATORIO_FINAL/RELATORIO_FINAL_PROJETO_P2.docx` e PDF correspondente. O relatório da pasta 13 é a versão canônica. A pasta 14 registra a dispensa de apresentação/vídeo; duplicatas e materiais de apresentação antigos foram removidos.

## Limitações e contato

A autorização do professor para usar o sistema foi registrada pelo grupo em 11/11/2026. A publicação, as issues e as evidências do Actions foram concluídas.
Não há auditoria completa de segurança, carga concorrente, CSRF dedicado ou aceitação externa comprovada. Parecer limitado ao laboratório acadêmico.
Contato: os três integrantes identificados no início.

## Inspeção interativa e organização final

A pasta 05 contém 24 capturas de casos conduzidos pela interface por assistente; a pasta 10 contém quatro cenários de aceitação técnica igualmente conferidos. O relatório detalha os bloqueios nativos do navegador e separa os 145 cenários automatizados das 28 observações adicionais. Os utilitários de apoio ficam junto ao produto que geram: medição (11), pipeline local (12), relatório (13), backup (16) e servidor de inspeção (05).

## Revisão complementar para fechamento técnico

A suíte atual possui 145 cenários, com 34 de unidade e 79 de integração/API. A cobertura de linhas é 98.32% e de ramos 94.19%. O ciclo TDD de contrato JSON tem três commits reais registrados na pasta 12. RNF-02 é atendido com PBKDF2-SHA256; hashes antigos são atualizados após login válido, sem alterar a senha. Os seis defeitos estão no P07 e nas issues correspondentes.
