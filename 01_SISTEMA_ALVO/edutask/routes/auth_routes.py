from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import get_db_connection, upgrade_password_hash
from ..services.task_service import validate_email, validate_password_strength

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or len(name) < 2:
            flash("O nome completo deve ter no mínimo 2 caracteres.", "danger")
            return render_template("register.html")

        if not validate_email(email):
            flash("Formato de e-mail inválido.", "danger")
            return render_template("register.html")

        valid_pwd, pwd_msg = validate_password_strength(password)
        if not valid_pwd:
            flash(pwd_msg, "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("As senhas digitadas não coincidem.", "danger")
            return render_template("register.html")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            flash("Este e-mail já está cadastrado no sistema.", "warning")
            return render_template("register.html")

        p_hash = generate_password_hash(password, method="pbkdf2:sha256")
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, 'student')",
            (name, email, p_hash),
        )
        conn.commit()
        conn.close()

        flash("Cadastro realizado com sucesso! Efetue login para continuar.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Preencha todos os campos para entrar.", "warning")
            return render_template("login.html")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, password_hash, role FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if not user or not check_password_hash(user["password_hash"], password):
            flash("Credenciais inválidas. Verifique seu e-mail e senha.", "danger")
            return render_template("login.html")

        upgrade_password_hash(user["id"], password, user["password_hash"])
        session.clear()
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]
        session["user_role"] = user["role"]

        flash(f'Bem-vindo(a), {user["name"]}!', "info")
        return redirect(url_for("main.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso.", "info")
    return redirect(url_for("auth.login"))
