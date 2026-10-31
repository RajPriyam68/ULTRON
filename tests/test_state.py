from __future__ import annotations

from core.state import AppState


def test_record_operation_keeps_limit() -> None:
    state = AppState()
    for index in range(12):
        state.record_operation(f"op-{index}", limit=8)
    assert len(state.recent_operations) == 8
    assert "op-11" in state.recent_operations[0]


def test_emergency_stop_halts_listening() -> None:
    state = AppState(listening=True, microphone_status="listening")
    state.trigger_emergency_stop()
    assert state.emergency_stopped is True
    assert state.listening is False
    assert state.microphone_status == "stopped"
    assert any("Emergency stop" in item for item in state.recent_operations)


def test_reset_emergency_stop() -> None:
    state = AppState()
    state.trigger_emergency_stop()
    state.reset_emergency_stop()
    assert state.emergency_stopped is False
    assert state.microphone_status == "idle"
