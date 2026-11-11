"""RNF-02: PBKDF2-SHA256 no cadastro inicial e migração transparente no login."""

import sys
from pathlib import Path

import pytest
from werkzeug.security import generate_password_hash, check_password_hash

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_SISTEMA_ALVO"))
from edutask.app import create_app
from edutask.models import get_db_connection


@pytest.fixture
def app(tmp_path):
    return create_app({"TESTING": True, "DATABASE": str(tmp_path / "hash.db")})


def test_seed_uses_required_hash(app):
    with app.app_context():
        conn = get_db_connection()
        row = conn.execute("SELECT password_hash FROM users WHERE id = 1").fetchone()
        conn.close()
    assert row["password_hash"].startswith("pbkdf2:sha256:")
    assert check_password_hash(row["password_hash"], "Senha@123")


@pytest.mark.parametrize("path,status", [("/login", 302), ("/api/auth/login", 200)])
def test_legacy_hash_is_upgraded_after_valid_login(app, path, status):
    legacy = generate_password_hash("Senha@123", method="scrypt")
    with app.app_context():
        conn = get_db_connection()
        conn.execute("UPDATE users SET password_hash = ? WHERE id = 1", (legacy,))
        conn.commit()
        conn.close()
    credentials = {"email": "aluno@unisagrado.edu.br", "password": "Senha@123"}
    response = (
        app.test_client().post(path, json=credentials)
        if path.startswith("/api/")
        else app.test_client().post(path, data=credentials)
    )
    assert response.status_code == status
    with app.app_context():
        conn = get_db_connection()
        updated = conn.execute("SELECT password_hash FROM users WHERE id = 1").fetchone()[0]
        conn.close()
    assert updated != legacy
    assert updated.startswith("pbkdf2:sha256:")
    assert check_password_hash(updated, "Senha@123")
