# Revisão de 11 de novembro de 2026

A revisão corrigiu o código e alinhou os documentos às evidências disponíveis. O relatório revisado contém 35 páginas, com sumário atualizado pelo Word e PDF exportado do mesmo DOCX.

## Resultados verificados

- 98 cenários aprovados: 30 unitários, 36 de integração/API, 24 do catálogo, 4 de aceitação técnica e 4 de navegador.
- Cobertura de linhas da suíte sem Selenium: 517 de 574, ou 90,07%. Cobertura por requisito é outra medida, com 8 de 8 requisitos vinculados.
- Flake8: 179 ocorrências antes e zero depois, sem ignorar falhas no workflow.
- 90 amostras HTTP de desempenho preservadas em CSV, todas abaixo do critério de 500 ms no ambiente local e na carga pequena documentada.
- Nova experiência de TDD com falha registrada antes da correção, execução aprovada e refatoração.
- Planilha de métricas com 12 fórmulas e fontes explícitas; três gráficos atualizados.

## Correções técnicas

- Validação da taxa de conclusão antes de tratar total zero.
- Aplicação efetiva da configuração DATABASE e banco temporário por teste.
- Sessão obrigatória na API e consultas/escritas restritas ao proprietário.
- Data inválida na API retorna HTTP 400, sem gravação ou erro interno.
- Urgência retornada pela API recalculada conforme a data atual.
- Teste de cadastro exige 201; dashboard compara o percentual exato.
- Selenium usa servidor próprio em porta livre e preserva capturas reais.
- Pipeline executa linter bloqueante e testes de diferentes níveis e preserva artefatos.

## Ajustes documentais

Foram corrigidos o significado de RF-05, as faixas de urgência, a cobertura dos RNFs na matriz e o cálculo da taxa de automação. RNF-02 explicita scrypt ou PBKDF2; a atualização precisa de validação do grupo/professor.

Os relatos históricos de testes manuais e defeitos foram identificados como não auditados. Atividades futuras no diário não foram mantidas como trabalho comprovado, e as horas e assinaturas não foram inventadas. O comprovante passou a ser uma minuta para preenchimento após envio efetivo.

Apresentação e vídeo foram marcados como dispensados conforme informação do solicitante. Os materiais antigos da pasta 14 permanecem como apoio histórico.

## O que ainda precisa do grupo

Consultar `PENDENCIAS_PARA_ENTREGA.md`: aprovação do sistema, publicação/execuções do Actions, issues, confirmação manual, aceitação humana, origem/licença, participação/assinaturas e entrega oficial. Os formulários CSV para registros manuais e aceite foram preparados sem resultados humanos presumidos.

A revisão técnica foi publicada e aprovada no Actions. Quatro issues foram registradas e encerradas, e o PR de demonstração comprovou falha controlada e correção. A inspeção interativa cobriu 24 casos e quatro cenários de aceitação técnica. A entrega no Drive, a aprovação docente e as assinaturas continuam dependentes do grupo.
