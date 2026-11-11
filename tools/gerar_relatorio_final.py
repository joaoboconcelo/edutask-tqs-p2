"""Gera o relatório completo a partir das evidências e do catálogo da entrega."""
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'13_RELATORIO_FINAL'


def read(path): return (ROOT/path).read_text(encoding='utf-8')
def load(path): return json.loads(read(path))


def source_markdown():
    summary=load('11_METRICAS_E_QUALIDADE/evidencias/resumo_entrega.json')
    perf=load('11_METRICAS_E_QUALIDADE/evidencias/desempenho.json')
    github=load('12_TDD_CICD_MELHORIA/evidencias/github/registro_consolidado.json')
    inspection=load('05_EXECUCAO_MANUAL/evidencias_interface/registro_consolidado.json')
    versions=load('11_METRICAS_E_QUALIDADE/evidencias/versoes_python.json')
    cov=summary['coverage']; linepercent=100*cov['covered_lines']/cov['num_statements']
    tdd=load('12_TDD_CICD_MELHORIA/evidencias/tdd_json/commits.json')
    tddrows='\n'.join(f"| {r['etapa']} | {r['commit'][:12]} | {r['data']} | {r['resultado']} |" for r in tdd['etapas'])
    tddlinks='\n'.join(f"- {r['etapa']}: {r['url']}" for r in tdd['etapas'])
    latency='\n'.join(f"| `{route}` | {v['n']} | {v['min_ms']:.3f} | {v['media_ms']:.3f} | {v['p95_ms']:.3f} | {v['max_ms']:.3f} |" for route,v in perf['rotas'].items())
    runrows='\n'.join(f"| {kind.replace('_',' ')} | {v['commit'][:12]} | {v['conclusao']} | {v['id']} |" for kind,v in github['execucoes'].items())
    requirements=[]; risks=[]
    for row in read('02_REQUISITOS_ESCOPO_RISCOS/P02_Requisitos_Escopo_Riscos.md').splitlines():
        cells=[c.strip() for c in row.strip('|').split('|')]
        if len(cells)==5 and re.fullmatch(r'\*\*(?:RF|RNF)-\d+\*\*',cells[0]):
            requirements.append(f"### {cells[0].replace('**','')}\n\n{cells[1]}\n\nTipo: {cells[2]}. Prioridade: {cells[3]}.\n\nCritério de aceitação: {cells[4].replace('<br>',' ')}\n")
        if len(cells)==6 and re.fullmatch(r'\*\*R-\d+\*\*',cells[0]):
            risks.append('| '+cells[0]+' | '+cells[1]+' | '+cells[2]+'/'+cells[3]+' | '+cells[4]+' |')
    scenarios='\n'.join(f"| {r['caso']} | {r['obtido']} | `evidencias_interface/{r['caso']}.png` |" for r in inspection['casos'] if r['caso'].startswith('UAT-'))
    uirows='\n'.join(f"| {r['caso']} | {r['obtido']} |" for r in inspection['casos'] if r['caso'].startswith('CT-'))
    versionrows='\n'.join(f'| {name} | {version} |' for name,version in versions.items())
    catalog=read('04_CASOS_E_RASTREABILIDADE/P04_Catalogo_Casos_de_Teste.md')
    catalog=catalog[catalog.index('### CT-001'):].split('## Observações da inspeção interativa')[0]
    catalog=catalog.replace('### CT-','### Caso CT-')
    defecttext=read('06_DEFEITOS/P07_Relatorio_e_Gestao_de_Defeitos.md')
    defecttext=defecttext[defecttext.index('## DEF-03'):].replace('## DEF-','### DEF-').split('## Vínculos e reteste remoto')[0]
    return f'''# Relatório técnico completo do EduTask Web

## Síntese dos resultados

O Projeto Integrado P2 aplicou planejamento, especificação, execução, automação e análise de qualidade ao EduTask Web. A versão revisada v1.0.1-p2 possui código executável, banco SQLite, interface web, API e regras de domínio separadas. A entrega reúne documentos rastreáveis, arquivos-fonte e evidências que permitem repetir a avaliação.

Foram aprovados **{summary['tests']['total']} cenários automatizados**: {summary['unidade']} unitários, {summary['integracao']} de integração/API, 24 de reexecução do catálogo e quatro de aceitação técnica, além de quatro fluxos Selenium incluídos nesse total. A cobertura da suíte sem navegador é de **{linepercent:.2f}% das linhas executáveis**. O Flake8 passou de 179 ocorrências na linha de base para zero depois da revisão.

Além da suíte, foram realizadas **28 observações interativas pela interface**, sendo 24 casos do catálogo e quatro cenários de aceitação técnica. As capturas e os snapshots foram preservados. Essas observações não são contadas novamente como testes da suíte e não constituem assinatura ou homologação humana.

Seis defeitos confirmados foram corrigidos e registrados nas issues #1, #2, #3, #4, #6 e #7. A revisão publicada passou no GitHub Actions. Um PR separado demonstrou falha intencional detectada pelo pipeline e uma execução aprovada depois da remoção da asserção falsa. O experimento foi encerrado sem merge na versão principal.

O parecer é favorável ao uso no laboratório acadêmico dentro do escopo verificado. Permanecem dependentes das pessoas responsáveis a aprovação docente, a conferência de participação e assinaturas, a homologação humana quando exigida e a entrega na pasta oficial do Drive.

<!-- pagebreak -->

## 1 Introdução

### 1.1 Contexto e problema orientador

Estudantes precisam organizar disciplinas, tarefas, prazos e prioridades. Uma aplicação que apresenta dados incorretos, permite acesso indevido ou aceita entradas inconsistentes pode prejudicar esse acompanhamento. O EduTask Web foi usado como objeto acadêmico para observar esses riscos e aplicar as técnicas da disciplina Testes e Qualidade de Software.

O problema orientador é determinar, com verificações reproduzíveis, quais requisitos selecionados são atendidos, quais falhas foram encontradas e quais limitações continuam relevantes. A avaliação não se baseia apenas em o sistema abrir no navegador: exige confrontar o esperado com o observado e conservar o vínculo entre requisito, risco, caso, resultado e defeito.

### 1.2 Objetivo geral e objetivos específicos

O objetivo geral é planejar, executar e avaliar a qualidade do EduTask Web em ambiente acadêmico controlado. Os objetivos específicos são delimitar requisitos e riscos; projetar casos com equivalência, limites e decisões; verificar comportamento e persistência; registrar defeitos; automatizar níveis complementares; medir indicadores; experimentar TDD; e comprovar a execução contínua no GitHub.

A estrutura segue os produtos P01 a P14 e as quantidades mínimas do manual fornecido pelo professor. Cada conjunto de evidências possui um papel definido. O relatório interpreta os resultados; ele não substitui os scripts, dados brutos, capturas ou instruções de reprodução.

### 1.3 Identificação e contexto da revisão

Instituição: UNISAGRADO. Curso: Ciência da Computação. Disciplina: Testes e Qualidade de Software. Professor: Prof. Dr. Elvio Gilberto da Silva. Turma A, Grupo 01. Integrantes: Gabriel Henrique Moreira, João Lucas de Antonio Boconcelo e Lucas Braga.

Versão revisada: v1.0.1-p2, identificação documental sem tag de release criada. Data de consolidação: 11/11/2026. Repositório: https://github.com/joaoboconcelo/edutask-tqs-p2 . A revisão técnica inicial foi publicada no commit `33d441c7f6dc4599da735727f232c5c1aa5d41f3`; alterações documentais posteriores estão identificadas no histórico.

Apresentação e vídeo foram dispensados conforme informação do solicitante. A estrutura da pasta 14 foi mantida para respeitar a organização do manual. A confirmação docente da dispensa e a eventual redistribuição da pontuação não foram presumidas.

## 2 Caracterização e arquitetura do sistema

### 2.1 Finalidade e fluxos funcionais

O EduTask Web permite cadastrar uma conta, autenticar um estudante, registrar disciplinas, criar tarefas vinculadas, atualizar status e consultar indicadores. Os quatro fluxos centrais usados na avaliação são autenticação/cadastro; manutenção de disciplinas; criação e acompanhamento de tarefas; e dashboard com filtros e percentual de conclusão.

O formulário de usuário exige nome, e-mail válido e confirmação de senha. O formulário de disciplina exige código no formato definido, nome, professor e carga entre 15h e 400h. O formulário de tarefa exige título de pelo menos três caracteres, disciplina existente, prazo e prioridade. A interface aceita uma tarefa vencida com aviso; sua urgência é calculada pela data, não pelo valor de prioridade escolhido.

### 2.2 Arquitetura e responsabilidades

| Camada | Arquivos principais | Responsabilidade |
|---|---|---|
| Inicialização | `edutask/app.py`, `run.py` | Criar aplicação, aplicar configuração, inicializar dados e registrar blueprints |
| Apresentação | `edutask/templates/*.html` | Renderizar formulários, alertas, filtros, listas e dashboard |
| Controle web | `routes/auth_routes.py`, `discipline_routes.py`, `task_routes.py`, `main_routes.py` | Interpretar formulários, consultar sessão e acionar persistência e domínio |
| API | `routes/api_routes.py` | Expor recursos JSON, exigir sessão e responder com status HTTP |
| Domínio | `services/task_service.py` | Validar entradas, calcular percentual e urgência, filtrar tarefas |
| Persistência | `edutask/models.py` | Abrir SQLite, criar tabelas e carregar dados fictícios |

O fluxo típico de uma inclusão é: o navegador envia um formulário; a rota verifica a sessão e a entrada; as regras de domínio validam os valores; uma consulta parametrizada grava no banco; a rota redireciona com feedback; e a tela seguinte consulta e exibe os dados. Na API, os resultados são retornados em JSON, com os códigos HTTP correspondentes.

Essa separação permite testar funções de domínio sem navegador, rotas com persistência integrada e fluxos completos com Selenium ou inspeção interativa. Uma aprovação em um nível não substitui os demais: funções corretas podem estar ligadas a rotas incorretas, e respostas de API corretas não demonstram, por si só, a clareza da interface.

### 2.3 Modelo de dados e integridade

| Tabela | Campos e regras relevantes | Relações |
|---|---|---|
| `users` | id, name, email único, password_hash, role, created_at | Um usuário possui disciplinas e tarefas |
| `disciplines` | id, code único, name, teacher, workload_hours, user_id | Referencia users; pode ser referenciada por tarefas |
| `tasks` | id, title, description, due_date, priority, status, discipline_id, user_id, urgency_score, urgency_level, created_at | Referencia disciplina e usuário |

Os valores de status são Pendente, Em Andamento e Concluída. As prioridades são Baixa, Média e Alta. Restrições CHECK reforçam esses domínios no banco. A conexão ativa chaves estrangeiras com PRAGMA foreign_keys=ON. A aplicação bloqueia a exclusão de uma disciplina com tarefas vinculadas.

Os códigos de disciplinas permanecem únicos globalmente, conforme o esquema atual; não são apenas únicos por usuário. A revisão restringiu consultas e alterações ao proprietário dos dados. A configuração DATABASE é lida por instância da aplicação, permitindo que dois testes ou aplicações tenham bancos diferentes sem compartilhar registros.

### 2.4 Sessão e segurança observada

A autenticação verifica a senha contra o hash armazenado. A sessão guarda a identificação do usuário autenticado. Rotas privadas da interface redirecionam ao login, e endpoints da API sem sessão retornam 401. Recursos pertencentes a outra pessoa não são retornados ou alterados pelas operações cobertas nos testes.

As consultas usam parâmetros, sem concatenar diretamente a entrada do usuário em valores SQL. A variável SECRET_KEY deve ser configurada para qualquer uso além da demonstração. O servidor de desenvolvimento e as credenciais fictícias não representam uma configuração de produção pública.

## 3 Escopo requisitos e riscos

### 3.1 Escopo incluído e excluído

Foram incluídos os módulos de usuários, disciplinas, tarefas, urgência, dashboard, filtros e API. Foram excluídos pagamentos, envio real de e-mails, aplicações móveis nativas, integrações institucionais reais, testes destrutivos em terceiros e uma auditoria completa de segurança. O ambiente utiliza apenas dados fictícios e execução local ou no runner de CI.

### 3.2 Catálogo de requisitos verificáveis

{''.join(requirements)}

RF-05 mantém seu significado de atualização de status e percentual. O cálculo de urgência complementa RF-04 e mitiga R-07. RNF-02 mantém PBKDF2-SHA256 conforme a especificação original. O cadastro e o seed usam o método explicitamente; hashes antigos são atualizados após login válido, sem alterar a senha. A migração foi verificada nos caminhos web e API.

### 3.3 Matriz de riscos

| Risco | Descrição | Probabilidade e impacto | Prioridade |
|---|---|---|---|
{chr(10).join(risks)}

A escala é qualitativa, conforme o documento P02, sem inventar pontuações numéricas. Armazenamento inseguro é verificado pelo hash após cadastro; acesso indevido é confrontado com requisições sem sessão e de outro usuário; entradas inválidas são tratadas com classes e limites; duplicidade é exercitada com código existente; vínculos são testados na exclusão; contagens inconsistentes são rejeitadas; urgência usa fronteiras de datas; e desempenho é medido por requisições repetidas.

## 4 Planejamento dos testes

### 4.1 Estratégia e níveis

Os testes unitários verificam regras puras com entradas pequenas e determinísticas. A integração exercita o cliente Flask, as rotas e um banco SQLite real em arquivo temporário. O sistema é verificado com quatro fluxos Selenium, incluindo navegação, formulários e resultados visíveis. Os cenários de aceitação técnica verificam objetivos do estudante; a inspeção interativa complementa as asserções com leitura do feedback e capturas.

O catálogo de 24 casos foi integralmente selecionado para reexecução automatizada nesta revisão. Por isso, a taxa de automação do catálogo usa 24 como denominador. O mínimo obrigatório de 15 testes automatizados do manual não foi tratado como se fosse um plano do grupo para produzir artificialmente uma taxa de 120%.

### 4.2 Ambiente e dados

O ambiente local verificado usa Python 3.13.2 e Windows 11, com Flask e SQLite. O runner remoto utiliza Ubuntu e Python 3.13, conforme o workflow. O navegador local e suas capacidades estão registrados em `09_SISTEMA_INTERFACE/evidencias/navegador.json`; os testes remotos preservam seus próprios artefatos.

Cada teste integrado recebe banco temporário, com um usuário de demonstração, duas disciplinas e três tarefas iniciais. O Selenium cria servidor próprio em porta livre e não exige um processo na porta 5000. A inspeção interativa usou outra instância descartável, na porta 5011, acumulando apenas seus dados de cenário. Nenhum desses procedimentos exige apagar o banco de demonstração.

### 4.3 Critérios de entrada saída suspensão e retomada

Critérios de entrada: dependências instaladas, aplicação inicializável, dados fictícios e configurações de isolamento válidas. Critérios de saída técnica: cenários planejados executados, resultados aprovados, ausência de ocorrências Flake8 e latências dentro do limite na carga definida. Critérios documentais: vínculos entre requisitos e evidências, arquivos íntegros e limitações identificadas.

Interrompe-se a rodada afetada quando servidor, driver ou banco ficam indisponíveis. A causa é corrigida antes de repetir as verificações pertinentes. Durante a revisão houve incompatibilidade de driver e instabilidade de preenchimento nos testes iniciais do Selenium; a execução final utilizou driver compatível e preenchimento controlado, com duas execuções consecutivas aprovadas antes da publicação.

### 4.4 Responsabilidades e acompanhamento

O plano original organiza Gabriel Henrique Moreira em planejamento, João Lucas de Antonio Boconcelo em automação e Lucas Braga em análise e execução. Esses papéis não são prova de presença em cada atividade. O diário final contém os fatos verificáveis da revisão e deixa a participação individual e as horas para conferência dos próprios integrantes.

## 5 Técnicas e especificação dos casos

### 5.1 Particionamento de equivalência

Foram escolhidas classes de e-mails válidos/inválidos, senhas com e sem componentes obrigatórios, códigos no formato aceito e códigos malformados, usuários existentes/inexistentes e buscas com/sem correspondência. A estratégia reduz repetições de entradas que exercitam a mesma regra sem assumir que um único valor cobre todos os casos possíveis.

### 5.2 Análise de valores limite

A carga horária é verificada em 14, 15, 400 e 401 horas. A senha de sete caracteres representa a classe imediatamente abaixo do mínimo de oito. Para urgência, os testes usam datas a -1, 0, 1, 2, 3, 7 e 8 dias do dia de referência, cobrindo as transições das faixas. O percentual de conclusão verifica coleção vazia, valores normais e contagens impossíveis.

### 5.3 Tabela de decisão e transições

| Status selecionado | Prioridade selecionada | Condição para aparecer |
|---|---|---|
| Pendente | Alta | Satisfazer ambos os critérios |
| Pendente | Baixa | Pendente e Baixa |
| Concluída | Alta | Concluída e Alta |
| Concluída | Baixa | Apenas registros com essa combinação, ou lista vazia |
| Todos | Todas | Aplicar somente busca textual, se informada |

O teste de filtro verifica inclusive ausência de correspondências. A inspeção preparou uma tarefa Pendente/Alta antes de aplicar o filtro, evitando tratar uma lista vazia como evidência suficiente da lógica de combinação. As transições de status são observadas na tarefa e no valor matemático do dashboard.

### 5.4 Rastreabilidade e referência ao catálogo

O apêndice A incorpora os 24 casos detalhados. O arquivo P05 relaciona os seis requisitos funcionais, os dois não funcionais e os oito riscos aos seus testes e fontes de resultado. O catálogo apresenta responsáveis planejados; o registro de execução identifica o executor técnico real, sem converter planejamento em participação comprovada.

## 6 Execução pela interface e defeitos

### 6.1 Procedimento da inspeção interativa

Em 11/11/2026 foram percorridos os 24 casos com navegação e preenchimento da interface. O executor foi um assistente de validação técnica a pedido do solicitante. Foram observados o resultado de cada ação, as mensagens, as listas e os percentuais. Para cada caso foram salvos PNG, snapshot textual e JSON com data, método, executor, esperado e obtido.

Essa rodada é distinta da reexecução automatizada com Flask e dos quatro fluxos Selenium. Ela não é atribuída a um estudante e não representa homologação humana. Os relatos históricos sem capturas contemporâneas não foram somados às métricas confirmadas; a entrega final usa o registro atual verificável.

| Caso | Resultado observado na interface |
|---|---|
{uirows}

### 6.2 Diferenças entre validação do navegador e do servidor

Em CT-002, CT-014, CT-016 e CT-021 o navegador impediu o envio antes do backend, por e-mail sem @, carga abaixo de 15, carga acima de 400 e data obrigatória vazia. O resultado funcional foi atendido, mas o feedback é nativo e não a mensagem flash do servidor. O catálogo foi esclarecido para representar essa diferença real.

A reexecução por cliente Flask não aplica as restrições HTML e por isso continua necessária: ela confirma que os mesmos valores inválidos também são rejeitados no backend. A combinação das duas verificações demonstra a defesa nas duas camadas sem confundir seus mecanismos.

### 6.3 Registro e correção dos defeitos

Os seis defeitos foram registrados depois de observados na revisão. Os quatro primeiros foram corrigidos na rodada inicial; DEF-07 e DEF-08 foram corrigidos na rodada complementar. A linha de base de referência é o commit `a0df9e6a2dd69687bc88222fca707bdc6f877583`. A correção foi publicada no commit `33d441c7f6dc4599da735727f232c5c1aa5d41f3`. As quatro primeiras issues foram encerradas após aprovação remota. As duas complementares foram encerradas após correção publicada no commit 4acc9d5, aprovação local dos 145 cenários e reteste remoto aprovado na execução 43099616601. Os metadados ficam na pasta 06.

| Defeito | Severidade | Correção | Issue |
|---|---|---|---|
| DEF-03 Contagem inconsistente com total zero | Média | Validar concluídas maior que total antes de tratar coleção vazia | #1 |
| DEF-04 Configuração de banco ignorada | Média | Ler DATABASE por instância e inicializar em contexto | #2 |
| DEF-05 API e dados sem isolamento adequado | Alta | Exigir sessão e restringir consultas e alterações ao proprietário | #3 |
| DEF-06 Data inválida provoca exceção | Alta | Responder HTTP 400 sem persistência | #4 |
| DEF-07 JSON ou credenciais com tipo inválido | Média | Validar contrato antes de acessar campos e responder 400 | #6 |
| DEF-08 Hash divergente do RNF-02 original | Média | PBKDF2 explícito e migração transparente após login válido | #7 |

Os detalhes reproduzíveis estão no apêndice B e no P07. Severidade descreve o impacto; prioridade orienta a ordem de correção. O registro local conserva o identificador DEF, enquanto o número da ferramenta é o número da issue. Os dois não são intercambiáveis.

## 7 Automação e reprodutibilidade

### 7.1 Inventário dos cenários

| Conjunto | Cenários executados | Propósito |
|---|---|---|
| Unidade | {summary['unidade']} | Regras de validação, cálculo, filtros, fronteiras e regressão TDD |
| Integração e API | {summary['integracao']} | Comunicação de rotas, domínio e banco, incluindo sessão, proprietário, tipos de JSON, migração de hash e fluxos alternativos |
| Reexecução do catálogo | 24 | Confrontar cada CT com resposta e persistência |
| Aceitação técnica | 4 | Exercitar objetivos do estudante |
| Sistema com Selenium | 4 | Completar fluxos reais de navegador com verificações |
| Total automatizado | {summary['tests']['total']} | Todos aprovados, sem casos ignorados na consolidação local |

Os casos parametrizados são contados por combinação executada, não como funções independentes. A inspeção interativa de 28 cenários é um conjunto adicional de observações, sem alterar o total de testes pytest. Os XMLs permitem conferir os nomes e os resultados individuais.

### 7.2 Qualidade das asserções

O teste positivo de criação de disciplina exige HTTP 201; uma resposta 409 não pode mais substituir o sucesso de cadastro. Os testes negativos verificam ausência de persistência. A validação do dashboard compara o percentual exato calculado por concluídas/total. Os testes de isolamento criam dois usuários ou duas aplicações e verificam que um não lê nem altera os dados do outro.

As fronteiras de urgência usam uma data de referência fixa no teste unitário. Datas correntes são usadas apenas quando o objetivo é observar o comportamento da execução naquele dia, como na interface. Na API, urgência é recalculada ao consultar a tarefa, evitando devolver uma pontuação armazenada que já ficou desatualizada.

### 7.3 Instruções principais

Executar da raiz do projeto, com as dependências da pasta 01 instaladas:

```powershell
python -m pip install -r 01_SISTEMA_ALVO/requirements.txt
python -m pytest -v
python -m flake8 01_SISTEMA_ALVO/edutask --config=01_SISTEMA_ALVO/.flake8
```

O pytest.ini limita a coleta às cinco pastas de testes e exclui diretórios de evidências e dependências. Para executar somente um nível, informar a pasta 07, 08, 09 ou 10. O arquivo de reexecução dos 24 CTs fica na pasta 05. O Chrome deve estar instalado para os testes de sistema; o Selenium Manager pode precisar de rede para obter o driver compatível na primeira execução.

## 8 Integração API e sistema

### 8.1 Contratos da API

| Método e rota | Objetivo | Respostas relevantes |
|---|---|---|
| POST /api/auth/login | Autenticar com e-mail e senha | 200 válido, 400 ausência de campos, 401 credenciais inválidas |
| GET /api/disciplinas | Consultar disciplinas do usuário | 200 autenticado, 401 sem sessão |
| POST /api/disciplinas | Criar disciplina | 201 válida, 400 regra inválida, 409 código duplicado |
| GET /api/tarefas | Consultar tarefas e filtros | 200 com dados do proprietário, 401 sem sessão |
| POST /api/tarefas | Criar tarefa e calcular urgência | 201 válida, 400 entrada inválida, 404 disciplina não acessível |
| GET /api/tarefas/id | Consultar uma tarefa | 200 própria, 404 ausente ou de outro usuário |
| PUT /api/tarefas/id | Atualizar status e prioridade | 200 válida, 400 valor inválido, 404 não acessível |
| DELETE /api/tarefas/id | Remover tarefa própria | 200 removida, 404 não acessível |
| GET /api/metricas | Consultar contagens e percentual | 200 com indicadores do usuário, 401 sem sessão |

A autenticação da API usa cookies de sessão. Na coleção Postman, executar o login válido primeiro e manter os cookies. A coleção e o ambiente são arquivos JSON editáveis. A revisão não apresenta uma execução Newman como se tivesse sido realizada: o resultado comprovado de integração vem dos testes Python e do pipeline.

### 8.2 Fluxos de sistema

E2E-01 verifica login, painel e logout, incluindo retorno ao login ao tentar abrir uma rota privada. E2E-02 cadastra uma disciplina e confirma código e nome na tabela. E2E-03 cadastra uma tarefa e verifica o título na lista. E2E-04 conclui uma tarefa e confronta o percentual esperado com a barra do dashboard.

O servidor do Selenium utiliza porta livre e banco temporário. As esperas são explícitas, os recursos são encerrados ao final e as capturas preservam o que foi exibido. A rotina utiliza preenchimento controlado de campos e submissão do formulário; não pretende avaliar habilidade de digitação ou comportamento de tecnologia assistiva.

## 9 Aceitação e verificações não funcionais

### 9.1 Critérios de aceitação observados

Os quatro objetivos do estudante foram verificados tanto na suíte quanto na inspeção de interface. UAT-01 reaproveita o usuário cadastrado no CT-001 e confirma primeiro login e painel próprio vazio. UAT-02 cria sua disciplina. UAT-03 cria uma entrega para dois dias depois e verifica Alta Urgência. UAT-04 conclui sua única tarefa e verifica 100% de progresso.

| Cenário | Resultado observado | Evidência na pasta 10 |
|---|---|---|
{scenarios}

A decisão é técnica, baseada na correspondência entre critério e interface. O campo de homologação humana não foi preenchido em nome de um integrante. Essa distinção permite aproveitar as evidências sem inventar a presença de um representante externo ou sua assinatura.

### 9.2 Desempenho TNF 01 e TNF 02

O procedimento faz três requisições de aquecimento e 30 medições por rota, em HTTP real de loopback, com um cliente sequencial. A base contém um usuário, duas disciplinas e três tarefas. O cronômetro usa perf_counter_ns e converte a duração para milissegundos. Cada amostra registra rota, repetição, status HTTP, tempo e quantidade de bytes.

| Rota | N | Mínimo ms | Média ms | P95 ms | Máximo ms |
|---|---|---|---|---|---|
{latency}

Todas as amostras ficaram abaixo de 500 ms, atendendo RNF-01 na carga documentada. O P95 é o 29º valor da lista ordenada de 30 amostras, método do posto mais próximo. Essa medição não é tempo de renderização completa do navegador, não inclui internet e não demonstra capacidade sob concorrência ou volume elevado.

Reprodução: `python tools/medir_qualidade.py`. Fontes: `latencias_http.csv` e `desempenho.json` na pasta 11. O ambiente e a data de medição constam do JSON, permitindo distinguir novas medições de resultados preservados.

### 9.3 Usabilidade TNF 03 e TNF 04

TNF-03 inspeciona a navegação dos fluxos centrais, a disponibilidade dos controles e a capacidade de chegar aos resultados. Na instância de inspeção, o menu compacto foi expandido para acessar opções de sessão. Os fluxos foram completados e suas telas registradas. Isso é uma inspeção técnica de navegação, não uma pesquisa com amostra de usuários.

TNF-04 verifica feedback de validação: senhas curtas ou sem símbolo, divergência de confirmação, login inválido, código de disciplina fora do padrão, duplicidade, título curto, limites de carga e data obrigatória. As mensagens nativas e as mensagens flash foram distinguidas. Os alertas do template possuem role=alert; contraste e leitores de tela não foram medidos nesta revisão.

### 9.4 Segurança TNF 05 e TNF 06

TNF-05 cadastra um usuário, consulta password_hash em banco temporário, exige o prefixo PBKDF2-SHA256, rejeita senha em texto claro e confirma a verificação da senha. O seed segue o mesmo algoritmo, e os testes verificam migração de hashes antigos após login válido, tanto pela interface quanto pela API. TNF-06 verifica ausência de sessão, tentativa de acesso a registros de outro usuário e entradas de SQL injection sem autenticação ou alteração indevida da base.

Os testes não constituem pentest completo. Permanecem fora da validação uma defesa CSRF dedicada, limitação de tentativas, implantação HTTPS e configurações de produção. Por esse motivo o parecer de uso se limita ao laboratório acadêmico controlado.

## 10 Métricas indicadores e análise estática

### 10.1 Indicadores obrigatórios

| Indicador | Fórmula e universo | Resultado | Fonte |
|---|---|---|---|
| Percentual de execução | CTs reexecutados / CTs planejados | 24/24 = 100% | catálogo e XML |
| Taxa de aprovação | CTs aprovados / CTs executados | 24/24 = 100% | catalogo.xml |
| Taxa de reprovação | CTs reprovados / CTs executados | 0/24 = 0% | catalogo.xml |
| Cobertura de requisitos | Requisitos com verificação executada / escopo | 8/8 = 100% | P05, testes e latências |
| Taxa de automação | CTs automatizados / CTs selecionados para automação | 24/24 = 100% | P03 e script da pasta 05 |
| Defeitos por severidade | Contagem dos seis confirmados | 4 médios, 2 altos | issues e P07 |
| Defeitos por status | Contagem após reteste | 6 encerrados, 0 abertos | GitHub Issues |
| Taxa de reabertura | Defeitos reabertos / retestados | 0/6 = 0% | registros da revisão |

A planilha Planilha_Metricas.xlsx contém dados identificados e 12 fórmulas, incluindo os indicadores de execução, aprovação, reprovação, requisitos, automação, defeitos, cobertura de linhas e aprovação da suíte. Os indicadores por severidade/status são contagens. Os dados históricos sem evidência não foram incorporados aos seis defeitos confirmados.

### 10.2 Cobertura de código e seus limites

Linhas executadas: {cov['covered_lines']}/{cov['num_statements']} = **{linepercent:.2f}%**. Ramos cobertos: {cov['covered_branches']}/{cov['num_branches']} = **{cov['percent_branches_covered']:.2f}%**. A cobertura foi medida na suíte sem Selenium; os XMLs do navegador são contabilizados separadamente.

Cobertura de requisito e cobertura de código são medidas diferentes. Um requisito com ao menos um teste não significa que todas as suas alternativas foram exercitadas. Da mesma forma, uma linha executada não prova que todos os seus resultados foram confrontados com uma asserção. O JSON de cobertura preserva informações por arquivo e linhas não cobertas.

### 10.3 Análise estática antes e depois

Foram usadas a mesma configuração Flake8 e a mesma largura máxima de 120 caracteres. A linha de base apresentou 179 ocorrências; a execução após a revisão não apresentou ocorrências. Foram corrigidos espaços residuais, importações não usadas, exportações de pacote e linhas excessivamente longas.

O workflow usa o código de saída real do Flake8, sem --exit-zero. Portanto, uma ocorrência faz a etapa falhar. Não foi apresentada medição Radon ou complexidade ciclomática que não tenha sido executada; o relatório se limita aos instrumentos e dados efetivamente disponíveis.

![Figura 1 Reexecução dos casos do catálogo](11_METRICAS_E_QUALIDADE/grafico_aprovacao_casos.png)

![Figura 2 Distribuição dos cenários automatizados](11_METRICAS_E_QUALIDADE/grafico_automacao_niveis.png)

![Figura 3 Severidade dos defeitos confirmados](11_METRICAS_E_QUALIDADE/grafico_defeitos_severidade.png)

## 11 TDD integração contínua e melhoria

### 11.1 Experiência TDD com commits cronológicos reais

O comportamento escolhido foi rejeitar corpos JSON não objeto e credenciais de tipos não textuais com resposta HTTP 400. Antes da correção, entradas como [1], texto, números e campos email/password não textuais podiam provocar exceção. Os testes de integração foram escritos e executados antes da implementação e registrados no primeiro commit do ciclo.

| Etapa | Commit | Data e fuso | Resultado real |
|---|---|---|---|
{tddrows}

RED registrou 17 falhas e três aprovações: as falhas revelaram erros do comportamento existente. GREEN implementou a guarda mínima de JSON e tipos de credenciais, aprovando os 20 cenários. REFACTOR extraiu a validação para a função pura json_payload_error, preservando as 20 aprovações. São três commits reais e sucessivos; não foram criados retrospectivamente como se fossem históricos de outubro.

Links verificáveis dos commits:

{tddlinks}

Os arquivos red/green/refactor.txt e .xml, além de commits.json, ficam em 12_TDD_CICD_MELHORIA/evidencias/tdd_json. A primeira experiência com cálculo de percentual continua como evidência complementar de logs/snapshots, mas a comprovação principal do requisito TDD agora é este ciclo com Git. A falha intencional de CI descrita a seguir tem outra finalidade e não é confundida com um defeito encontrado por TDD.

### 11.2 Pipeline real no GitHub Actions

O arquivo canônico é `.github/workflows/ci.yml`, na raiz do repositório. Os gatilhos são push e pull_request em main/develop, além de workflow_dispatch. O job faz checkout, configura Python 3.13, instala dependências, executa Flake8, unidade, integração/catálogo/aceitação, Selenium e upload dos artefatos. O resumo usa o estado real do job.

| Execução | Commit | Conclusão | Run ID |
|---|---|---|---|
{runrows}

URLs verificáveis:

- Revisão publicada aprovada: {github['execucoes']['principal']['url']}
- Falha intencional detectada: {github['execucoes']['falha_controlada']['url']}
- Correção aprovada: {github['execucoes']['correcao']['url']}
- Suíte ampliada e PBKDF2 aprovados: {github['execucoes']['complementar']['url']}
- PR de demonstração encerrado sem merge: https://github.com/joaoboconcelo/edutask-tqs-p2/pull/5

O teste temporário continha assert False e falhou na etapa de testes unitários, como planejado. Depois de removido, o pipeline voltou a passar. A versão principal permaneceu funcional. Os logs originais do GitHub foram baixados e extraídos na pasta 12 para que a comprovação não dependa apenas de um ícone na interface.

### 11.3 Plano de melhoria

| Prioridade | Ação | Critério de verificação |
|---|---|---|
| Alta | Conferir aprovação docente, homologação e assinaturas | Registros reais das pessoas responsáveis |
| Alta | Adicionar proteção CSRF antes de exposição pública | POST sem token rejeitado, regressão aprovada |
| Média | Paginar consultas e avaliar 500 registros | Medição por volume e comparação com a base pequena |
| Média | Empacotar Bootstrap e ícones localmente | Fluxos estilizados com rede externa desativada |
| Média | Ampliar caminhos ainda não cobertos | Novas asserções de comportamento e cobertura conferida |
| Baixa | Avaliar PostgreSQL conforme concorrência necessária | Ensaio comparativo antes da decisão de migração |

Publicação, issues e demonstração de CI estão concluídas. Os responsáveis individuais pelas próximas atividades devem ser confirmados pelo grupo, sem atribuição de execução ou horas por inferência.

## 12 Discussão dos resultados e riscos residuais

Os resultados mais relevantes são a correção de falhas reais de isolamento e validação, o fortalecimento das asserções, a preservação de dados brutos e a demonstração remota de que o pipeline aceita uma versão correta e bloqueia uma regressão intencional. A inspeção da interface acrescenta observações sobre mensagens nativas e navegação que o cliente Flask não reproduz.

Os {summary['tests']['total']} cenários aprovados não provam ausência geral de falhas. A cobertura de linhas e ramos é parcial, o desempenho foi medido em carga pequena, a interface usa recursos externos por CDN e a segurança não foi auditada de forma exaustiva. Esses limites orientam o plano de melhoria e restringem o parecer ao uso acadêmico local.

O solicitante não confirmou aprovação docente ou validações humanas anteriores. Por isso, a ficha do professor, o aceite humano e as assinaturas permanecem sem preenchimento. Os registros interativos deixam explícito o executor técnico. A entrega oficial no Google Drive e a conferência de permissões e prazo também não são substituídas pela publicação no GitHub.

## 13 Conclusão e parecer de qualidade

A versão revisada apresenta comportamento aprovado nos cenários selecionados, rastreabilidade entre requisitos e evidências, métricas calculadas a partir de resultados preservados, defeitos acompanhados na ferramenta e execução real de CI. A estrutura final conserva as 17 pastas do manual, elimina duplicatas de relatório e mantém o material necessário para instalação, execução e avaliação.

O parecer é favorável ao uso do EduTask Web no laboratório acadêmico dentro do escopo testado. A conclusão deve ser lida com as limitações de cobertura, carga e segurança apresentadas. As confirmações humanas e a aprovação docente dependem das pessoas responsáveis; o relatório não apresenta declarações ou assinaturas em nome delas.

## Referências

SILVA, Elvio Gilberto da. Testes e Qualidade de Software Projeto P2. Manual fornecido pelo professor, 2026. Critérios, estrutura e modelos das seções 9 a 16 e apêndices.

EduTask Web. Código-fonte e documentos P01 a P14 desta entrega. Linha de base a0df9e6 e revisão publicada 33d441c. Repositório: https://github.com/joaoboconcelo/edutask-tqs-p2 .

Evidências efetivamente utilizadas: relatórios JUnit XML; JSON de cobertura e ambiente; CSV de latências; logs Flake8; snapshots de TDD; capturas e metadados da inspeção interativa; issues #1, #2, #3, #4, #6 e #7; runs de CI e PR #5 indicados na seção 11.

<!-- pagebreak -->

## Apêndice A Catálogo completo dos 24 casos

Os responsáveis indicados neste catálogo são papéis previstos no planejamento. Os resultados da rodada atual, método e executor estão no P06 e na seção 6. As diferenças de feedback nativo foram explicitadas após a inspeção.

{catalog}

<!-- pagebreak -->

## Apêndice B Registros detalhados dos defeitos

{defecttext}

Vínculos: DEF-03 = issue #1; DEF-04 = #2; DEF-05 = #3; DEF-06 = #4; DEF-07 = #6; DEF-08 = #7. URLs completas e metadados estão no P07 e no diretório de evidências da pasta 06.

<!-- pagebreak -->

## Apêndice C Evidências visuais selecionadas

As capturas completas da inspeção por caso ficam nas pastas 05 e 10. As figuras abaixo exemplificam autenticação, cadastro de disciplina, criação de tarefa e progresso no conjunto Selenium. Foram selecionadas as capturas desse conjunto para manter legibilidade no papel. São imagens reais do sistema no navegador, não reconstruções.

![Figura 4 Painel após autenticação válida E2E 01](09_SISTEMA_INTERFACE/evidencias/E2E-01-login.png)

![Figura 5 Disciplina cadastrada e conferida na lista E2E 02](09_SISTEMA_INTERFACE/evidencias/E2E-02-disciplina.png)

![Figura 6 Tarefa criada pela interface E2E 03](09_SISTEMA_INTERFACE/evidencias/E2E-03-tarefa.png)

![Figura 7 Percentual recalculado após concluir tarefa E2E 04](09_SISTEMA_INTERFACE/evidencias/E2E-04-dashboard.png)

<!-- pagebreak -->

## Apêndice D Instalação execução e organização da entrega

### Ambiente e versões verificadas

| Dependência | Versão local |
|---|---|
{versionrows}

Os requisitos declaram versões mínimas e as versões verificadas estão registradas no JSON de ambiente. A versão do driver deve ser compatível com o Chrome instalado. O primeiro uso pode precisar de rede; os testes de API não precisam do navegador.

### Instalação configuração e execução

```powershell
python -m venv .venv
.venv/Scripts/Activate.ps1
python -m pip install -r 01_SISTEMA_ALVO/requirements.txt
python 01_SISTEMA_ALVO/run.py
```

Abrir http://127.0.0.1:5000 . Usuário fictício: aluno@unisagrado.edu.br. Senha fictícia: Senha@123. O banco de demonstração é criado automaticamente em 01_SISTEMA_ALVO/edutask.db. Não é necessário apagar esse banco para rodar os testes, que usam configurações isoladas.

O valor de SECRET_KEY pode ser definido no ambiente. Para reinicializar somente a demonstração, parar o servidor, remover apenas o arquivo edutask.db e reiniciar. Dados de usuários reais não devem ser usados no laboratório. Datas iniciais são fixas, enquanto o cálculo de urgência acompanha a data de consulta.

### Comandos de verificação

```powershell
python -m pytest -v 07_AUTOMACAO_UNITARIA
python -m pytest -v 08_INTEGRACAO_API
python -m pytest -v 05_EXECUCAO_MANUAL/test_reexecucao_catalogo.py
python -m pytest -v 09_SISTEMA_INTERFACE
python -m pytest -v 10_ACEITACAO_NAO_FUNCIONAIS
python tools/medir_qualidade.py
python tools/verificar_pipeline.py
```

### Organização final das pastas

| Pasta | Conteúdo necessário |
|---|---|
| 00_IDENTIFICACAO_E_README | Identificação, ficha docente, instruções, confirmações restantes e minuta de entrega |
| 01_SISTEMA_ALVO | Aplicação, templates, dependências e configuração de análise |
| 02_REQUISITOS_ESCOPO_RISCOS | Oito requisitos e oito riscos priorizados |
| 03_PLANO_DE_TESTES | Estratégia, ambiente, dados, critérios e responsabilidades planejadas |
| 04_CASOS_E_RASTREABILIDADE | Catálogo, matriz e CSV editável |
| 05_EXECUCAO_MANUAL | Registro atual de inspeção, 24 capturas e reexecução automatizada |
| 06_DEFEITOS | Seis defeitos, exportação e metadados das issues |
| 07_AUTOMACAO_UNITARIA | Trinta cenários unitários |
| 08_INTEGRACAO_API | Testes integrados, coleção e ambiente Postman |
| 09_SISTEMA_INTERFACE | Quatro fluxos Selenium e suas evidências |
| 10_ACEITACAO_NAO_FUNCIONAIS | Cenários, critérios não funcionais e quatro capturas de aceitação técnica |
| 11_METRICAS_E_QUALIDADE | Planilha com fórmulas, gráficos, latências, cobertura e relatórios |
| 12_TDD_CICD_MELHORIA | Ciclo TDD, logs, metadados e evidências do Actions |
| 13_RELATORIO_FINAL | Relatório canônico completo em DOCX e PDF e fonte de geração |
| 14_APRESENTACAO_E_VIDEO_CONTINGENCIA | Registro da dispensa, sem materiais antigos divergentes |
| 15_DIARIO_DE_PARTICIPACAO | Atividades verificáveis e declaração para conferência/assinatura |
| 16_BACKUP_ENTREGA | Checklist, manifesto SHA-256 e pacote de backup |

Os utilitários de tools apoiam medição, reprodução e geração documental. Caches, bancos temporários, dependências instaladas localmente, cópias de relatório, slides dispensados e arquivos transitórios de publicação não fazem parte da entrega final.

### Evidências e integridade

O manifesto SHA-256 identifica os conteúdos do pacote de backup, excluindo o próprio manifesto e o ZIP. O empacotador verifica a integridade do arquivo e compara os hashes de cada item. O ZIP não contém banco local, ambiente virtual ou credenciais. Os metadados de GitHub preservam IDs, commits e conclusões para consulta posterior.

### Confirmações finais

Antes da entrega oficial, o grupo deve conferir a ficha docente, o atendimento do RNF-02 original, eventual licença de redistribuição, participação, assinaturas, dispensa de apresentação e permissões do Drive. O comprovante é uma minuta e deve receber data e hora reais somente após o envio. Nenhum desses atos foi antecipado no relatório.
'''


def add_text(paragraph,text):
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1 (\2)',text).replace('<br>',' ')
    for token in re.split(r'(\*\*.*?\*\*|`[^`]+`)',text):
        if not token:continue
        if not token.startswith(('**','`')) and re.search(r'https?://',token):
            for piece in re.split(r'(https?://[^\s<>]+)',token):
                if piece.startswith(('https://','http://')):
                    url=piece.rstrip('.,;)' )
                    link=OxmlElement('w:hyperlink')
                    link.set(qn('r:id'),paragraph.part.relate_to(url,RT.HYPERLINK,is_external=True))
                    run=OxmlElement('w:r');props=OxmlElement('w:rPr')
                    color=OxmlElement('w:color');color.set(qn('w:val'),'000000');props.append(color)
                    underline=OxmlElement('w:u');underline.set(qn('w:val'),'single');props.append(underline)
                    run.append(props);content=OxmlElement('w:t');content.text=url;run.append(content);link.append(run);paragraph._p.append(link)
                    if len(url)<len(piece):paragraph.add_run(piece[len(url):])
                elif piece:paragraph.add_run(piece)
            continue
        run=paragraph.add_run(token[2:-2] if token.startswith('**') else token[1:-1] if token.startswith('`') else token)
        if token.startswith('**'):run.bold=True
        if token.startswith('`'):run.font.name='Consolas';run.font.size=Pt(9)


def build_document(markdown):
    doc=Document(); sec=doc.sections[0]
    sec.page_width,sec.page_height=Cm(21),Cm(29.7)
    sec.top_margin=sec.bottom_margin=Cm(2)
    sec.left_margin=sec.right_margin=Cm(2.1)
    for style in doc.styles:
        if hasattr(style,'font'):
            style.font.name='Calibri';style.font.color.rgb=RGBColor(0,0,0)
    normal=doc.styles['Normal'];normal.font.size=Pt(10.5)
    normal.paragraph_format.space_after=Pt(6)
    normal.paragraph_format.line_spacing=1.08
    for name,size in [('Heading 1',16),('Heading 2',12.5),('Heading 3',11.5)]:
        doc.styles[name].font.size=Pt(size)
        doc.styles[name].paragraph_format.keep_with_next=True
        doc.styles[name].paragraph_format.space_before=Pt(12)
    sec.header.paragraphs[0].text='UNISAGRADO | Testes e Qualidade de Software | Grupo 01'
    sec.header.paragraphs[0].runs[0].font.size=Pt(8)
    footer=sec.footer.paragraphs[0];footer.text='EduTask Web v1.0.1-p2 | 11/11/2026 | Página '
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
    doc.add_paragraph('UNISAGRADO\nCiência da Computação\nTestes e Qualidade de Software',style='Subtitle')
    doc.add_paragraph('Relatório técnico completo do EduTask Web',style='Title')
    doc.add_paragraph('Projeto Integrado P2 | Turma A | Grupo 01')
    doc.add_paragraph('Professor Prof Dr Elvio Gilberto da Silva')
    doc.add_paragraph('Gabriel Henrique Moreira\nJoão Lucas de Antonio Boconcelo\nLucas Braga')
    doc.add_paragraph('Bauru SP\n11 de novembro de 2026')
    doc.add_paragraph('Planejamento, execução, automação e avaliação de qualidade com evidências locais e remotas. Versão revisada v1.0.1-p2. Os resultados e seus limites estão descritos nas seções e apêndices.')
    doc.add_page_break()
    doc.add_heading('Sumário',level=1)
    toc=OxmlElement('w:fldSimple');toc.set(qn('w:instr'),'TOC \\o "1-2" \\h \\z \\u');doc.add_paragraph()._p.append(toc)
    doc.add_page_break()
    lines=markdown.splitlines();i=0;in_code=False
    while i<len(lines):
        line=lines[i].strip();i+=1
        if line.startswith('# '):continue
        if line.startswith('```'):
            in_code=not in_code;continue
        if in_code:
            p=doc.add_paragraph();p.paragraph_format.space_after=Pt(1)
            r=p.add_run(line);r.font.name='Consolas';r.font.size=Pt(8.5);continue
        if not line:continue
        if line=='<!-- pagebreak -->':doc.add_page_break();continue
        if line=='---':continue
        image=re.fullmatch(r'!\[([^]]+)\]\(([^)]+)\)',line)
        if image:
            path=(ROOT/image.group(2)).resolve();path.relative_to(ROOT)
            # Limitar altura de capturas para manter imagem e legenda juntas.
            from PIL import Image
            with Image.open(path) as im:w,h=im.size
            width=min(15.5,14.0*w/h)
            p=doc.add_paragraph();p.paragraph_format.keep_with_next=True
            p.add_run().add_picture(str(path),width=Cm(width))
            p=doc.add_paragraph(image.group(1));p.style=doc.styles['Caption'];continue
        if line.startswith('|'):
            rows=[line]
            while i<len(lines) and lines[i].strip().startswith('|'):rows.append(lines[i].strip());i+=1
            data=[[c.strip() for c in r.strip('|').split('|')] for r in rows if not re.fullmatch(r'\|?[\s:|\-]+\|?',r)]
            if not data:continue
            columns=len(data[0]);table=doc.add_table(rows=0,cols=columns)
            table.alignment=WD_TABLE_ALIGNMENT.CENTER;table.autofit=False
            for j,row in enumerate(data):
                cells=table.add_row().cells
                trpr=table.rows[-1]._tr.get_or_add_trPr();cant=OxmlElement('w:cantSplit');trpr.append(cant)
                if j==0:trpr.append(OxmlElement('w:tblHeader'))
                for k,cell in enumerate(cells):
                    cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
                    cell.width=Cm(16.8/columns)
                    add_text(cell.paragraphs[0],row[k] if k<len(row) else '')
                    for p in cell.paragraphs:
                        p.paragraph_format.space_after=Pt(4);p.paragraph_format.space_before=Pt(4)
                        if j==0:p.paragraph_format.keep_with_next=True
                        for r in p.runs:r.font.size=Pt(8.5 if columns>=5 else 9)
                    props=cell._tc.get_or_add_tcPr()
                    shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'333333' if j==0 else 'F1F1F1' if j%2 else 'FFFFFF');props.append(shade)
                    borders=OxmlElement('w:tcBorders')
                    for edge in ['top','left','bottom','right']:
                        node=OxmlElement('w:'+edge);node.set(qn('w:val'),'single');node.set(qn('w:sz'),'4');node.set(qn('w:color'),'D9D9D9');borders.append(node)
                    props.append(borders)
                    if j==0:
                        for r in cell.paragraphs[0].runs:r.bold=True;r.font.color.rgb=RGBColor(255,255,255)
            doc.add_paragraph().paragraph_format.space_after=Pt(2)
            continue
        heading=re.match(r'^(#{2,4}) (.+)$',line)
        if heading:
            title=heading.group(2).replace('**','').replace(':','').replace('`','')
            doc.add_heading(title,level=min(len(heading.group(1))-1,3));continue
        bullet=re.match(r'^(?:\* |- |\d+\. )(.*)$',line)
        if bullet:
            p=doc.add_paragraph(style='List Bullet') if line.startswith(('* ','- ')) else doc.add_paragraph()
            add_text(p,bullet.group(1) if line.startswith(('* ','- ')) else line)
        else:add_text(doc.add_paragraph(),line)
    for element in [doc._element,doc.styles.element]:
        for border in element.xpath('.//w:pBdr'):border.getparent().remove(border)
    doc.core_properties.title='Relatório técnico completo do EduTask Web'
    doc.core_properties.author='Grupo 01 Turma A'
    doc.core_properties.subject='Projeto Integrado P2 de Testes e Qualidade de Software'
    doc.save(OUT/'RELATORIO_FINAL_PROJETO_P2.docx')


if __name__=='__main__':
    content=source_markdown()
    (OUT/'RELATORIO_FINAL_PROJETO_P2.md').write_text(content,encoding='utf-8')
    build_document(content)
    print('Relatório completo gerado:',len(content.split()),'palavras, com catálogo e evidências.')
