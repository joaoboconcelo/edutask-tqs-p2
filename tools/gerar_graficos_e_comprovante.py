"""Gráficos da revisão atual e minuta que não simula entrega ou assinatura."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'11_METRICAS_E_QUALIDADE'
summary=json.loads((OUT/'evidencias/resumo_entrega.json').read_text(encoding='utf-8'))
charts = [
 ('grafico_aprovacao_casos.png', 'Reexecução automatizada do catálogo', ['Aprovados','Reprovados'], [summary['catalogo']['passed'],summary['catalogo']['failed']]),
 ('grafico_automacao_niveis.png', 'Cenários executados por conjunto', ['Unidade','Integração','Catálogo','Aceitação técnica','Selenium'], [30,36,24,4,4]),
 ('grafico_defeitos_severidade.png', 'Defeitos confirmados na revisão', ['Crítica','Alta','Média','Baixa'], [0,2,2,0]),
]
for filename,title,labels,values in charts:
    fig,ax=plt.subplots(figsize=(7,2.3),layout='constrained')
    bars=ax.bar(labels,values,color='#555555',width=.55)
    ax.bar_label(bars,padding=3)
    ax.set_title(title,loc='left',fontsize=12,fontweight='bold')
    ax.set_ylim(0,max(values)*1.25+1)
    ax.set_ylabel('Quantidade')
    ax.spines[['top','right']].set_visible(False)
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.tick_params(axis='x',labelsize=8)
    fig.savefig(OUT/filename,dpi=160)
    plt.close(fig)

styles=getSampleStyleSheet()
styles['Title'].textColor=colors.black
styles['Heading2'].textColor=colors.black
target=ROOT/'00_IDENTIFICACAO_E_README/COMPROVANTE_DE_ENTREGA.pdf'
doc=SimpleDocTemplate(str(target),pagesize=A4,rightMargin=55,leftMargin=55,topMargin=55,bottomMargin=55,
                      title='Minuta de comprovante de entrega do EduTask Web',author='Grupo 01')
story=[]
def para(text,style='Normal'):
    story.append(Paragraph(text,styles[style])); story.append(Spacer(1,10))
para('Minuta de comprovante de entrega','Title')
para('UNISAGRADO | Ciência da Computação | Testes e Qualidade de Software')
para('Turma A / Grupo 01 | EduTask Web v1.0.1-p2')
para('Este formulário deve ser preenchido e assinado pelo grupo somente após o envio efetivo ao Drive oficial. A revisão local não comprova entrega, horário, permissões ou assinaturas.')
for text in ['Data e hora efetivas do envio: __________________________________',
             'Pasta oficial do professor: _____________________________________',
             'Responsável pelo envio: _______________________________________',
             'Verificação de acesso sem privilégios e download: __________________',
             'Checklist final conferido pelo grupo: ____________________________']:
    para(text)
para('Itens locais verificáveis','Heading2')
para('Relatório DOCX/PDF, código, testes, dados brutos, matriz, métricas e backup. Consultar o checklist da pasta 16 e a lista de pendências da pasta 00 antes do envio.')
para('A apresentação e o vídeo foram dispensados conforme informação do solicitante; a dispensa não substitui a confirmação dos demais itens.')
para('Assinaturas após conferência','Heading2')
for name in ['Gabriel Henrique Moreira','João Lucas de Antonio Boconcelo','Lucas Braga']:
    para(name+'<br/>Assinatura: __________________________ Data: ______________')
doc.build(story)
print('Gráficos atuais e minuta gerados.')
