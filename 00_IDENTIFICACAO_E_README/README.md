# EduTask Web Projeto Integrado P2

UNISAGRADO, Ciência da Computação, Turma A, Grupo 01. Professor: Prof. Dr. Elvio Gilberto da Silva.
Integrantes: Gabriel Henrique Moreira, João Lucas de Antonio Boconcelo e Lucas Braga.

## Sistema e versão

EduTask Web v1.0.1-p2, revisão de 11/11/2026; versão documental sem tag Git publicada. Aplicação acadêmica local de disciplinas e tarefas.
Repositório: https://github.com/joaoboconcelo/edutask-tqs-p2 . Esta revisão ainda precisa ser publicada pelo grupo.

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
python tools/medir_qualidade.py
python tools/verificar_pipeline.py
```

Selenium inicia seu próprio servidor local em porta livre; não requer servidor na porta 5000. Se necessário, definir CHROMEDRIVER como caminho do executável compatível e CHROME_BINARY como caminho do Chrome.
Resultado consolidado desta revisão: 98/98 cenários; logs e ambiente na pasta 11. Parametrizações são contadas como cenários.

## API e Postman

Importar `08_INTEGRACAO_API/edutask_api_collection.postman_collection.json` e `edutask_environment.postman_environment.json`.
Executar login válido primeiro e manter cookies na mesma sessão; demais endpoints exigem autenticação. Os testes Python usam Flask test client integrado ao SQLite, não requests de rede.
As medições de latência usam requests e HTTP real separadamente. A coleção Postman é fornecida; não há resultado Newman comprovado nesta revisão.

## Pipeline

Arquivo canônico: `.github/workflows/ci.yml`. Instala dependências, executa linter bloqueante e os testes e preserva artefatos.
Sem URL de run desta revisão: publicar e executar no GitHub é pendência. `tools/verificar_pipeline.py` comprova falha e sucesso locais e identifica o ambiente corretamente.

## Documentos e evidências

00 identificação e pendências; 01 sistema; 02 requisitos e riscos; 03 plano; 04 catálogo e matriz; 05 relatos manuais e reexecução automatizada; 06 defeitos históricos e confirmados; 07 unidade; 08 integração/Postman; 09 Selenium e capturas; 10 aceitação e não funcionais; 11 métricas, planilha e dados brutos; 12 TDD e CI; 13 relatório DOCX/PDF; 14 dispensa de apresentação/vídeo; 15 diário para conferência; 16 backup e checklist.

Relatório atual: `13_RELATORIO_FINAL/RELATORIO_FINAL_PROJETO_P2.docx` e PDF correspondente. O memorial na raiz é cópia do relatório revisado; materiais antigos da apresentação não são fonte dos resultados atuais.

## Limitações e contato

Consulte `PENDENCIAS_PARA_ENTREGA.md`: aprovação docente, registros manuais e humanos, origem/licença, publicação/Actions/Issues e entrega oficial ainda dependem do grupo.
Não há auditoria completa de segurança, carga concorrente, CSRF dedicado ou aceitação externa comprovada. Parecer limitado ao laboratório acadêmico.
Contato: os três integrantes identificados no início; nenhum contato pessoal foi inventado.
