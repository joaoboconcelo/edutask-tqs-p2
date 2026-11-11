# TDD integração contínua e melhoria

## Ciclo principal com três commits cronológicos reais

Comportamento: a API deve rejeitar JSON não objeto e credenciais não textuais com HTTP 400, sem erro interno. O teste foi escrito e executado antes da correção. As falhas do RED correspondem ao defeito observado, não a uma asserção falsa inserida apenas para a demonstração de CI.

| Etapa | Commit real | Data | Resultado |
|---|---|---|---|
| RED | e2ad848831f68d84b2976ca20c85c59f3123b73c | 2026-11-11T17:53:29-03:00 | 17 falhas e 3 aprovados antes da correção |
| GREEN | 9feabf493df34e27a876651d08037ac668d67a30 | 2026-11-11T17:54:13-03:00 | 20 aprovados após implementação mínima |
| REFACTOR | 4e55cbbaa515950dbdcb50b02483deb37e01d131 | 2026-11-11T17:54:33-03:00 | 20 aprovados após isolamento da validação |

GREEN acrescentou a validação mínima antes do acesso a campos. REFACTOR extraiu a função pura json_payload_error sem alterar o comportamento e manteve os 20 cenários aprovados. Código, datas e resultados podem ser confrontados com o Git e os arquivos red/green/refactor em evidencias/tdd_json. O histórico da primeira experiência do cálculo de percentual continua como evidência complementar, claramente separado deste ciclo com commits.

## Pipeline preparado e demonstração local

Arquivo canônico: `.github/workflows/ci.yml`, na raiz. A configuração da raiz é a referência canônica.
Gatilhos: push e pull_request em main/develop, além de workflow_dispatch. Etapas: instalação, Flake8 bloqueante, unidade, integração, catálogo, aceitação técnica, Selenium e upload de artefatos.
O resumo usa o estado real do job; não anuncia sucesso quando uma etapa falha.

Execução local equivalente: `python tools/verificar_pipeline.py`. Um teste temporário com `assert 25 == 100` retorna código 1; depois a suíte correta retorna 0. Logs `pipeline_local_falha.txt`, `pipeline_local_sucesso.txt` e `pipeline_local.json`.
A demonstração local foi complementada por execuções reais no GitHub Actions. A revisão publicada foi aprovada; um PR separado falhou exatamente na asserção intencional e voltou a passar após sua remoção. O PR foi encerrado sem merge, preservando a versão principal funcional.

## Melhoria contínua

| Prioridade | Ação | Responsabilidade proposta | Verificação |
|---|---|---|---|
| Concluída | Publicação e comprovação de falha/correção no Actions | Revisão técnica | Três execuções e PR #5 |
| Alta | Confirmar execução manual, aceitação e aprovação do sistema | Grupo | Registros datados e assinados, sem reconstruir histórico |
| Alta | Proteção CSRF e restrições de sessão antes de exposição pública | João Lucas, confirmar | POST sem token rejeitado e regressão |
| Média | Paginar tarefas e medir carga com 500 registros | Grupo | Tempo sob carga, sem extrapolar a medição pequena |
| Média | Empacotar Bootstrap e ícones localmente | Grupo | Navegação com rede externa desativada |
| Baixa | Avaliar PostgreSQL conforme necessidade de concorrência | Grupo | Teste comparativo de concorrência |

Análise de qualidade: 179 ocorrências Flake8 antes e 0 depois, com logs na pasta P10. A alteração funcional corrigiu inconsistência observada e ampliou regressão e isolamento.

## Execuções reais e commits

| Etapa | Commit | Conclusão | URL |
|---|---|---|---|
| principal | 33d441c7f6dc4599da735727f232c5c1aa5d41f3 | success | https://github.com/joaoboconcelo/edutask-tqs-p2/actions/runs/43094289919 |
| falha_controlada | 018467182875469c7eb57214fdcdc75eefd600e1 | failure | https://github.com/joaoboconcelo/edutask-tqs-p2/actions/runs/43094396473 |
| correcao | 7407afef2a4d9744661295ccc99d795dd6be2db5 | success | https://github.com/joaoboconcelo/edutask-tqs-p2/actions/runs/43094602358 |

PR de demonstração: https://github.com/joaoboconcelo/edutask-tqs-p2/pull/5 . Metadados e logs originais extraídos em evidencias/github. As execuções remotas são de CI; os registros RED/GREEN/REFACTOR continuam identificados separadamente.

## Regressão ampliada publicada

145 cenários aprovados localmente; 98,32% de linhas e 94,19% de ramos. A execução remota 43099616601 aprovou o commit 4acc9d5, incluindo contrato JSON, PBKDF2-SHA256 e migração de hashes. Evidências originais em evidencias/github.

https://github.com/joaoboconcelo/edutask-tqs-p2/actions/runs/43099616601
