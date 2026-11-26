# 08_INTEGRACAO_API

79 cenários de integração com banco temporário, sessão e proprietário.

Da raiz: `python -m pytest -v 08_INTEGRACAO_API`.

## Coleção Postman executada com Newman

Em 26/11/2026 a coleção foi executada com Newman 6.2.1 (Node.js 26.13.1) contra uma instância local com banco temporário: 6 requisições e 12 asserções aprovadas, nenhuma falha, tempo médio de resposta de 153 ms. Relatórios em `08_INTEGRACAO_API/evidencias_newman/` (texto, JSON e JUnit).

Reproduzir: iniciar `python 05_EXECUCAO_MANUAL/servidor_validacao_interativa.py` (porta 5011, banco temporário) e, em outro terminal:

```powershell
npx newman@6.2.1 run 08_INTEGRACAO_API/edutask_api_collection.postman_collection.json -e 08_INTEGRACAO_API/edutask_environment.postman_environment.json --env-var base_url=http://127.0.0.1:5011
```

Instruções completas em `00_IDENTIFICACAO_E_README/README.md`.
