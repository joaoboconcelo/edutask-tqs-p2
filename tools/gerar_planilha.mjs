import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const root = process.cwd();
const data = JSON.parse(await fs.readFile(path.join(root, '11_METRICAS_E_QUALIDADE/evidencias/resumo_entrega.json'), 'utf8'));
const workbook = Workbook.create();
const sheet = workbook.worksheets.add('Indicadores');
const source = workbook.worksheets.add('Dados');
sheet.showGridLines = false;
source.showGridLines = false;
sheet.getRange('A1:D1').values = [['EduTask Web | Indicadores da revisão de 11/11/2026', null, null, null]];
sheet.getRange('A3:D3').values = [['Indicador', 'Valor', 'Unidade', 'Interpretação']];
const rows = [
 ['Execução do catálogo', null, '%', 'Reexecução automatizada; rodada manual histórica não auditada'],
 ['Aprovação do catálogo', null, '%', 'Casos aprovados na revisão atual'],
 ['Reprovação do catálogo', null, '%', 'Casos com falha na revisão atual'],
 ['Cobertura de requisitos', null, '%', 'Requisitos com verificação vinculada e executada'],
 ['Automação planejada', null, '%', '24 cenários selecionados e automatizados nesta revisão'],
 ['Defeitos médios confirmados', null, 'defeitos', 'DEF-03 e DEF-04'],
 ['Defeitos altos confirmados', null, 'defeitos', 'DEF-05 e DEF-06'],
 ['Defeitos confirmados encerrados', null, 'defeitos', 'Corrigidos e cobertos por regressão'],
 ['Defeitos confirmados abertos', null, 'defeitos', 'Exclui riscos residuais e relatos históricos'],
 ['Taxa de reabertura', null, '%', 'Somente quatro defeitos confirmados nesta revisão'],
 ['Cobertura de linhas', null, '%', 'Suíte sem navegador; não equivale à cobertura de requisitos'],
 ['Aprovação da suíte completa', null, '%', 'Unidade, integração, catálogo e quatro fluxos Selenium'],
];
sheet.getRange('A4:D15').values = rows;
const inputs = [
 ['Dado', 'Valor', 'Fonte'],
 ['Casos planejados', 24, 'P04 / plano da revisão'],
 ['Casos executados', data.catalogo.total, 'catalogo.xml'],
 ['Casos aprovados', data.catalogo.passed, 'catalogo.xml'],
 ['Casos reprovados', data.catalogo.failed, 'catalogo.xml'],
 ['Requisitos no escopo', 8, 'P02'],
 ['Requisitos com execução', 8, 'P05 + testes.xml + desempenho.json'],
 ['Cenários planejados para automação', 24, 'P03 revisão'],
 ['Cenários automatizados', 24, 'test_reexecucao_catalogo.py'],
 ['Defeitos médios', 2, 'DEF-03 e DEF-04'],
 ['Defeitos altos', 2, 'DEF-05 e DEF-06'],
 ['Defeitos encerrados', 4, 'P07 / regressão'],
 ['Defeitos abertos', 0, 'P07 revisão'],
 ['Defeitos reabertos', 0, 'P07 revisão'],
 ['Defeitos retestados', 4, 'P07 revisão'],
 ['Linhas executadas', data.coverage.covered_lines, 'cobertura.json'],
 ['Linhas executáveis', data.coverage.num_statements, 'cobertura.json'],
 ['Testes totais', data.tests.total, 'testes.xml + selenium.xml'],
 ['Testes aprovados', data.tests.passed, 'testes.xml + selenium.xml'],
];
source.getRange('A1:C19').values = inputs;
const formulas = ['=Dados!B3/Dados!B2','=Dados!B4/Dados!B3','=Dados!B5/Dados!B3',
 '=Dados!B7/Dados!B6','=Dados!B9/Dados!B8','=Dados!B10','=Dados!B11','=Dados!B12',
 '=Dados!B13','=Dados!B14/Dados!B15','=Dados!B16/Dados!B17','=Dados!B19/Dados!B18'];
sheet.getRange('B4:B15').formulas = formulas.map(x=>[x]);
sheet.getRange('B4:B8').setNumberFormat('0.00%');
sheet.getRange('B9:B12').setNumberFormat('0');
sheet.getRange('B13:B15').setNumberFormat('0.00%');
sheet.getRange('A17:D18').values = [
 ['Escopo dos dados', 'Revisão atual', null, 'Resultados históricos de DEF-01/02 não incorporados às métricas confirmadas.'],
 ['Limitação', 'Ver PENDENCIAS_PARA_ENTREGA.md', null, 'Aprovação docente e execução remota do Actions ainda dependem de confirmação.']];
for(const s of [sheet,source]) {
 const r=s.getUsedRange(); r.format.font.name='Aptos'; r.format.font.size=11;
 r.format.rowHeight=38; r.format.wrapText=true; r.format.verticalAlignment='center';
 r.format.borders={preset:'all',style:'thin',color:'#D9D9D9'};
 s.getRange('A:A').format.columnWidth=38;
 s.getRange('B:B').format.columnWidth=18;
 s.getRange('C:C').format.columnWidth=25;
 s.freezePanes.freezeRows(s===sheet?3:1);
}
sheet.getRange('D:D').format.columnWidth=70;
for (const [s,range] of [[sheet,'A3:D3'],[source,'A1:C1']]) {
 s.getRange(range).format.fill='#303030'; s.getRange(range).format.font.color='#FFFFFF';
 s.getRange(range).format.font.bold=true;
}
sheet.getRange('A1:D1').format.font.bold=true;
sheet.getRange('A1:D1').format.font.size=14;
await workbook.recalculate();
console.log((await workbook.inspect({kind:'table',range:'Indicadores!A3:D15',include:'values,formulas',tableMaxRows:13,tableMaxCols:4,maxChars:3500})).ndjson);
const xlsx=await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(path.join(root,'11_METRICAS_E_QUALIDADE/Planilha_Metricas.xlsx'));
const preview=await workbook.render({sheetName:'Indicadores',range:'A1:D15',scale:1,format:'png'});
await fs.writeFile(path.join(root,'tmp/quality_review/metricas.png'),new Uint8Array(await preview.arrayBuffer()));
