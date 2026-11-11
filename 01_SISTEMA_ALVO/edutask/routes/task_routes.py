from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime, date
from ..models import get_db_connection
from ..services.task_service import calculate_task_urgency, filter_task_list

task_bp = Blueprint("tasks", __name__)


def login_required():
    return "user_id" in session


@task_bp.route("/tarefas")
def list_tasks():
    if not login_required():
        flash("Faça login para acessar suas tarefas.", "warning")
        return redirect(url_for("auth.login"))

    status_filter = request.args.get("status", "Todos")
    priority_filter = request.args.get("priority", "Todas")
    search_query = request.args.get("q", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT t.*, d.name as discipline_name, d.code as discipline_code
        FROM tasks t
        JOIN disciplines d ON t.discipline_id = d.id
        WHERE t.user_id = ?
        ORDER BY t.due_date ASC
    """,
        (session["user_id"],),
    )
    raw_tasks = [dict(row) for row in cursor.fetchall()]

    # Recalcula urgência dinâmica para cada tarefa
    for t in raw_tasks:
        score, level = calculate_task_urgency(t["due_date"])
        t["urgency_score"] = score
        t["urgency_level"] = level

    filtered_tasks = filter_task_list(raw_tasks, status_filter, priority_filter, search_query)

    # Busca disciplinas para combo de filtro
    cursor.execute(
        "SELECT id, code, name FROM disciplines WHERE user_id = ? ORDER BY name ASC", (session["user_id"],)
    )
    disciplines = cursor.fetchall()
    conn.close()

    return render_template(
        "tarefas.html",
        tasks=filtered_tasks,
        disciplines=disciplines,
        current_status=status_filter,
        current_priority=priority_filter,
        current_query=search_query,
    )


@task_bp.route("/tarefas/nova", methods=["GET", "POST"])
def new_task():
    if not login_required():
        flash("Faça login para criar tarefas.", "warning")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        due_date = request.form.get("due_date", "").strip()
        priority = request.form.get("priority", "Média")
        discipline_id = request.form.get("discipline_id")

        if not title or len(title) < 3:
            conn.close()
            flash("O título da tarefa deve ter no mínimo 3 caracteres.", "danger")
            return redirect(url_for("tasks.new_task"))

        if not due_date:
            conn.close()
            flash("A data limite de entrega é obrigatória.", "danger")
            return redirect(url_for("tasks.new_task"))

        try:
            parsed_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            if parsed_date < date.today():
                flash("Atenção: A data limite informada é anterior à data de hoje.", "warning")
        except ValueError:
            conn.close()
            flash("Formato de data inválido.", "danger")
            return redirect(url_for("tasks.new_task"))

        if priority not in ("Baixa", "Média", "Alta"):
            priority = "Média"

        if not discipline_id:
            conn.close()
            flash("Selecione uma disciplina vinculada.", "danger")
            return redirect(url_for("tasks.new_task"))

        cursor.execute(
            "SELECT id FROM disciplines WHERE id = ? AND user_id = ?", (discipline_id, session["user_id"])
        )
        if not cursor.fetchone():
            conn.close()
            flash("Disciplina não encontrada para este usuário.", "danger")
            return redirect(url_for("tasks.new_task"))

        urgency_score, urgency_level = calculate_task_urgency(due_date)

        cursor.execute(
            """
            INSERT INTO tasks (title, description, due_date, priority, status,
                               discipline_id, user_id, urgency_score, urgency_level)
            VALUES (?, ?, ?, ?, 'Pendente', ?, ?, ?, ?)
        """,
            (
                title,
                description,
                due_date,
                priority,
                int(discipline_id),
                session["user_id"],
                urgency_score,
                urgency_level,
            ),
        )

        conn.commit()
        conn.close()
        flash("Atividade acadêmica cadastrada com sucesso!", "success")
        return redirect(url_for("tasks.list_tasks"))

    cursor.execute(
        "SELECT id, code, name FROM disciplines WHERE user_id = ? ORDER BY name ASC", (session["user_id"],)
    )
    disciplines = cursor.fetchall()
    conn.close()

    if not disciplines:
        flash("Cadastre pelo menos uma disciplina antes de criar atividades.", "warning")
        return redirect(url_for("disciplines.new_discipline"))

    return render_template("tarefa_form.html", disciplines=disciplines)


@task_bp.route("/tarefas/status/<int:task_id>", methods=["POST"])
def update_status(task_id):
    if not login_required():
        return redirect(url_for("auth.login"))

    new_status = request.form.get("status")
    if new_status not in ("Pendente", "Em Andamento", "Concluída"):
        flash("Status inválido.", "danger")
        return redirect(url_for("tasks.list_tasks"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?", (new_status, task_id, session["user_id"])
    )
    conn.commit()
    conn.close()

    flash(f'Status da tarefa atualizado para "{new_status}".', "success")
    return redirect(url_for("tasks.list_tasks"))


@task_bp.route("/tarefas/excluir/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if not login_required():
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, session["user_id"]))
    conn.commit()
    conn.close()

    flash("Tarefa excluída com sucesso.", "info")
    return redirect(url_for("tasks.list_tasks"))
