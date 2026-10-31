from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass
class AppState:
    emergency_stopped: bool = False
    listening: bool = False
    current_view: str = "dashboard"
    connectivity: str = "offline-local"
    model_status: str = "offline"
    microphone_status: str = "idle"
    last_command: str = ""
    recent_operations: list[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=utc_now)

    def record_operation(self, message: str, limit: int = 8) -> None:
        stamp = utc_now().strftime("%H:%M:%S")
        self.recent_operations.insert(0, f"{stamp}  {message}")
        self.recent_operations = self.recent_operations[:limit]

    def trigger_emergency_stop(self) -> None:
        self.emergency_stopped = True
        self.listening = False
        self.microphone_status = "stopped"
        self.record_operation("Emergency stop engaged")

    def reset_emergency_stop(self) -> None:
        self.emergency_stopped = False
        self.microphone_status = "idle"
        self.record_operation("Emergency stop cleared")
