from __future__ import annotations

from core.constants import APP_NAME, CURRENT_SPRINT, NAV_ITEMS, TASK_STATES


def test_sprint_zero_identity() -> None:
    assert APP_NAME == "ULTRON"
    assert CURRENT_SPRINT == 0
    assert len(NAV_ITEMS) == 11
    keys = [item[0] for item in NAV_ITEMS]
    assert keys[0] == "dashboard"
    assert "settings" in keys


def test_task_lifecycle_includes_terminal_states() -> None:
    assert TASK_STATES[0] == "PENDING"
    assert "COMPLETED" in TASK_STATES
    assert "FAILED" in TASK_STATES
    assert "CANCELLED" in TASK_STATES
    assert "TIMED_OUT" in TASK_STATES
