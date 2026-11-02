# PRODUTO P10 - RELATÓRIO DE MÉTRICAS E INDICADORES DE QUALIDADE
**Projeto:** EduTask Web v1.0.0-p2  
**Disciplina:** Testes e Qualidade de Software | **UNISAGRADO 2026**  
**Docente:** Prof. Dr. Elvio Gilberto da Silva  
**Equipe:** Gabriel Henrique Moreira, João Lucas de Antonio Boconcelo, Lucas Braga  

---

## 1. Painel Mínimo de Métricas Obrigatórias (Apêndice K e Seção 9.13)

| Indicador | Fórmula de Cálculo | Valor Obtido | Fonte dos Dados | Interpretação Técnica dos Resultados |
| :--- | :--- | :---: | :--- | :--- |
| **1. Percentual de Execução** | $\frac{\text{Casos Executados}}{\text{Casos Planejados}} \times 100$ | **100,0%** | Catálogo de Casos P04 e Registro de Execuções P06 | Demonstra que todo o escopo de testes planejado foi rigorosamente executado dentro do cronograma sem deixar itens pendentes (24 de 24 casos). |
| **2. Taxa de Aprovação** | $\frac{\text{Casos Aprovados}}{\text{Casos Executados}} \times 100$ | **91,67%** *(1º Ciclo)*<br>**100,0%** *(Reteste)* | Registro de Execução P06 | No ciclo inicial, 22 dos 24 casos foram aprovados imediatamente e 2 apresentaram não-conformidades. Após as correções (DEF-01 e DEF-02), a aprovação atingiu 100%. |
| **3. Taxa de Reprovação** | $\frac{\text{Casos Reprovados}}{\text{Casos Executados}} \times 100$ | **8,33%** *(1º Ciclo)*<br>**0,0%** *(Final)* | Registro de Execução P06 e Gestão de Defeitos P07 | Indica a proporção de falhas observadas na primeira rodada (2 falhas em 24 casos). O baixo percentual reflete a boa maturidade arquitetural inicial do software. |
| **4. Cobertura de Requisitos** | $\frac{\text{Requisitos com Teste}}{\text{Requisitos no Escopo}} \times 100$ | **100,0%** | Matriz de Rastreabilidade P05 | Todos os 8 requisitos aprovados (RF-01 a RF-06 e RNF-01 a RNF-02) possuem casos de teste associados e executados com sucesso, assegurando cobertura total. |
| **5. Taxa de Automação** | $\frac{\text{Casos Automatizados}}{\text{Planejados para Automação}} \times 100$ | **120,0%** | Scripts P08 (8 unitários, 6 de API e 4 Selenium E2E = 18 entregues vs 15 mínimos) | Superou a meta mínima estabelecida pelo plano, reduzindo o esforço de testes de regressão manual para ciclos futuros. |
| **6. Defeitos por Severidade** | Contagem por categoria | **Crítica:** 0<br>**Alta:** 0<br>**Média:** 2<br>**Baixa:** 0 | Relatório de Defeitos P07 | Os problemas detectados foram restritos a regras de validação (complexidade de senha e limite de carga horária), sem travamentos críticos ou perda de dados. |
| **7. Defeitos por Status** | Contagem por estado | **Encerrados:** 2<br>**Abertos:** 0<br>**Em Análise:** 0 | Relatório de Defeitos P07 | 100% dos defeitos identificados foram corrigidos, retestados e devidamente encerrados antes do fechamento da versão. |
| **8. Taxa de Reabertura** | $\frac{\text{Defeitos Reabertos}}{\text{Defeitos Retestados}} \times 100$ | **0,0%** | Histórico de Retestes P06 e P07 | As correções aplicadas pela equipe de desenvolvimento foram precisas na primeira tentativa de reteste, sem reincidência de bugs nem regressões. |

---

## 2. Gráficos de Qualidade Gerados

### 2.1 Taxa de Aprovação dos Casos de Teste
*Arquivo gerado:* `grafico_aprovacao_casos.png`  
*Interpretação:* O gráfico em setor circular destaca que 91,7% dos casos foram aprovados imediatamente no primeiro ciclo de testes manuais, e os 8,3% restantes (2 casos) foram corrigidos e aprovados após o reteste de regressão.

### 2.2 Cobertura da Automação por Nível de Teste
*Arquivo gerado:* `grafico_automacao_niveis.png`  
*Interpretação:* O gráfico comparativo de barras evidencia que o grupo excedeu os requisitos mínimos nos três níveis:
* **Testes Unitários:** 8 testes entregues (meta mínima: 6).
* **Testes de Integração / API:** 6 testes entregues (meta mínima: 5).
* **Testes de Interface E2E com Selenium:** 4 fluxos entregues (meta mínima: 4).

### 2.3 Distribuição e Resolução de Defeitos
*Arquivo gerado:* `grafico_defeitos_severidade.png`  
*Interpretação:* Nenhum defeito de severidade "Crítica" ou "Alta" foi encontrado. Os 2 defeitos registrados com severidade "Média" foram sanados e homologados, resultando em taxa de resolução de 100% e taxa de reabertura de 0%.

---

## 3. Análise Estática de Qualidade de Código (Seção 9.16)

A análise estática de código foi realizada utilizando o analisador **Flake8** em dois momentos cronológicos distintos:

### 3.1 Linha de Base (*Baseline* Inicial)
* **Momento da Medição:** Primeira versão funcional da aplicação antes da padronização e refatoração.
* **Métricas Apontadas:** O analisador apontou violações de estilo PEP8, excesso de linhas longas sem quebra (`E501`) e espaçamentos inconsistentes entre funções (`E302`/`W293`).
* **Complexidade Ciclomática Máxima:** Identificada na função de rotas de tarefas com múltiplos `if-else` encadeados.

### 3.2 Medição Posterior (Após TDD e Refatoração)
* **Momento da Medição:** Versão pós-introdução do módulo de regras puras `task_service.py`, isolamento de cálculo de urgência e configuração do arquivo `.flake8`.
* **Resultados:**
  * Redução drástica de avisos de código desnecessário e importações órfãs.
  * Modularização das funções com complexidade ciclomática mantida abaixo de 5 em cada método do serviço.
  * Legibilidade aprimorada e aderência aos padrões de código limpo (Clean Code).
