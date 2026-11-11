"""Regressão escrita antes da correção de DEF-03 em 11/11/2026."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_SISTEMA_ALVO"))
from edutask.services.task_service import calculate_completion_rate


@pytest.mark.parametrize("total,completed", [(0, 1), (0, 5), (2, 3)])
def test_rejects_completed_tasks_above_total(total, completed):
    """RF-05 / R-06: inclusive total zero não aceita concluídas positivas."""
    with pytest.raises(ValueError, match="exceder"):
        calculate_completion_rate(total, completed)
