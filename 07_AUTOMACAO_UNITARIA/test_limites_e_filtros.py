"""RF-05, RF-06 e R-07: fronteiras completas e combinações de filtros."""

import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_SISTEMA_ALVO"))
from edutask.services.task_service import calculate_task_urgency, calculate_completion_rate, filter_task_list


@pytest.mark.parametrize("days,expected", [(-1, 100), (0, 100), (1, 75), (2, 75), (3, 50), (7, 50), (8, 25)])
def test_urgency_boundaries(days, expected):
    today = date(2026, 11, 11)
    assert calculate_task_urgency((today + timedelta(days=days)).isoformat(), today)[0] == expected


@pytest.mark.parametrize("value", ["2026-02-30", "abc", "11/11/2026"])
def test_invalid_dates(value):
    with pytest.raises(ValueError):
        calculate_task_urgency(value)


@pytest.mark.parametrize(
    "total,completed,exception", [(-1, 0, ValueError), (3, -1, ValueError), ("3", 1, TypeError)]
)
def test_completion_invalid_values(total, completed, exception):
    with pytest.raises(exception):
        calculate_completion_rate(total, completed)


@pytest.mark.parametrize(
    "status,priority,search,ids",
    [
        ("Pendente", "Alta", None, [1]),
        ("Pendente", "Baixa", None, [2]),
        ("Concluída", "Alta", None, [3]),
        ("Concluída", "Baixa", None, []),
        ("Todos", "Todas", " MÉTRICAS ", [1]),
        ("Todos", "Todas", "INEXISTENTE", []),
    ],
)
def test_filter_decision_table(status, priority, search, ids):
    tasks = [
        dict(id=1, title="Relatório", description="Métricas", status="Pendente", priority="Alta"),
        dict(id=2, title="Exercício", description="", status="Pendente", priority="Baixa"),
        dict(id=3, title="Entrega", description="", status="Concluída", priority="Alta"),
    ]
    assert [t["id"] for t in filter_task_list(tasks, status, priority, search)] == ids
