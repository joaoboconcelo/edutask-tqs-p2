import sqlite3
from werkzeug.security import generate_password_hash
from flask import current_app


def get_db_connection():
    conn = sqlite3.connect(current_app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela de Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de Disciplinas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            teacher TEXT NOT NULL,
            workload_hours INTEGER NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    # Tabela de Tarefas / Atividades
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            priority TEXT NOT NULL CHECK(priority IN ('Baixa', 'Média', 'Alta')),
            status TEXT NOT NULL DEFAULT 'Pendente' CHECK(status IN ('Pendente', 'Em Andamento', 'Concluída')),
            discipline_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            urgency_score INTEGER DEFAULT 0,
            urgency_level TEXT DEFAULT 'Normal',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (discipline_id) REFERENCES disciplines (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()


def seed_initial_data():
    """Popula banco com dados fictícios controlados para teste"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Usuário padrão de teste se não existir
    cursor.execute("SELECT id FROM users WHERE email = 'aluno@unisagrado.edu.br'")
    user = cursor.fetchone()
    if not user:
        p_hash = generate_password_hash("Senha@123")
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ("Aluno Demonstração", "aluno@unisagrado.edu.br", p_hash, "student"),
        )
        user_id = cursor.lastrowid

        # Disciplinas iniciais
        cursor.execute(
            "INSERT INTO disciplines (code, name, teacher, workload_hours, user_id) VALUES (?, ?, ?, ?, ?)",
            ("CC-TQS01", "Testes e Qualidade de Software", "Prof. Dr. Elvio Gilberto da Silva", 80, user_id),
        )
        d1_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO disciplines (code, name, teacher, workload_hours, user_id) VALUES (?, ?, ?, ?, ?)",
            ("CC-BD02", "Banco de Dados Avançado", "Prof. Roberto Souza", 60, user_id),
        )
        d2_id = cursor.lastrowid

        # Tarefas iniciais
        cursor.execute(
            "INSERT INTO tasks (title, description, due_date, priority, status, "
            "discipline_id, user_id, urgency_score, urgency_level) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "Entrega do Plano de Testes P2",
                "Elaborar documento P03 com estratégias e critérios.",
                "2026-11-15",
                "Alta",
                "Concluída",
                d1_id,
                user_id,
                10,
                "Baixa Urgência",
            ),
        )
        cursor.execute(
            "INSERT INTO tasks (title, description, due_date, priority, status, "
            "discipline_id, user_id, urgency_score, urgency_level) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "Automação com Selenium",
                "Criar 4 fluxos E2E de interface.",
                "2026-11-20",
                "Alta",
                "Em Andamento",
                d1_id,
                user_id,
                30,
                "Média Urgência",
            ),
        )
        cursor.execute(
            "INSERT INTO tasks (title, description, due_date, priority, status, "
            "discipline_id, user_id, urgency_score, urgency_level) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "Modelagem Conceitual de Dados",
                "Construir DER da aplicação.",
                "2026-11-25",
                "Média",
                "Pendente",
                d2_id,
                user_id,
                20,
                "Normal",
            ),
        )

        conn.commit()
    conn.close()
