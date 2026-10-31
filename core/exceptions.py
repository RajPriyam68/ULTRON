class UltronError(Exception):
    """Base error for ULTRON."""


class ConfigurationError(UltronError):
    """Invalid or missing configuration."""


class SecurityError(UltronError):
    """Policy or permission violation."""
