from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from config.settings import Settings, get_settings

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class PathLayout:
    root: Path
    data_dir: Path
    log_dir: Path
    db_path: Path
    resources_dir: Path
    models_dir: Path
    screenshots_dir: Path
    audit_dir: Path

    def ensure(self) -> PathLayout:
        for directory in (
            self.data_dir,
            self.log_dir,
            self.resources_dir,
            self.models_dir,
            self.screenshots_dir,
            self.audit_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)
        return self


def resolve_paths(settings: Settings | None = None) -> PathLayout:
    settings = settings or get_settings()
    data_dir = settings.data_dir if settings.data_dir else PROJECT_ROOT / "data"
    data_dir = data_dir.expanduser().resolve()
    layout = PathLayout(
        root=PROJECT_ROOT,
        data_dir=data_dir,
        log_dir=data_dir / "logs",
        db_path=data_dir / "ultron.db",
        resources_dir=PROJECT_ROOT / "resources",
        models_dir=data_dir / "models",
        screenshots_dir=data_dir / "screenshots",
        audit_dir=data_dir / "audit",
    )
    return layout.ensure()
