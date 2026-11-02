from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models import get_db_connection
from ..services.task_service import validate_discipline_code, validate_workload

discipline_bp = Blueprint('disciplines', __name__)

def login_required():
    return 'user_id' in session

@discipline_bp.route('/disciplinas')
def list_disciplines():
    if not login_required():
        flash('Faça login para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.*, COUNT(t.id) as total_tasks 
        FROM disciplines d 
        LEFT JOIN tasks t ON t.discipline_id = d.id 
        GROUP BY d.id 
        ORDER BY d.code ASC
    ''')
    disciplines = cursor.fetchall()
    conn.close()
    
    return render_template('disciplinas.html', disciplines=disciplines)

@discipline_bp.route('/disciplinas/nova', methods=['GET', 'POST'])
def new_discipline():
    if not login_required():
        flash('Faça login para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
        name = request.form.get('name', '').strip()
        teacher = request.form.get('teacher', '').strip()
        workload = request.form.get('workload_hours', '')
        
        if not validate_discipline_code(code):
            flash('Código de disciplina inválido. Formato esperado: CC-TQS01, ENG-101 (2 a 4 letras, hífen e 2 a 6 alfanuméricos).', 'danger')
            return render_template('disciplina_form.html')
            
        if not name or len(name) < 3:
            flash('O nome da disciplina deve ter pelo menos 3 caracteres.', 'danger')
            return render_template('disciplina_form.html')
            
        if not teacher or len(teacher) < 3:
            flash('O nome do professor(a) deve ter pelo menos 3 caracteres.', 'danger')
            return render_template('disciplina_form.html')
            
        if not validate_workload(workload):
            flash('A carga horária deve ser um valor numérico entre 15 e 400 horas.', 'danger')
            return render_template('disciplina_form.html')
            
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM disciplines WHERE code = ?", (code,))
        if cursor.fetchone():
            conn.close()
            flash(f'Já existe uma disciplina cadastrada com o código {code}.', 'warning')
            return render_template('disciplina_form.html')
            
        cursor.execute(
            "INSERT INTO disciplines (code, name, teacher, workload_hours, user_id) VALUES (?, ?, ?, ?, ?)",
            (code, name, teacher, int(workload), session['user_id'])
        )
        conn.commit()
        conn.close()
        
        flash('Disciplina cadastrada com sucesso!', 'success')
        return redirect(url_for('disciplines.list_disciplines'))
        
    return render_template('disciplina_form.html')

@discipline_bp.route('/disciplinas/excluir/<int:disc_id>', methods=['POST'])
def delete_discipline(disc_id):
    if not login_required():
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE discipline_id = ?", (disc_id,))
    task_count = cursor.fetchone()[0]
    
    if task_count > 0:
        conn.close()
        flash('Não é possível excluir disciplina que possui tarefas vinculadas.', 'danger')
        return redirect(url_for('disciplines.list_disciplines'))
        
    cursor.execute("DELETE FROM disciplines WHERE id = ?", (disc_id,))
    conn.commit()
    conn.close()
    flash('Disciplina removida com sucesso.', 'info')
    return redirect(url_for('disciplines.list_disciplines'))
