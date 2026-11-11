# Métricas e indicadores da revisão

Data: 2026-11-11T12:31:56-03:00. Dados: JUnit XML, respostas HTML/JSON, CSV de latências e coverage.py. Planilha editável com fórmulas: `Planilha_Metricas.xlsx`.

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

Suíte completa: 98/98 cenários aprovados, sem skip. Unidade 30, integração 36, catálogo 24, aceitação técnica 4 e Selenium 4.
Cobertura de linhas sem Selenium: 517/574 = 90.07%. Cobertura de ramos e dados por arquivo disponíveis em cobertura.json. Essa medida não inclui a execução do navegador.

## Comparação estática

Mesmo comando e limite de 120 caracteres antes/depois: `python -m flake8 01_SISTEMA_ALVO/edutask --config=01_SISTEMA_ALVO/.flake8`.
Linha de base: 179 ocorrências. Após revisão: 0. Logs: `evidencias/flake8_antes.txt` e `flake8_depois.txt`.
Foram removidos espaços residuais, imports não usados e linhas excessivas; exportações de pacote são explícitas. Não se usa --exit-zero no CI.
As duas medições são da revisão atual. Não há relatório Radon ou complexidade medida; as alegações anteriores foram removidas.

## Interpretação

A revisão executou todos os cenários planejados e encontrou quatro defeitos confirmados. A aprovação atual demonstra a regressão selecionada, sem comprovar todos os caminhos do sistema ou aceitação por usuários.
A avaliação de desempenho é limitada à base pequena e ao ambiente registrado. Os gráficos representam dados atuais, sem repetir os valores históricos sem evidência.
