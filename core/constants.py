from __future__ import annotations

APP_NAME = "ULTRON"
APP_VERSION = "0.1.0"
CURRENT_SPRINT = 0
ORGANIZATION_NAME = "ULTRON"
ORGANIZATION_DOMAIN = "ultron.local"

COLOR_BACKGROUND = "#08090D"
COLOR_PANEL = "#151923"
COLOR_PANEL_ALT = "#1C2230"
COLOR_CRIMSON = "#E11D48"
COLOR_ELECTRIC = "#FF334F"
COLOR_CYAN = "#22D3EE"
COLOR_WHITE = "#F8FAFC"
COLOR_MUTED = "#8B95A8"
COLOR_BORDER = "#2A3142"
COLOR_SUCCESS = "#34D399"
COLOR_WARNING = "#FBBF24"
COLOR_DANGER = "#E11D48"

NAV_ITEMS: tuple[tuple[str, str, str], ...] = (
    ("dashboard", "Dashboard", "Command center"),
    ("voice", "Voice Assistant", "Push-to-talk and wake word"),
    ("chat", "AI Chat", "Text conversation"),
    ("files", "File Manager", "Approved file operations"),
    ("apps", "Application Control", "Launch and window control"),
    ("automation", "Automation Center", "Multi-step tasks"),
    ("developer", "Developer Tools", "Projects, Git, servers"),
    ("memory", "Memory", "Persistent memory"),
    ("history", "History", "Tasks and conversations"),
    ("monitor", "System Monitor", "CPU, RAM, processes"),
    ("settings", "Settings", "Preferences and security"),
)

TASK_STATES: tuple[str, ...] = (
    "PENDING",
    "VALIDATING",
    "PLANNING",
    "AWAITING_APPROVAL",
    "EXECUTING",
    "VERIFYING",
    "COMPLETED",
    "FAILED",
    "CANCELLED",
    "TIMED_OUT",
)
