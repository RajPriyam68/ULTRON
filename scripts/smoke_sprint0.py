from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QTimer

from core.app import create_application
from ui.main_window import MainWindow


def main() -> int:
    app = create_application(["ultron-smoke"])
    window = MainWindow(app.state, app.signals)
    window.show()
    QTimer.singleShot(1500, app.quit)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
