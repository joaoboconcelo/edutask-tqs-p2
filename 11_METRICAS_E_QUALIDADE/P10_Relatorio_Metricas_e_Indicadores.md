# Métricas e indicadores consolidados

Resultados da revisão de 11/11/2026. Fontes: JUnit, coverage.py, CSV de latências, Flake8, SonarQube Cloud e seis issues de defeitos. A planilha editável conserva 12 fórmulas com dados identificados.

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

Além da automação, 24 casos e quatro cenários foram inspecionados interativamente pela interface. Essas 28 observações complementares têm capturas e executor identificado e não são somadas novamente ao total pytest.

## Análise estática antes e depois

O mesmo comando e limite de 120 caracteres registraram 179 ocorrências antes e zero depois: `python -m flake8 01_SISTEMA_ALVO/edutask --config=01_SISTEMA_ALVO/.flake8`. Os logs foram preservados; não se usa --exit-zero no workflow.

## SonarQube Cloud antes e depois

A análise de qualidade também foi feita no SonarQube Cloud (projeto `joaoboconcelo_edutask-tqs-p2`, análise automática, perfil Sonar way), em duas execuções em 26/11/2026:

| Métrica | Linha de base (commit 08b913a) | Posterior (commit 4b04687) |
|---|---|---|
| Linhas analisadas | 8.325 | 3.242 |
| Vulnerabilidades | 94 (nota E) | 5 (nota E) |
| Bugs | 40 (nota D) | 0 (nota A) |
| Code smells | 19 (nota A) | 0 (nota A) |
| Duplicação | 49,2% | 0,0% |
| Quality gate | Não calculado | Aprovado |

Interpretação: 134 dos 153 issues da linha de base estavam em arquivos de evidência (HTML salvos das telas nas pastas 05 e 09), que não são código do sistema; esses arquivos também explicam a duplicação de 49,2%. O escopo foi ajustado em `.sonarcloud.properties` para excluir evidências e documentos, o que responde pela maior parte da redução. No código real foram corrigidos: integridade (SRI) dos três recursos de CDN em `base.html`, rótulos associados aos três filtros de `tarefas.html` (6 issues de confiabilidade/acessibilidade) e instalação apenas por pacotes binários no CI; três issues de um script de apoio removido também deixaram de existir.

Permanecem 5 vulnerabilidades: a senha fictícia de demonstração `Senha@123` em `models.py` (classificada como bloqueadora por constar em listas de senhas vazadas, o que mantém a nota E) e no script de medição; a ausência de proteção CSRF em `app.py`, já declarada como limitação; e dependências do CI sem versões travadas com hash. Essas ações compõem o plano de melhoria. Evidências: `11_METRICAS_E_QUALIDADE/evidencias/sonarcloud_linha_de_base_*` e `sonarcloud_posterior_*`.

## Interpretação

A regressão foi ampliada para contratos JSON inválidos, tipos de credenciais, migração de hashes, exclusões e fluxos alternativos. A cobertura alta não prova ausência geral de falhas. Os indicadores não substituem a análise dos riscos. O desempenho é restrito à base pequena e ao ambiente declarado; a taxa de reabertura não é uma previsão de ausência futura de regressão.

Os três gráficos em PNG usam os mesmos totais da planilha. O algoritmo PBKDF2-SHA256 é verificado diretamente, conforme RNF-02 original; não foi alterado o requisito para acomodar a implementação.
