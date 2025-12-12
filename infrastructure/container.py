from __future__ import annotations

from typing import Any, Dict, Type


class DependencyContainer:
 
    def __init__(self) -> None:
        self._instances: Dict[Any, Any] = {}

    def register(self, key: Any, instance: Any) -> None:
        self._instances[key] = instance

    def resolve(self, key: Any) -> Any:
        if key not in self._instances:
            raise KeyError(f"Зависимость с ключом {key!r} не зарегистрирована")
        return self._instances[key]

    def remove(self, key: Any) -> None:
        self._instances.pop(key, None)

    def initialize(self) -> None:
     
        pass
