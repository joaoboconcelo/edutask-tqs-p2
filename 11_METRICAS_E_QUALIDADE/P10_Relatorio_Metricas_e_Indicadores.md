# Métricas e indicadores consolidados

Resultados da revisão de 11/11/2026. Fontes: JUnit, coverage.py, CSV de latências, Flake8 e seis issues de defeitos. A planilha editável conserva 12 fórmulas com dados identificados.

| Indicador obrigatório | Cálculo | Resultado | Fonte |
|---|---|---|---|
| Execução do catálogo | 24/24 | 100% | Catálogo e XML |
| Aprovação do catálogo | 24/24 | 100% | catalogo.xml |
| Reprovação do catálogo | 0/24 | 0% | catalogo.xml |
| Cobertura de requisitos | 8/8 | 100% | P05 e verificações executadas |
| Automação planejada do catálogo | 24/24 | 100% | Plano e script da pasta 05 |
| Defeitos por severidade | Média 4; Alta 2; Crítica/Baixa 0 | 6 confirmados | P07 e issues #1, #2, #3, #4, #6 e #7 |
| Defeitos por status | Encerrados 6; abertos 0 | 6 corrigidos | Quatro com reteste remoto inicial e dois com regressão complementar publicada |
| Taxa de reabertura | 0/6 | 0% | Limitada à rodada atual |

Suíte: **145/145 cenários aprovados**. Unidade 34; integração/API 79; catálogo 24; aceitação técnica 4; Selenium 4. Casos parametrizados são contados por entrada executada, não como funções distintas.

Cobertura de linhas sem Selenium: **586/596 = 98.32%**. Ramos: **162/172 = 94.19%**. Há 10 linhas não cobertas, identificadas em cobertura.json; a métrica não foi inflada por excluir linhas do produto.

Além da automação, 24 casos e quatro cenários foram inspecionados interativamente pela interface. Essas 28 observações complementares têm capturas e executor técnico identificado, sem serem somadas novamente ao total pytest ou apresentadas como assinaturas humanas.

## Análise estática antes e depois

O mesmo comando e limite de 120 caracteres registraram 179 ocorrências antes e zero depois: `python -m flake8 01_SISTEMA_ALVO/edutask --config=01_SISTEMA_ALVO/.flake8`. Os logs foram preservados; não se usa --exit-zero no workflow.

## Interpretação

A regressão foi ampliada para contratos JSON inválidos, tipos de credenciais, migração de hashes, exclusões e fluxos alternativos. A cobertura alta não prova ausência geral de falhas. Os indicadores não substituem análise dos riscos ou homologação humana. O desempenho é restrito à base pequena e ao ambiente declarado; a taxa de reabertura não é uma previsão de ausência futura de regressão.

Os três gráficos em PNG usam os mesmos totais da planilha. O algoritmo PBKDF2-SHA256 é verificado diretamente, conforme RNF-02 original; não foi alterado o requisito para acomodar a implementação.
