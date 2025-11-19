# Clients package (weather, notification stubs)
# PUBLIC_INTERFACE
# Do not import submodules here; only declare __all__ for static analysis/completion.

__all__ = ["WeatherClient", "NotificationClient"]
# NOTE: Do NOT import WeatherClient/NotificationClient here to avoid circular import issues.
