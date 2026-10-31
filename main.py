from __future__ import annotations

import sys

from core.app import create_application
from ui.main_window import MainWindow


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv
    app = create_application(args)
    window = MainWindow(app.state, app.signals)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
