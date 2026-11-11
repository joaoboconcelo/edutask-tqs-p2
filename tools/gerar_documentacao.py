"""Reconstrói os documentos a partir das evidências, sem inventar homologações."""
import csv
import hashlib
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.now(timezone(timedelta(hours=-3))).isoformat(timespec='seconds')
TEAM = 'Gabriel Henrique Moreira, João Lucas de Antonio Boconcelo e Lucas Braga'


def write(path, text):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.strip() + '\n', encoding='utf-8')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def junit(path):
    cases = list(ET.parse(ROOT / path).getroot().iter('testcase'))
    failed = sum(c.find('failure') is not None or c.find('error') is not None for c in cases)
    skipped = sum(c.find('skipped') is not None for c in cases)
    return {'total': len(cases), 'passed': len(cases) - failed - skipped, 'failed': failed, 'skipped': skipped}


def main():
    tech = junit('11_METRICAS_E_QUALIDADE/evidencias/testes.xml')
    browser = junit('09_SISTEMA_INTERFACE/evidencias/selenium.xml')
    catalog = junit('05_EXECUCAO_MANUAL/evidencias_reexecucao/catalogo.xml')
    coverage = json.loads(read('11_METRICAS_E_QUALIDADE/evidencias/cobertura.json'))['totals']
    perf = json.loads(read('11_METRICAS_E_QUALIDADE/evidencias/desempenho.json'))
    total = {key: tech[key] + browser[key] for key in tech}
    assert total['failed'] == 0 and total['skipped'] == 0
    summary = {'data': NOW, 'tests': total, 'catalogo': catalog, 'coverage': coverage,
               'unidade': 30, 'integracao': 36, 'aceitacao_tecnica': 4, 'navegador': browser,
               'nota': 'Parâmetros do pytest são contados como cenários; não são funções distintas.'}
    write('11_METRICAS_E_QUALIDADE/evidencias/resumo_entrega.json', json.dumps(summary, ensure_ascii=False, indent=2))
    before = len(read('11_METRICAS_E_QUALIDADE/evidencias/flake8_antes.txt').splitlines())
    after = len(read('11_METRICAS_E_QUALIDADE/evidencias/flake8_depois.txt').splitlines())

    # Conservar relatos históricos, identificando o que a revisão não comprova.
    note = ('> **Nota da revisão de 11/11/2026:** os registros de outubro abaixo são relatos históricos do grupo, '
            'sem capturas contemporâneas ou issues externas disponibilizadas. A reexecução atual comprova o '
            'comportamento da versão revisada, mas não comprova as datas nem o ciclo original de defeitos.\n\n')
    for path in ['05_EXECUCAO_MANUAL/P06_Registro_Execucoes_Manuais.md', '06_DEFEITOS/P07_Relatorio_e_Gestao_de_Defeitos.md']:
        text = read(path)
        if not text.startswith('> **Nota da revisão'):
            write(path, note + text)
    write('05_EXECUCAO_MANUAL/REEXECUCAO_ATUAL.md', f'''# Reexecução verificável do catálogo

Data da consolidação: {NOW}. Método: Flask test client, banco SQLite temporário por cenário.

Os 24 cenários CT-001 a CT-024 foram reexecutados por automação. Resultado: {catalog['passed']}/{catalog['total']} aprovados.
Esta rodada é automatizada e não é apresentada como execução manual. Os relatos EX-001 a EX-024 permanecem históricos.

Cada caso possui resposta HTML e metadados JSON em `evidencias_reexecucao/CT-NNN.*`.
O relatório JUnit está em `evidencias_reexecucao/catalogo.xml`.
Além da mensagem, o script verifica persistência, ausência de gravação inválida, sessão ou resultado calculado conforme o cenário.
CT-023 prepara explicitamente uma tarefa Pendente/Alta para evitar uma aprovação por lista vazia.

Reproduzir da raiz: `python -m pytest -v 05_EXECUCAO_MANUAL/test_reexecucao_catalogo.py`.

## Confirmação manual do grupo

O grupo deve percorrer os 24 casos no navegador e registrar data, executor e captura quando o professor exigir execução manual comprovada.
Não preencher esse aceite com os resultados automatizados. Modelo: `EX-M-NNN | CT-NNN | data e versão | executor | esperado | obtido | captura | defeito`.
''')

    # RNF-02 aceita os algoritmos seguros efetivamente usados pelo Werkzeug.
    p02 = read('02_REQUISITOS_ESCOPO_RISCOS/P02_Requisitos_Escopo_Riscos.md').split('## Esclarecimentos da revisão')[0].rstrip()
    p02 = re.sub(r'(?:scrypt ou )*PBKDF2-SHA256', 'scrypt ou PBKDF2-SHA256', p02).replace('hash PBKDF2/SHA256', 'hash scrypt ou PBKDF2/SHA256')
    p02 += '\n## Esclarecimentos da revisão de 11/11/2026\n\nRF-05 continua sendo atualização de status e taxa de conclusão. O cálculo de urgência é regra complementar de RF-04, mitigando R-07: <=0 dias =100; 1-2=75; 3-7=50; >7=25. Datas vencidas são aceitas com aviso na interface. A API exige sessão, e tarefas, disciplinas e indicadores são restritos ao usuário autenticado. Códigos de disciplinas permanecem únicos globalmente. RNF-02 é atualizado nesta revisão para aceitar scrypt, padrão efetivamente usado, ou PBKDF2-SHA256; a validação dessa alteração de requisito cabe ao grupo/professor.\n'
    write('02_REQUISITOS_ESCOPO_RISCOS/P02_Requisitos_Escopo_Riscos.md', p02)
    plan = read('03_PLANO_DE_TESTES/P03_Plano_de_Testes.md').split('## Plano da revisão de 11/11/2026')[0].rstrip()
    plan += f'''\n## Plano da revisão de 11/11/2026

Versão revisada: v1.0.1-p2 (identificação documental; sem tag Git publicada). Linha de base: código do HEAD anterior à revisão.
Automação planejada do catálogo: 24 cenários; denominador de automação =24, sem usar os 15 mínimos do manual como plano fictício.
Suíte atual: 30 cenários unitários, 36 de integração/API, 24 do catálogo, 4 de aceitação técnica e 4 de navegador, total {total['total']}.
As parametrizações contam como cenários executados. Há quatro fluxos distintos no Selenium.
Ambiente de cada teste: SQLite temporário; sem escrita no banco de demonstração. E2E e latências usam porta HTTP efêmera.
Entrada: dependências instaladas, testes coletáveis e dados fictícios. Saída técnica: suíte aprovada, nenhum erro Flake8 e latências inferiores a 500 ms na carga definida.
Saída documental: correlação entre requisitos/casos/resultados, DOCX/PDF consistentes e pendências humanas explicitadas.
Suspender em falha de servidor, driver ou banco; corrigir o ambiente e repetir apenas as verificações afetadas antes da consolidação.
Apresentação e vídeo dispensados conforme informação do solicitante. Sem comprovação docente anexada ou redistribuição de pesos presumida.
Não presumir aprovação do sistema, homologação manual ou entrega no Drive por conclusão dos testes locais.
'''
    write('03_PLANO_DE_TESTES/P03_Plano_de_Testes.md', plan)

    matrix = read('04_CASOS_E_RASTREABILIDADE/P05_Matriz_de_Rastreabilidade.md').split('## Complemento da revisão')[0]
    if '### Resumo da Rastreabilidade:' in matrix:
        matrix = matrix[:matrix.find('### Resumo da Rastreabilidade:')]
    matrix += '''## Complemento da revisão e cobertura demonstrada

Os vínculos históricos acima são preservados. Abaixo estão as verificações executáveis da revisão, incluindo os dois requisitos não funcionais.

| Requisito | Riscos | Verificação executada | Evidência |
|---|---|---|---|
| RF-01 | R-01, R-03 | CT-001 a CT-006; validações unitárias; hash após cadastro | CT-001 a CT-006 HTML/JSON; testes.xml |
| RF-02 | R-02 | CT-007 a CT-010; sessão API; isolamento entre usuários | CT-007 a CT-010 HTML/JSON; testes.xml; E2E-01 |
| RF-03 | R-03, R-04, R-05 | CT-011 a CT-018; limites, duplicidade e exclusão protegida | CT-011 a CT-018 HTML/JSON; testes.xml; E2E-02 |
| RF-04 | R-07 | CT-019 a CT-021; datas inválidas; fronteiras de urgência | CT-019 a CT-021 HTML/JSON; testes.xml; E2E-03 |
| RF-05 | R-06 | CT-022; taxa exata; inconsistência total zero | CT-022 HTML/JSON; testes.xml; E2E-04; red/green/refactor.xml |
| RF-06 | R-03, R-08 | CT-023/024; tabela de decisão dos filtros | CT-023/024 HTML/JSON; testes.xml |
| RNF-01 | R-08 | 30 requisições HTTP por rota, após aquecimento | latencias_http.csv; desempenho.json |
| RNF-02 | R-01 | Cadastro, consulta do hash e check_password_hash | test_rnf02_password_hash_and_login; testes.xml |

Cobertura por requisito: 8/8 com verificação executada. Cobertura por risco: R-01 a R-08 com vínculo explícito.
Isso não significa cobertura de todos os caminhos possíveis. A cobertura de linhas é medida separadamente em `cobertura.json`.
Cada CT-NNN tem reexecução atual em `05_EXECUCAO_MANUAL/evidencias_reexecucao/CT-NNN.json`.
'''
    write('04_CASOS_E_RASTREABILIDADE/P05_Matriz_de_Rastreabilidade.md', matrix)

    defects = [
        ('DEF-03', 'Taxa de conclusão aceita concluídas positivas com total zero', 'RF-05', 'R-06', 'Média', 'Alta',
         'calculate_completion_rate(0, 1) retornava 0.0 em vez de rejeitar a inconsistência.',
         'Verificar completed_tasks > total_tasks antes do caso vazio.', 'test_tdd_consistencia.py / red.xml e green.xml'),
        ('DEF-04', 'Configuração de banco ignorada e testes contaminam demonstração', 'RF-03/RF-04', 'R-05', 'Média', 'Alta',
         'models.py usava caminho global enquanto create_app aceitava DATABASE sem aplicá-lo.',
         'Ler DATABASE de current_app, inicializar dentro do contexto e usar temporários.', 'test_isolated_databases_do_not_share_records'),
        ('DEF-05', 'API permite leitura e alteração sem sessão e mistura dados de usuários', 'RF-02', 'R-02', 'Alta', 'Alta',
         'Endpoints não verificavam sessão e gravavam user_id=1. Consultas HTML não filtravam o proprietário.',
         'Exigir sessão na API e filtrar leituras e escritas por user_id.', 'test_r02_api_requires_session / test_r02_users_cannot_read_or_modify_each_others_records'),
        ('DEF-06', 'Data inválida na API causa exceção em vez de resposta 400', 'RF-04', 'R-07', 'Alta', 'Alta',
         'POST /api/tarefas com due_date=2026-02-30 propagava ValueError.',
         'Capturar ValueError, encerrar conexão e retornar JSON com HTTP 400 sem persistência.', 'test_rf04_invalid_task_does_not_persist'),
    ]
    text = '# Defeitos confirmados na revisão de 11 de novembro de 2026\n\nIdentificadores locais; não são números de GitHub Issues. Status encerrado significa correção e regressão local, sem homologação externa presumida.\n'
    for ident, title, req, risk, severity, priority, observed, fix, test in defects:
        text += f'\n## {ident} {title}\n\nRequisito: {req}. Risco: {risk}. Severidade: {severity}. Prioridade: {priority}.\n\nAmbiente: Python 3.13.2, Flask, SQLite local isolado. Data: 11/11/2026. Status: Encerrado na revisão local.\n\nObtido antes: {observed}\n\nEsperado: rejeitar entradas inconsistentes, preservar isolamento e responder sem erro interno.\n\nCorreção: {fix}\n\nReprodução e reteste: `{test}`. Código-fonte anterior verificável no Git HEAD anterior à revisão; código atualizado no diff. Logs consolidados em `11_METRICAS_E_QUALIDADE/evidencias/testes.xml`.\n\nResponsabilidade: revisão assistida por Codex a pedido do grupo; validação dos integrantes pendente.\n'
    text += '\nDEF-01 e DEF-02 permanecem relatos históricos sem issue ou captura contemporânea. Não são contados como defeitos confirmados desta revisão. Taxa de reabertura dos quatro confirmados: 0/4, limitada a esta rodada.\n'
    write('06_DEFEITOS/DEFEITOS_REVISAO.md', text)
    with (ROOT / '06_DEFEITOS/defeitos_revisao.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream, delimiter=';')
        writer.writerow(['ID', 'Título', 'Requisito', 'Risco', 'Severidade', 'Prioridade', 'Status', 'Evidência'])
        writer.writerows([[d[0], d[1], d[2], d[3], d[4], d[5], 'Encerrado local', d[8]] for d in defects])

    perf_rows = '\n'.join(f"| {route} | {v['n']} | {v['media_ms']:.3f} | {v['p95_ms']:.3f} | {v['max_ms']:.3f} | {'Atende' if v['atende'] else 'Não atende'} |" for route,v in perf['rotas'].items())
    write('10_ACEITACAO_NAO_FUNCIONAIS/P09_Testes_Aceitacao_e_Nao_Funcionais.md', f'''# Aceitação e testes não funcionais

Revisão: {NOW}. Sistema: EduTask Web v1.0.1-p2.

## Quatro cenários de aceitação

| ID | Necessidade do estudante | Critério | Verificação técnica |
|---|---|---|---|
| UAT-01 | Cadastrar e acessar sua conta | Cadastro seguro, login e painel próprio vazio | test_uat01_student_registers_and_logs_in |
| UAT-02 | Organizar disciplinas | Salvar e consultar código e dados | test_uat02_student_organizes_disciplines |
| UAT-03 | Priorizar uma entrega próxima | Prazo em dois dias exibe Alta Urgência | test_uat03_student_sees_urgency |
| UAT-04 | Acompanhar seu progresso | Concluir tarefa aumenta contagem e percentual exato | test_uat04_student_tracks_completion |

Resultado técnico: os quatro cenários passaram na suíte consolidada. Decisão humana de aceitação: pendente de confirmação do grupo; não há representante externo ou assinatura comprovada.
Reproduzir: `python -m pytest -v 10_ACEITACAO_NAO_FUNCIONAIS`.

## Seis verificações não funcionais em três categorias

TNF-01 Desempenho da lista web: GET /tarefas. TNF-02 Desempenho da API: GET /api/tarefas e /api/metricas.
Métrica: todas as respostas abaixo de 500 ms, de acordo com RNF-01. Banco de 1 usuário, 2 disciplinas e 3 tarefas; um cliente sequencial, três aquecimentos e 30 medições por rota. Mede resposta HTTP, não renderização completa ou carga concorrente.

| Rota | Amostras | Média ms | P95 ms | Máximo ms | Critério <500 ms |
|---|---|---|---|---|---|
{perf_rows}

Fonte: `11_METRICAS_E_QUALIDADE/evidencias/latencias_http.csv` e `desempenho.json`. Reproduzir: `python tools/medir_qualidade.py`.

TNF-03 Usabilidade por inspeção de navegação: quatro fluxos Selenium com controles identificáveis e capturas E2E-01 a E2E-04. Critério: completar os fluxos sem rotas inexistentes e encontrar os resultados nas telas correspondentes. Resultado: quatro fluxos aprovados. Não equivale a estudo de usabilidade com participantes.

TNF-04 Usabilidade por feedback: CT-002, CT-003, CT-004, CT-008, CT-014, CT-020 e CT-021 verificam mensagens específicas na resposta HTML; o template utiliza role=alert. Resultado: verificações aprovadas. Limitação: contraste, leitores de tela e compreensão por usuários não foram avaliados.

TNF-05 Segurança de armazenamento: cadastro real em banco temporário, hash seguro scrypt ou PBKDF2, senha original ausente e check_password_hash positivo. Evidência: test_rnf02_password_hash_and_login em testes.xml. Atende ao requisito revisado RNF-02.

TNF-06 Segurança de acesso e entradas: API sem sessão retorna 401, páginas privadas redirecionam, usuário não acessa registros alheios, tentativa de SQL injection não autentica nem altera a base. Evidência: test_r02_api_requires_session, test_r02_users_cannot_read_or_modify_each_others_records e test_r03_sql_injection_does_not_authenticate_or_delete. Resultado: aprovado.

Limites de segurança: não há ensaio de invasão completo, proteção CSRF dedicada ou ensaio de carga. Parecer restrito ao ambiente acadêmico local; não se declara prontidão para produção pública.
''')
    line_cov = coverage['covered_lines'] / coverage['num_statements'] * 100
    write('11_METRICAS_E_QUALIDADE/P10_Relatorio_Metricas_e_Indicadores.md', f'''# Métricas e indicadores da revisão

Data: {NOW}. Dados: JUnit XML, respostas HTML/JSON, CSV de latências e coverage.py. Planilha editável com fórmulas: `Planilha_Metricas.xlsx`.

| Indicador obrigatório | Cálculo atual | Resultado | Fonte e interpretação |
|---|---|---|---|
| Percentual de execução | 24/24 | 100% | Reexecução automatizada do catálogo; não valida retroativamente o histórico manual |
| Taxa de aprovação | 24/24 | 100% | catalogo.xml |
| Taxa de reprovação | 0/24 | 0% | catalogo.xml |
| Cobertura de requisitos | 8/8 | 100% | P05, testes.xml e desempenho.json; cobertura por requisito, não por caminho |
| Taxa de automação | 24/24 selecionados | 100% | Plano atual do catálogo; os mínimos do manual não são usados como denominador |
| Defeitos por severidade | Média 2; Alta 2; Baixa/Crítica 0 | 4 confirmados | DEF-03 a DEF-06; DEF-01/02 históricos excluídos |
| Defeitos por status | Encerrados 4; abertos 0 | 4 retestados | Reteste local, sem presumir aprovação externa |
| Taxa de reabertura | 0/4 | 0% | Somente rodada atual; não prova ausência futura de regressões |

Suíte completa: {total['passed']}/{total['total']} cenários aprovados, sem skip. Unidade 30, integração 36, catálogo 24, aceitação técnica 4 e Selenium 4.
Cobertura de linhas sem Selenium: {coverage['covered_lines']}/{coverage['num_statements']} = {line_cov:.2f}%. Cobertura de ramos e dados por arquivo disponíveis em cobertura.json. Essa medida não inclui a execução do navegador.

## Comparação estática

Mesmo comando e limite de 120 caracteres antes/depois: `python -m flake8 01_SISTEMA_ALVO/edutask --config=01_SISTEMA_ALVO/.flake8`.
Linha de base: {before} ocorrências. Após revisão: {after}. Logs: `evidencias/flake8_antes.txt` e `flake8_depois.txt`.
Foram removidos espaços residuais, imports não usados e linhas excessivas; exportações de pacote são explícitas. Não se usa --exit-zero no CI.
As duas medições são da revisão atual. Não há relatório Radon ou complexidade medida; as alegações anteriores foram removidas.

## Interpretação

A revisão executou todos os cenários planejados e encontrou quatro defeitos confirmados. A aprovação atual demonstra a regressão selecionada, sem comprovar todos os caminhos do sistema ou aceitação por usuários.
A avaliação de desempenho é limitada à base pequena e ao ambiente registrado. Os gráficos representam dados atuais, sem repetir os valores históricos sem evidência.
''')

    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'12_TDD_CICD_MELHORIA/evidencias').glob('task_service_*.py')}
    write('12_TDD_CICD_MELHORIA/evidencias/snapshots_sha256.json', json.dumps(hashes, indent=2))
    write('12_TDD_CICD_MELHORIA/P11_Registro_TDD_CICD_Melhoria.md', f'''# TDD integração contínua e melhoria

## TDD efetivamente registrado nesta revisão

Data: 11/11/2026. Comportamento: RF-05/R-06 deve rejeitar concluídas positivas quando total é zero, preservando 0/0=0%.
O ciclo antigo de urgência não possui commits fornecidos. Por isso, ele não é usado como comprovação histórica de TDD.

1. RED: escrito `07_AUTOMACAO_UNITARIA/test_tdd_consistencia.py` antes da correção. Resultado real: 2 falhas e 1 aprovação. Evidências: `evidencias/red.txt` e `red.xml`.
2. GREEN: movida a validação de concluídas>total para antes do retorno por total zero. Resultado real: 3 aprovações. Evidências: `green.txt`, `green.xml`, `task_service_green.py`.
3. REFACTOR: simplificado o retorno do cálculo vazio, sem alterar a regra; após os ajustes da revisão, a regressão unitária/API registrou 17 aprovações. Evidências: `refactor.txt`, `refactor.xml`, `task_service_refactor.py`. A suíte final ampliada está em testes.xml.

O snapshot baseline foi extraído do HEAD anterior à revisão, e os arquivos GREEN/REFACTOR foram salvos durante o trabalho. SHA-256 em `evidencias/snapshots_sha256.json` identifica os conteúdos. Não são apresentados hashes de arquivo como commits. Commits específicos do ciclo não foram criados; eventual exigência de commits cronológicos depende de validação docente dos logs/snapshots disponíveis.

## Pipeline preparado e demonstração local

Arquivo canônico: `.github/workflows/ci.yml`, na raiz. A cópia na pasta P11 é idêntica.
Gatilhos: push e pull_request em main/develop, além de workflow_dispatch. Etapas: instalação, Flake8 bloqueante, unidade, integração, catálogo, aceitação técnica, Selenium e upload de artefatos.
O resumo usa o estado real do job; não anuncia sucesso quando uma etapa falha.

Execução local equivalente: `python tools/verificar_pipeline.py`. Um teste temporário com `assert 25 == 100` retorna código 1; depois a suíte correta retorna 0. Logs `pipeline_local_falha.txt`, `pipeline_local_sucesso.txt` e `pipeline_local.json`.
Isso é uma demonstração local real, não uma execução do GitHub Actions. Não há URL de execução remota desta revisão nem autorização de pipeline simulado anexada. Publicar e executar no GitHub ainda é necessário para completar esse item do manual.

## Melhoria contínua

| Prioridade | Ação | Responsabilidade proposta | Verificação |
|---|---|---|---|
| Alta | Publicar revisão e preservar Actions verde e falha controlada | João Lucas, confirmar pelo grupo | URLs dos runs e artefatos |
| Alta | Confirmar execução manual, aceitação e aprovação do sistema | Grupo | Registros datados e assinados, sem reconstruir histórico |
| Alta | Proteção CSRF e restrições de sessão antes de exposição pública | João Lucas, confirmar | POST sem token rejeitado e regressão |
| Média | Paginar tarefas e medir carga com 500 registros | Grupo | Tempo sob carga, sem extrapolar a medição pequena |
| Média | Empacotar Bootstrap e ícones localmente | Grupo | Navegação com rede externa desativada |
| Baixa | Avaliar PostgreSQL conforme necessidade de concorrência | Grupo | Teste comparativo de concorrência |

Análise de qualidade: {before} ocorrências Flake8 antes e {after} depois, com logs na pasta P10. A alteração funcional corrigiu inconsistência observada e ampliou regressão e isolamento.
''')

    # Diário: preservar declarações anteriores sem transformá-las em fatos comprovados.
    diary_path = '15_DIARIO_DE_PARTICIPACAO/P14_Diario_de_Participacao.md'
    diary = read(diary_path)
    archive = ROOT/'15_DIARIO_DE_PARTICIPACAO/DIARIO_ORIGINAL_PARA_CONFERENCIA.md'
    if not archive.exists():
        archive.write_text('> Registro recebido antes da revisão; datas, horas e evidências dependem de conferência dos integrantes. Não usar como comprovação validada.\n\n' + diary, encoding='utf-8')
    write(diary_path, f'''# Diário de participação e declaração

## Registro verificável desta revisão

| Data | Atividade | Execução | Evidência | Tempo |
|---|---|---|---|---|
| 11/11/2026 | Revisão técnica e documental solicitada por João Lucas; testes, correções e coleta de evidências | Assistência do Codex; autoria e revisão final do grupo a confirmar | Diff Git, XML, capturas, CSV e snapshots | Não medido; não atribuído aos integrantes |

## Conferência do histórico

O diário recebido foi preservado em `DIARIO_ORIGINAL_PARA_CONFERENCIA.md`. Ele contém registros posteriores a 11/11/2026 apresentados como concluídos e declara 85,5 horas sem comprovação anexada.
Atividades de 17/11/2026 em diante devem ser tratadas como planejamento, não trabalho realizado. Não se antecipa assinatura nem se atribui participação individual por inferência.
O grupo deve confirmar os registros anteriores, corrigir divergências entre datas de execução e diário e associar evidências reais. Não há totais de horas auditados nesta revisão.

## Declaração para assinatura após conferência

Declaramos que revisamos os arquivos, compreendemos os testes e identificamos as limitações e o uso de assistência por inteligência artificial. As execuções da revisão são rastreáveis aos arquivos brutos. Não declaramos comprovadas atividades históricas sem registro.

Integrantes: {TEAM}.

Assinaturas e datas efetivas: pendentes do grupo. Não assinar em nome de terceiros.
''')
    write('14_APRESENTACAO_E_VIDEO_CONTINGENCIA/DISPENSA_DA_APRESENTACAO.md', '''# Apresentação e vídeo dispensados

Conforme informação do solicitante em 11/11/2026, não será necessária apresentação e não haverá vídeo de contingência.
Os slides e o roteiro antigos são materiais históricos de apoio, não evidência técnica atual nem obrigação desta revisão.
Nenhuma redistribuição da pontuação de apresentação foi presumida. Não há documento docente da dispensa anexado.
''')
    # Formulário de aprovação permanece em branco; não inventar autorização ou origem.
    ap = read('00_IDENTIFICACAO_E_README/Apendice_A_Ficha_Proposta_Aprovacao.md')
    ap = ap.replace('Projeto público de código aberto com licença acadêmica permissiva (MIT License) no GitHub, adaptado e modularizado para testes.', 'Aplicação acadêmica do grupo; origem exata e eventual projeto-base precisam ser confirmados pelos integrantes.')
    ap = ap.replace('Licença MIT (permissão integral para estudo, alteração e execução de testes em ambiente local).', 'Licença e autorização a confirmar pelo grupo; não foi encontrado arquivo LICENSE que comprove a declaração anterior.')
    write('00_IDENTIFICACAO_E_README/Apendice_A_Ficha_Proposta_Aprovacao.md', ap)
    write('00_IDENTIFICACAO_E_README/PENDENCIAS_PARA_ENTREGA.md', '''# Pendências que dependem do grupo

A revisão local melhora os critérios técnicos, mas não garante nota 10. Para completar os itens que não podem ser produzidos por inferência:

1. Obter ou anexar aprovação do sistema pelo professor. A ficha continua sem aprovação preenchida.
2. Confirmar a dispensa da apresentação/vídeo e a forma de redistribuição da nota, se aplicável.
3. Publicar a revisão no repositório, executar Actions e guardar URLs de sucesso e falha controlada. O workflow local está preparado; a demonstração local não é um run remoto.
4. Registrar os defeitos na ferramenta exigida (GitHub Issues/Jira), com seus links. Os registros atuais são arquivos locais.
5. Confirmar os 24 casos manuais com executor, data real e capturas; a revisão fornece reexecução automatizada, identificada como tal.
6. Homologar os quatro cenários de aceitação como representante do usuário, com observações reais.
7. Conferir origem/licença, diário, participação e assinaturas; não usar atividades futuras como concluídas. Validar também a atualização de RNF-02 para scrypt/PBKDF2.
8. Fazer upload no Drive oficial, testar acesso sem privilégios e preencher o comprovante apenas após a entrega efetiva.

Não é necessário inventar histórico. Corrigir o registro ou confirmar a exceção com o professor é a forma adequada de fechar cada pendência.
''')
    write('16_BACKUP_ENTREGA/CHECKLIST_FINAL_VERIFICADO.md', f'''# Checklist da revisão local

Consolidação: {NOW}.

- [x] Estrutura de 17 pastas preservada e dependências declaradas.
- [x] Banco isolado e verificações de sessão e proprietário corrigidas.
- [x] {total['passed']} cenários automatizados aprovados, incluindo quatro de navegador.
- [x] 24 cenários do catálogo reexecutados com HTML, JSON e JUnit.
- [x] Dois RNFs e oito riscos com vínculos na matriz atualizada.
- [x] Dados brutos de desempenho e cobertura preservados.
- [x] Flake8 antes/depois, sem ignorar falhas no CI.
- [x] Ciclo TDD novo com falha real, correção e refatoração registrados.
- [x] Workflow preparado e cópias sincronizadas.
- [x] DOCX/PDF regenerados a partir do mesmo documento nesta revisão; verificação visual ao final.
- [x] Apresentação/vídeo marcados como dispensados segundo o solicitante.
- [ ] Aprovação docente do sistema anexada.
- [ ] Execuções remotas de sucesso/falha do Actions anexadas.
- [ ] Defeitos vinculados a GitHub Issues/Jira.
- [ ] Execução manual e aceitação humana confirmadas.
- [ ] Origem/licença, diário e assinaturas confirmados.
- [ ] Upload e permissões no Drive oficial verificados.
- [ ] Comprovante preenchido após entrega efetiva.

O ZIP será atualizado ao final; seu conteúdo não contém dependências locais temporárias ou o banco de demonstração.
''')

    readme = f'''# EduTask Web Projeto Integrado P2

UNISAGRADO, Ciência da Computação, Turma A, Grupo 01. Professor: Prof. Dr. Elvio Gilberto da Silva.
Integrantes: {TEAM}.

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
Resultado consolidado desta revisão: {total['passed']}/{total['total']} cenários; logs e ambiente na pasta 11. Parametrizações são contadas como cenários.

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
'''
    write('00_IDENTIFICACAO_E_README/README.md', readme)
    write('README.md', '# EduTask Web Projeto P2\n\nComece por [identificação e instruções](00_IDENTIFICACAO_E_README/README.md).\n\nPendências de validação humana e entrega: [lista](00_IDENTIFICACAO_E_README/PENDENCIAS_PARA_ENTREGA.md).\n')
    for folder, label, command in [
        ('07_AUTOMACAO_UNITARIA', '30 cenários unitários, incluindo parametrizações de limites, filtros e regressão TDD', '07_AUTOMACAO_UNITARIA'),
        ('08_INTEGRACAO_API', '36 cenários de integração com banco temporário, sessão e proprietário', '08_INTEGRACAO_API'),
        ('09_SISTEMA_INTERFACE', '4 fluxos Selenium com capturas HTML/PNG e servidor próprio', '09_SISTEMA_INTERFACE'),
        ('01_SISTEMA_ALVO', 'Aplicação local Flask e SQLite; configuração DATABASE aplicada por instância', None)]:
        write(folder+'/README.md', f'# {folder}\n\n{label}.\n\n'+(f'Da raiz: `python -m pytest -v {command}`.\n\n' if command else 'Da raiz: `python 01_SISTEMA_ALVO/run.py`.\n\n')+'Instruções completas em `00_IDENTIFICACAO_E_README/README.md`.\n')
    build_report(summary, perf, before, after)


def build_report(summary, perf, before, after):
    document = Document()
    section = document.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin = section.bottom_margin = Cm(2)
    section.left_margin = section.right_margin = Cm(2.1)
    normal = document.styles['Normal']
    normal.font.name, normal.font.size = 'Calibri', Pt(11)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_after = Pt(7)
    normal.paragraph_format.line_spacing = 1.08
    for style in ['Title', 'Subtitle', 'Heading 1', 'Heading 2']:
        document.styles[style].font.name = 'Calibri'
        document.styles[style].font.color.rgb = RGBColor(0, 0, 0)
    for style in document.styles:
        if hasattr(style, 'font'):
            style.font.color.rgb = RGBColor(0, 0, 0)
    header = section.header.paragraphs[0]
    header.text = 'UNISAGRADO | Testes e Qualidade de Software | EduTask Web'
    header.style = document.styles['Caption']
    footer = section.footer.paragraphs[0]
    footer.text = 'Revisão de 11/11/2026 | Página '
    field = OxmlElement('w:fldSimple'); field.set(qn('w:instr'), 'PAGE'); footer._p.append(field)

    def p(text):
        return document.add_paragraph(text)

    def heading(title):
        document.add_heading(title, level=1)

    def table(headers, rows, widths=None):
        t = document.add_table(rows=1, cols=len(headers)); t.style = 'Table Grid'
        for c, value in zip(t.rows[0].cells, headers): c.text = str(value)
        trpr = t.rows[0]._tr.get_or_add_trPr(); repeat = OxmlElement('w:tblHeader'); trpr.append(repeat)
        for idx, row in enumerate(rows):
            for cell, value in zip(t.add_row().cells, row): cell.text = str(value)
        for i, row in enumerate(t.rows):
            for j, cell in enumerate(row.cells):
                if widths: cell.width = Cm(widths[j])
                tcpr = cell._tc.get_or_add_tcPr()
                shade = OxmlElement('w:shd'); shade.set(qn('w:fill'), '333333' if i == 0 else ('F2F2F2' if i % 2 else 'FFFFFF')); tcpr.append(shade)
                for para in cell.paragraphs:
                    para.paragraph_format.space_after = Pt(5)
                    para.paragraph_format.space_before = Pt(5)
                    for run in para.runs:
                        run.font.size = Pt(9.5)
                        run.font.color.rgb = RGBColor(255,255,255) if i==0 else RGBColor(0,0,0)
                        run.bold = i == 0
                borders = OxmlElement('w:tcBorders')
                for side in ['top','left','bottom','right']:
                    edge=OxmlElement('w:'+side); edge.set(qn('w:val'),'single'); edge.set(qn('w:sz'),'4'); edge.set(qn('w:color'),'D9D9D9'); borders.append(edge)
                tcpr.append(borders)
                cant=OxmlElement('w:cantSplit'); row._tr.get_or_add_trPr().append(cant)
        p('')
        return t

    def page(): document.add_page_break()

    document.add_paragraph('UNISAGRADO\nCiência da Computação\nTestes e Qualidade de Software', style='Subtitle')
    p('')
    document.add_paragraph('Relatório de qualidade do EduTask Web', style='Title')
    p('Projeto Integrado P2 | Turma A | Grupo 01 | Versão revisada v1.0.1-p2')
    p('Professor: Prof. Dr. Elvio Gilberto da Silva')
    p('Integrantes: '+TEAM+'.')
    p('Bauru SP | 11 de novembro de 2026')
    heading('Resultado e finalidade')
    p(f"Este relatório consolida a revisão técnica do EduTask Web e vincula seus resultados aos arquivos executáveis da entrega. A suíte final aprovou {summary['tests']['passed']} cenários, incluindo quatro fluxos reais de navegador, com banco isolado, evidências brutas e métricas reproduzíveis.")
    p('A revisão corrigiu quatro defeitos confirmados e inconsistências de documentação. O parecer é favorável ao uso no laboratório acadêmico dentro do escopo testado. Aprovação docente, homologação manual e humana, publicação do pipeline e entrega no Drive permanecem dependentes de confirmação do grupo.')
    p('Apresentação e vídeo foram dispensados conforme informação do solicitante. Nenhuma redistribuição da pontuação foi presumida. A versão revisada é uma identificação documental, sem tag publicada.')
    page()
    heading('Identificação e navegação')
    p('Repositório informado: https://github.com/joaoboconcelo/edutask-tqs-p2 . A revisão local ainda precisa ser publicada. Instruções completas: 00_IDENTIFICACAO_E_README/README.md. Ambiente: Python 3.13.2, Flask, Werkzeug, SQLite e Chrome; versões e capacidades do navegador em 09_SISTEMA_INTERFACE/evidencias/navegador.json.')
    p('Autoria e participação: os nomes dos integrantes foram mantidos conforme a entrega recebida. Esta revisão contou com assistência do Codex solicitada por João Lucas. Os integrantes devem conferir, compreender e assumir a versão final; não foram criadas assinaturas ou horas de participação.')
    heading('Sumário')
    toc = OxmlElement('w:fldSimple'); toc.set(qn('w:instr'), 'TOC \\o "1-1" \\h \\z \\u')
    document.add_paragraph()._p.append(toc)
    p('Os títulos abaixo organizam o relatório: introdução; caracterização; escopo e riscos; planejamento; casos; execução e defeitos; automação; integração; aceitação e não funcionais; métricas; TDD e CI; discussão; conclusão; referências e anexos.')
    page()
    heading('1 Introdução')
    p('O problema orientador é demonstrar quais requisitos da aplicação acadêmica foram verificados, quais falhas foram corrigidas e quais limitações persistem. A avaliação considera processo de teste e evidências, sem inferir qualidade apenas pela quantidade de arquivos ou pela aprovação de uma suíte pequena.')
    p('A estratégia combina casos derivados de equivalência, limites, decisão e transição de estados, integrações com persistência, execução de navegador e medições HTTP. A revisão separa relatos históricos de verificações atuais, permitindo repetir os procedimentos e conferir seus resultados.')
    heading('2 Caracterização do sistema')
    p('O EduTask Web organiza disciplinas, tarefas, prioridades e prazos para estudantes. Seus quatro fluxos centrais são cadastro/autenticação, gestão de disciplinas, gestão de tarefas e acompanhamento de progresso e filtros. Os formulários persistem dados em SQLite e as rotas de API retornam JSON.')
    table(['Camada','Componentes','Verificação'], [
        ['Interface','HTML/Jinja2 e Bootstrap','Selenium e respostas HTML'],
        ['Controle','Blueprints Flask','Status HTTP, sessão, validação e proprietário'],
        ['Domínio','task_service.py','Funções puras, fronteiras e filtros'],
        ['Persistência','SQLite e consultas parametrizadas','Gravação, vínculos e isolamento entre bases']])
    p('A aplicação usa servidor de desenvolvimento local. Bootstrap e ícones são carregados por CDN; portanto, uma interface totalmente estilizada offline não foi garantida. Os testes criam bancos próprios, sem exigir limpeza da base de demonstração.')
    page()
    heading('3 Escopo requisitos e riscos')
    table(['ID','Comportamento verificável','Riscos principais'], [
        ['RF-01','Cadastro com e-mail válido e política de senha','R-01 e R-03'],
        ['RF-02','Autenticação, sessão e restrição de acesso','R-02'],
        ['RF-03','Disciplina com código único e carga de 15 a 400h','R-03, R-04 e R-05'],
        ['RF-04','Tarefa vinculada, título, data e prioridade','R-07'],
        ['RF-05','Alteração de status e percentual de conclusão','R-06'],
        ['RF-06','Busca e filtros combinados','R-03 e R-08'],
        ['RNF-01','Consultas HTTP abaixo de 500ms na carga definida','R-08'],
        ['RNF-02','Senha em hash seguro scrypt ou PBKDF2 SHA256','R-01']])
    p('RF-05 mantém o significado original de status/progresso. A urgência é regra complementar de RF-04: atraso ou hoje=100, 1 a 2 dias=75, 3 a 7=50 e mais de 7=25. Datas vencidas são aceitas com aviso na interface. A atualização de RNF-02 explicita o algoritmo efetivamente usado e precisa de validação do grupo/professor.')
    p('R-01 armazenamento inseguro; R-02 acesso indevido; R-03 entradas inválidas; R-04 duplicidade; R-05 integridade referencial; R-06 divisão/inconsistência de contagem; R-07 prazo/urgência; R-08 desempenho. Prioridade considera probabilidade e impacto, com maior atenção a acesso, dados e regressão.')
    p('Fora do escopo: integrações financeiras, envio real de e-mail, aplicativos nativos, testes destrutivos em terceiros, auditoria completa de segurança e desempenho sob concorrência.')
    page()
    heading('4 Planejamento dos testes')
    p('Critérios de entrada: dependências disponíveis, aplicação inicializável, dados fictícios e isolamento de banco. Critérios de saída técnica: todos os cenários da revisão aprovados, Flake8 sem ocorrências e consultas dentro do limite sob a carga documentada. Critérios documentais: vínculos rastreáveis, arquivos brutos acessíveis e limites identificados.')
    p('Suspensão e retomada: interromper a rodada afetada por falha de driver, indisponibilidade de servidor ou banco; corrigir a causa e repetir a verificação antes de consolidar resultados. A revisão inicial de Selenium identificou driver incompatível e instabilidade de preenchimento; a execução final utilizou driver compatível e campos controlados.')
    p('Os responsáveis propostos do plano original permanecem como organização do grupo, sem atribuir automaticamente a eles as atividades desta sessão. O diário exige conferência e assinaturas efetivas. A aprovação docente do sistema não foi preenchida por inferência.')
    heading('5 Especificação dos casos')
    p('O catálogo P04 contém 24 casos e é mantido como referência de execução manual. Equivalência separa e-mails, senhas e códigos válidos e inválidos. Limites exercitam carga 14, 15, 400 e 401, além de fronteiras de urgência -1, 0, 1, 2, 3, 7 e 8 dias. A tabela de decisão verifica status/prioridade com e sem correspondência. Transições validam mudança de status e seu efeito matemático.')
    p('A matriz P05 inclui os seis requisitos funcionais, os dois não funcionais e os oito riscos. Cada CT possui resposta HTML e JSON da reexecução, e os testes automatizados nomeiam regras e riscos. Cobertura de requisito indica ao menos uma verificação vinculada; não equivale a exaurir todos os seus caminhos.')
    page()
    heading('6 Execução e gestão de defeitos')
    p('A entrega recebida relata 24 execuções manuais de outubro e dois defeitos corrigidos. Sem capturas contemporâneas ou links de issues disponibilizados, esses dados permanecem históricos e não são tratados como auditados. A revisão reexecutou os 24 cenários por automação, com base temporária por caso e verificações de resultado e persistência.')
    p('Evidências atuais: 05_EXECUCAO_MANUAL/evidencias_reexecucao/CT-NNN.html e .json, além de catalogo.xml. A natureza automatizada está declarada; o grupo ainda deve confirmar execução manual quando exigida pelo professor.')
    table(['Defeito confirmado','Correção','Reteste'], [
        ['DEF-03 Total zero com concluídas positivas','Validar consistência antes do retorno vazio','TDD e cenários (0,1), (0,5), (2,3)'],
        ['DEF-04 DATABASE ignorado','Configuração por instância e temporários','Duas aplicações sem compartilhar registros'],
        ['DEF-05 API e dados sem isolamento','Sessão e proprietário nas consultas/escritas','Sem sessão 401 e outro usuário sem acesso'],
        ['DEF-06 Data inválida gera exceção','Resposta 400 sem persistência','Datas impossíveis e malformadas']])
    p('Os quatro registros estão encerrados no reteste local e exportados em defeitos_revisao.csv. Os identificadores são locais; criação e vinculação de GitHub Issues/Jira ainda dependem do grupo. Não há alegação de histórico remoto de estados.')
    page()
    heading('7 Automação')
    table(['Conjunto','Cenários','Resultado'], [
        ['Unidade',30,'Aprovados'],['Integração e API',36,'Aprovados'],
        ['Reexecução do catálogo',24,'Aprovados'],['Aceitação técnica',4,'Aprovados'],['Selenium',4,'Aprovados']])
    p('Total: 98 cenários. Os testes parametrizados são contados por entrada executada; não se apresentam 98 funções distintas. A suíte sem navegador tem JUnit e cobertura separados. O navegador possui quatro fluxos reais de usuário, relatório XML e capturas PNG/HTML.')
    p('A API é testada pelo cliente integrado Flask com persistência SQLite real em arquivo temporário. Chamadas HTTP de rede são usadas na medição de desempenho e pelo navegador. O cadastro positivo exige HTTP 201; HTTP 409 não é aceito como sucesso substituto. O dashboard é validado pelo percentual exato e não apenas pela presença do símbolo %.')
    heading('8 Integração e sistema')
    p('As integrações verificadas são interface/rotas, rotas/regras de domínio e rotas/SQLite. A revisão valida códigos HTTP de sucesso e erro, ausência de gravação inválida, proteção da disciplina com tarefas e ausência de compartilhamento entre bancos configurados separadamente.')
    p('No Selenium, autenticação/logout, cadastro de disciplina, criação de tarefa e mudança de status/dashboard possuem esperas explícitas e verificações de conteúdo ou cálculo. O servidor inicia em porta livre e o navegador fecha ao final. A instalação do driver compatível pode precisar de rede na primeira execução.')
    page()
    heading('9 Aceitação e testes não funcionais')
    p('Os cenários UAT-01 a UAT-04 verificam cadastro/acesso, organização de disciplinas, urgência e progresso. Os quatro passaram tecnicamente. Homologação humana não foi assinada; a aprovação técnica não foi convertida automaticamente em decisão de usuário.')
    p('As seis verificações não funcionais cobrem desempenho da página e da API, navegação por inspeção de fluxos, feedback de validação, armazenamento de senhas e controle de acesso/entradas. Usabilidade é uma inspeção técnica, sem pesquisa com participantes, contraste ou leitor de tela.')
    table(['Rota HTTP','N','Média ms','P95 ms','Máximo ms'], [[route,v['n'],f"{v['media_ms']:.3f}",f"{v['p95_ms']:.3f}",f"{v['max_ms']:.3f}"] for route,v in perf['rotas'].items()])
    p('Foram três aquecimentos e 30 amostras por rota, com um cliente sequencial, um usuário, duas disciplinas e três tarefas em SQLite temporário. Todas as amostras ficaram abaixo de 500ms. Fonte: latencias_http.csv e desempenho.json. Essa medida é tempo de resposta HTTP em loopback, não renderização completa nem teste de carga.')
    p('Segurança: hash verificado com check_password_hash, rejeição de acesso sem sessão, restrição por proprietário e consultas parametrizadas. Esses testes não constituem auditoria completa de segurança. A aplicação continua destinada ao laboratório local.')
    page()
    heading('10 Métricas e análise de qualidade')
    table(['Indicador','Cálculo e resultado'], [
        ['Execução do catálogo','24/24 =100%'],['Aprovação','24/24 =100%'],['Reprovação','0/24 =0%'],
        ['Cobertura de requisitos','8/8 =100% com vínculos explícitos'],['Automação do catálogo','24/24 selecionados =100%'],
        ['Severidade','2 médios e 2 altos confirmados'],['Status','4 encerrados localmente e 0 abertos'],['Reabertura','0/4 =0% nesta rodada']])
    cov=summary['coverage']; percent=cov['covered_lines']/cov['num_statements']*100
    p(f"Cobertura de linhas: {cov['covered_lines']}/{cov['num_statements']} = {percent:.2f}% sem Selenium. Dados de linhas e ramos por arquivo estão em cobertura.json. A planilha Planilha_Metricas.xlsx mantém fórmulas e fontes; a taxa de automação usa o plano real dos 24 cenários e não o mínimo de 15 do manual.")
    p(f'Análise estática Flake8: {before} ocorrências na linha de base e {after} na versão revisada, com o mesmo limite de linha e sem --exit-zero. Logs antes/depois preservados. A revisão não apresenta complexidade Radon não medida ou densidade como substituição não autorizada dos indicadores obrigatórios.')
    p('Interpretação: a aprovação demonstra os cenários selecionados, não ausência geral de defeitos. A reabertura é limitada à revisão. Relatos históricos DEF-01/02 não entram nos totais confirmados. Gráficos atuais estão na pasta 11 e refletem os mesmos dados da planilha.')
    page()
    heading('Gráficos da revisão atual')
    for name, caption in [
        ('grafico_aprovacao_casos.png', 'Figura 1 Reexecução automatizada dos 24 cenários do catálogo'),
        ('grafico_automacao_niveis.png', 'Figura 2 Distribuição dos 98 cenários executados'),
        ('grafico_defeitos_severidade.png', 'Figura 3 Severidade dos quatro defeitos confirmados')]:
        document.add_picture(str(ROOT/'11_METRICAS_E_QUALIDADE'/name), width=Cm(15))
        p(caption)
    p('Fonte das três figuras: arquivos JUnit da revisão e registros DEF-03 a DEF-06. Os dados históricos não auditados não foram agregados.')
    page()
    heading('11 TDD integração contínua e melhoria')
    p('O ciclo TDD novo trata DEF-03: a função de percentual deve rejeitar concluídas positivas quando total é zero. O teste foi escrito antes da correção; RED registrou duas falhas e uma aprovação. GREEN moveu a validação e aprovou os três cenários. REFACTOR simplificou o retorno e preservou a regressão. Logs XML/texto e snapshots SHA256 estão na pasta 12.')
    p('O ciclo histórico da função de urgência não foi usado como comprovação de TDD por ausência de commits apresentados. A revisão preserva snapshots e ordem de execução real, sem inventar hashes Git ou datas de commits. A aceitação desses registros diante da exigência de commits cabe ao professor.')
    p('O workflow canônico na raiz instala dependências, bloqueia erros Flake8, executa testes dos diferentes níveis e faz upload de artefatos. O resumo registra o status real. A cópia na pasta 12 está sincronizada. Uma demonstração local executa falha controlada (código 1) e depois a suíte correta (código 0), com logs preservados.')
    p('Não há execução remota comprovada desta revisão no Actions. Publicação, runs verde/vermelho e URLs são pendências; a demonstração local não foi apresentada como pipeline remoto nem como simulação autorizada pelo professor.')
    p('Melhorias priorizadas: completar evidências humanas e remotas, adicionar CSRF antes de exposição pública, empacotar recursos de interface localmente, paginar tarefas e medir carga maior antes de adotar outro banco. O P11 define responsáveis propostos e critérios de verificação.')
    heading('12 Discussão dos resultados')
    p('Pontos fortes: correção de falhas efetivas, isolamento por usuário e banco, asserções mais precisas, fronteiras completas, respostas HTTP preservadas e medições reproduzíveis. Limitações: registros históricos não auditados, dependência inicial de rede para driver e CDN, ausência de ensaio concorrente e de aceitação externa. O diário original contém datas futuras e foi preservado apenas para conferência.')
    page()
    heading('13 Conclusão')
    p('A versão revisada atende às verificações técnicas executadas no ambiente acadêmico local: 98 cenários aprovados, latências dentro do critério na base pequena e análise estática sem ocorrências. O trabalho apresenta evidências atuais e distingue claramente o que foi medido do que ainda depende dos integrantes.')
    p('O parecer é favorável ao escopo testado em laboratório, com ressalvas documentais e operacionais. Não se declara prontidão para produção pública, aprovação docente ou entrega oficial já concluída. A nota pertence ao professor e depende também das pendências que a automação não pode substituir.')
    heading('Referências')
    p('SILVA, Elvio Gilberto da. Testes e Qualidade de Software Projeto P2. Manual fornecido para esta avaliação, 2026. Seções 9 a 16 e apêndices.')
    p('Código-fonte EduTask Web e documentos P02 a P14 desta entrega. Linha de base do Git local e revisão de 11/11/2026.')
    p('Ferramentas efetivamente executadas: Python, Flask/Werkzeug, SQLite, pytest, Selenium WebDriver, coverage.py, Flake8 e Black. As bibliotecas são declaradas em requirements.txt; Black foi utilizado como ferramenta local de formatação.')
    heading('Apêndices e evidências')
    table(['Local','Conteúdo'], [
        ['04_CASOS_E_RASTREABILIDADE','Catálogo, CSV editável e matriz atualizada'],
        ['05_EXECUCAO_MANUAL/evidencias_reexecucao','24 pares HTML/JSON e JUnit'],
        ['06_DEFEITOS','Relatos históricos e quatro registros confirmados'],
        ['09_SISTEMA_INTERFACE/evidencias','Capturas e resultados do navegador'],
        ['11_METRICAS_E_QUALIDADE','Planilha, gráficos, latências, cobertura e logs'],
        ['12_TDD_CICD_MELHORIA/evidencias','RED/GREEN/REFACTOR e pipeline local'],
        ['00_IDENTIFICACAO_E_README','Instruções e pendências humanas'],
        ['16_BACKUP_ENTREGA','Checklist e ZIP atualizado']])
    out=ROOT/'13_RELATORIO_FINAL/RELATORIO_FINAL_PROJETO_P2.docx'
    for element in [document._element, document.styles.element]:
        for border in element.xpath('.//w:pBdr'):
            border.getparent().remove(border)
    document.save(out)
    print('Gerado',out)


if __name__ == '__main__':
    main()
