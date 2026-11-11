# TDD integração contínua e melhoria

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

Análise de qualidade: 179 ocorrências Flake8 antes e 0 depois, com logs na pasta P10. A alteração funcional corrigiu inconsistência observada e ampliou regressão e isolamento.
