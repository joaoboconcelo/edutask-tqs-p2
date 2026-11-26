# Reexecução verificável do catálogo

Data da consolidação: 2026-11-11T12:31:56-03:00. Método: Flask test client, banco SQLite temporário por cenário.

Os 24 cenários CT-001 a CT-024 foram reexecutados por automação. Resultado: 24/24 aprovados.
Esta rodada é automatizada e não é apresentada como execução manual. Os relatos EX-001 a EX-024 permanecem históricos.

Cada caso possui resposta HTML e metadados JSON em `evidencias_reexecucao/CT-NNN.*`.
O relatório JUnit está em `evidencias_reexecucao/catalogo.xml`.
Além da mensagem, o script verifica persistência, ausência de gravação inválida, sessão ou resultado calculado conforme o cenário.
CT-023 prepara explicitamente uma tarefa Pendente/Alta para evitar uma aprovação por lista vazia.

Reproduzir da raiz: `python -m pytest -v 05_EXECUCAO_MANUAL/test_reexecucao_catalogo.py`.

## Execução manual do grupo

Em 26/11/2026, João Lucas de Antonio Boconcelo executou manualmente os 24 casos no navegador. Resultado: 24/24 aprovados. Registro em `REGISTRO_EXECUCAO_MANUAL.csv` (EX-M-001 a EX-M-024).
