"""Classes de entrada ausente e limites de tamanho das validações puras."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_SISTEMA_ALVO"))
from edutask.services.task_service import validate_email, validate_password_strength, calculate_task_urgency


@pytest.mark.parametrize("email", ["a@b", "a" * 121 + "@example.com"])
def test_email_size_outside_allowed_range(email):
    assert not validate_email(email)


def test_password_missing_has_actionable_feedback():
    valid, message = validate_password_strength(None)
    assert not valid and message == "Senha não informada."


def test_missing_due_date_has_explicit_neutral_urgency():
    assert calculate_task_urgency(None) == (0, "Sem Data")
