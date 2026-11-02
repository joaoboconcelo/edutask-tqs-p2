from flask import Blueprint, render_template, session, redirect, url_for
from ..models import get_db_connection
from ..services.task_service import calculate_completion_rate, calculate_task_urgency

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Contagens de tarefas
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Concluída'")
    completed_tasks = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Pendente'")
    pending_tasks = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Em Andamento'")
    in_progress_tasks = cursor.fetchone()[0]
    
    # Contagem de disciplinas
    cursor.execute("SELECT COUNT(*) FROM disciplines")
    total_disciplines = cursor.fetchone()[0]
    
    # Próximas 5 tarefas ordenadas por data
    cursor.execute('''
        SELECT t.*, d.name as discipline_name, d.code as discipline_code 
        FROM tasks t
        JOIN disciplines d ON t.discipline_id = d.id
        ORDER BY t.due_date ASC
        LIMIT 5
    ''')
    upcoming_tasks = [dict(r) for r in cursor.fetchall()]
    conn.close()
    
    # Calcula taxa percentual
    completion_rate = calculate_completion_rate(total_tasks, completed_tasks)
    
    for t in upcoming_tasks:
        score, level = calculate_task_urgency(t['due_date'])
        t['urgency_score'] = score
        t['urgency_level'] = level
        
    return render_template(
        'dashboard.html',
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        total_disciplines=total_disciplines,
        completion_rate=completion_rate,
        upcoming_tasks=upcoming_tasks
    )
