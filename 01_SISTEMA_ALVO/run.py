"""
Ponto de entrada para execução da aplicação EduTask Web.
UNISAGRADO - Ciência da Computação - P2 Testes e Qualidade de Software
"""
from edutask.app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("Iniciando EduTask Web - Sistema de Gestão Acadêmica")
    print("Acesse no navegador: http://127.0.0.1:5000")
    print("Credenciais de Teste Padrão:")
    print("  E-mail: aluno@unisagrado.edu.br")
    print("  Senha:  Senha@123")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=False)
