"""Implementación sencilla del patrón Singleton mediante metaclase."""

from threading import Lock


class SingletonMeta(type):
    """Metaclase que garantiza una única instancia para cada clase que la use."""

    _instances: dict[type, object] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
