from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from ..models import get_db_connection
from ..services.task_service import (
    validate_discipline_code,
    validate_workload,
    calculate_task_urgency,
    calculate_completion_rate,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.before_request
def require_api_session():
    if request.endpoint != "api.api_login" and "user_id" not in session:
        return jsonify({"error": "Autenticação necessária."}), 401
    if request.method in ("POST", "PUT"):
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "O corpo JSON deve ser um objeto."}), 400
        if request.endpoint == "api.api_login" and any(
            not isinstance(payload.get(field, ""), str) for field in ("email", "password")
        ):
            return jsonify({"error": "E-mail e senha devem ser textos."}), 400


@api_bp.route("/auth/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Parâmetros obrigatórios ausentes: 'email' e 'password'."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password_hash, role FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Credenciais inválidas."}), 401

    session.clear()
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]
    return (
        jsonify(
            {
                "message": "Autenticação realizada com sucesso.",
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"],
                },
            }
        ),
        200,
    )


@api_bp.route("/disciplinas", methods=["GET", "POST"])
def api_disciplines():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        code = str(data.get("code", "")).strip().upper()
        name = str(data.get("name", "")).strip()
        teacher = str(data.get("teacher", "")).strip()
        workload = data.get("workload_hours")

        if not validate_discipline_code(code):
            conn.close()
            return jsonify({"error": "Código de disciplina inválido. Formato esperado ex: CC-TQS01."}), 400

        if not name or len(name) < 3:
            conn.close()
            return jsonify({"error": "Nome da disciplina deve ter pelo menos 3 caracteres."}), 400

        if not teacher or len(teacher) < 3:
            conn.close()
            return jsonify({"error": "Professor deve ter pelo menos 3 caracteres."}), 400

        if not validate_workload(workload):
            conn.close()
            return jsonify({"error": "Carga horária deve ser entre 15 e 400 horas."}), 400

        cursor.execute("SELECT id FROM disciplines WHERE code = ?", (code,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": f"Disciplina com código '{code}' já existe."}), 409

        cursor.execute(
            "INSERT INTO disciplines (code, name, teacher, workload_hours, user_id) VALUES (?, ?, ?, ?, ?)",
            (code, name, teacher, int(workload), session["user_id"]),
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return (
            jsonify(
                {
                    "message": "Disciplina criada com sucesso.",
                    "discipline": {
                        "id": new_id,
                        "code": code,
                        "name": name,
                        "teacher": teacher,
                        "workload_hours": int(workload),
                    },
                }
            ),
            201,
        )

    # GET
    cursor.execute("SELECT * FROM disciplines WHERE user_id = ? ORDER BY code ASC", (session["user_id"],))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows), 200


@api_bp.route("/tarefas", methods=["GET", "POST"])
def api_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        title = str(data.get("title", "")).strip()
        description = str(data.get("description", "")).strip()
        due_date = str(data.get("due_date", "")).strip()
        priority = data.get("priority", "Média")
        discipline_id = data.get("discipline_id")

        if not title or len(title) < 3:
            conn.close()
            return jsonify({"error": "Título da tarefa deve ter pelo menos 3 caracteres."}), 400

        if not due_date:
            conn.close()
            return jsonify({"error": "Data limite 'due_date' é obrigatória."}), 400

        if priority not in ("Baixa", "Média", "Alta"):
            conn.close()
            return jsonify({"error": "Prioridade inválida. Opções: Baixa, Média, Alta."}), 400

        if not discipline_id:
            conn.close()
            return jsonify({"error": "Campo 'discipline_id' é obrigatório."}), 400

        cursor.execute(
            "SELECT id FROM disciplines WHERE id = ? AND user_id = ?", (discipline_id, session["user_id"])
        )
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": f"Disciplina de ID {discipline_id} não encontrada."}), 404

        try:
            urgency_score, urgency_level = calculate_task_urgency(due_date)
        except ValueError as exc:
            conn.close()
            return jsonify({"error": str(exc)}), 400

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
                discipline_id,
                session["user_id"],
                urgency_score,
                urgency_level,
            ),
        )

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return (
            jsonify(
                {
                    "message": "Tarefa criada com sucesso.",
                    "task": {
                        "id": new_id,
                        "title": title,
                        "due_date": due_date,
                        "priority": priority,
                        "status": "Pendente",
                        "urgency_score": urgency_score,
                        "urgency_level": urgency_level,
                        "discipline_id": discipline_id,
                    },
                }
            ),
            201,
        )

    # GET
    status_filter = request.args.get("status")
    priority_filter = request.args.get("priority")

    query = ("SELECT t.*, d.name as discipline_name FROM tasks t "
             "JOIN disciplines d ON t.discipline_id = d.id WHERE t.user_id = ?")
    params = [session["user_id"]]
    if status_filter:
        query += " AND t.status = ?"
        params.append(status_filter)
    if priority_filter:
        query += " AND t.priority = ?"
        params.append(priority_filter)
    query += " ORDER BY t.due_date ASC"

    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    for row in rows:
        row['urgency_score'], row['urgency_level'] = calculate_task_urgency(row['due_date'])
    conn.close()
    return jsonify(rows), 200


@api_bp.route("/tarefas/<int:task_id>", methods=["GET", "PUT", "DELETE"])
def api_task_detail(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, session["user_id"]))
    task = cursor.fetchone()

    if not task:
        conn.close()
        return jsonify({"error": f"Tarefa com ID {task_id} não encontrada."}), 404

    if request.method == "GET":
        res = dict(task)
        res['urgency_score'], res['urgency_level'] = calculate_task_urgency(res['due_date'])
        conn.close()
        return jsonify(res), 200

    elif request.method == "PUT":
        data = request.get_json(silent=True) or {}
        new_status = data.get("status", task["status"])
        new_priority = data.get("priority", task["priority"])

        if new_status not in ("Pendente", "Em Andamento", "Concluída"):
            conn.close()
            return jsonify({"error": "Status inválido."}), 400
        if new_priority not in ("Baixa", "Média", "Alta"):
            conn.close()
            return jsonify({"error": "Prioridade inválida."}), 400

        cursor.execute(
            "UPDATE tasks SET status = ?, priority = ? WHERE id = ?", (new_status, new_priority, task_id)
        )
        conn.commit()
        conn.close()
        return (
            jsonify(
                {
                    "message": "Tarefa atualizada com sucesso.",
                    "id": task_id,
                    "status": new_status,
                    "priority": new_priority,
                }
            ),
            200,
        )

    elif request.method == "DELETE":
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Tarefa com ID {task_id} removida com sucesso."}), 200


@api_bp.route("/metricas", methods=["GET"])
def api_metrics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (session["user_id"],))
    total_tasks = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'Concluída' AND user_id = ?", (session["user_id"],)
    )
    completed_tasks = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'Pendente' AND user_id = ?", (session["user_id"],)
    )
    pending_tasks = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'Em Andamento' AND user_id = ?", (session["user_id"],)
    )
    progress_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM disciplines WHERE user_id = ?", (session["user_id"],))
    total_disciplines = cursor.fetchone()[0]
    conn.close()

    rate = calculate_completion_rate(total_tasks, completed_tasks)

    return (
        jsonify(
            {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "in_progress_tasks": progress_tasks,
                "completion_rate_percent": rate,
                "total_disciplines": total_disciplines,
            }
        ),
        200,
    )
