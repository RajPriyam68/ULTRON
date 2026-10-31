# ULTRON

Unified Local and Remote Task-Orchestration Network.

ULTRON is a native Windows 10/11 desktop assistant. Primary interaction is voice; text is secondary. Sprint 0 delivers the application foundation only: configuration, logging, architecture packages, and a real PySide6 command-center shell.

## Current status

**Sprint 0 — Foundation (this tree)**

- Python package layout for later sprints
- Pydantic settings and path layout
- Structured logging with secret redaction
- PySide6 application, theme, navigation, reactor, waveform, system meters
- Emergency stop, command intake, and CPU/RAM polling
- Foundational pytest coverage

Later sprints (not implemented yet): voice, desktop automation, AI routing, secure tools, browser/dev workflows, memory, packaging.

## Requirements

- Python 3.11+ (3.12+ preferred on Windows)
- Windows 10/11 for production use
- Linux is supported for Sprint 0 UI and tests via Qt offscreen/xcb

## Setup

```bash
# Install runtime dependencies
pip install --break-system-packages -r requirements.txt

# Install development dependencies
pip install --break-system-packages -r requirements-dev.txt

# Optional local environment file
copy .env.example .env
```

On Linux/macOS use `cp .env.example .env`. Fill `USER_LLM_*` yourself in later sprints. Do not place API keys in source.

## Run

```bash
# From the repository root
python main.py
```

Headless / CI:

```bash
# Force Qt offscreen platform
set QT_QPA_PLATFORM=offscreen
python main.py
```

On Linux/macOS:

```bash
QT_QPA_PLATFORM=offscreen python main.py
```

## Tests

```bash
QT_QPA_PLATFORM=offscreen python -m pytest
```

Lint:

```bash
python -m ruff check .
```

## Architecture (Sprint 0)

```text
ULTRON/
  main.py
  requirements.txt
  requirements-dev.txt
  .env.example
  README.md
  config/          settings and path layout
  core/            app, state, signals, logging, constants
  assistant/       Sprint 3+
  voice/           Sprint 1+
  tools/           Sprint 2+
  security/        Sprint 4+
  memory/          Sprint 6+
  database/        Sprint 6+
  ui/              main window, theme, widgets, views
  resources/
  tests/
  scripts/
  data/            created at runtime (logs, db, screenshots)
```

UI, AI, voice, security, database, and automation stay in separate packages. Sprint 0 wires only UI, config, logging, and application state.

## Security notes already in force

- No unrestricted shell execution
- Logging redacts messages that look like secrets
- LLM keys are read from `USER_LLM_*` placeholders only
- Emergency stop is a first-class UI and state action

## Sprint roadmap

| Sprint | Focus |
|--------|--------|
| 0 | Foundation, PySide6 shell, config, logging |
| 1 | Voice: microphone, Faster-Whisper, Piper |
| 2 | Desktop automation |
| 3 | AI intelligence and routing |
| 4 | Secure agent and tool registry |
| 5 | Browser, terminal, developer workflows |
| 6 | Memory and SQLite |
| 7 | Production polish and packaging |
