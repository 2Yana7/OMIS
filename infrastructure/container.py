from __future__ import annotations

from typing import Any, Dict, Type


class DependencyContainer:
    """
    Аналог класса «КонтейнерЗависимостей» с диаграммы.

    Методы диаграммы:
        - зарегистрировать(тип, объект)
        - разрешить(тип)
        - инициализировать()
        - удалить(тип)
    """

    def __init__(self) -> None:
        self._instances: Dict[Any, Any] = {}

    def register(self, key: Any, instance: Any) -> None:
        """зарегистрировать(тип, объект)"""
        self._instances[key] = instance

    def resolve(self, key: Any) -> Any:
        """разрешить(тип)"""
        if key not in self._instances:
            raise KeyError(f"Зависимость с ключом {key!r} не зарегистрирована")
        return self._instances[key]

    def remove(self, key: Any) -> None:
        """удалить(тип)"""
        self._instances.pop(key, None)

    def initialize(self) -> None:
        """
        инициализировать()

        В реальной системе здесь можно вызывать start/initialize у объектов.
        Сейчас просто заглушка.
        """
        # Пока ничего не делаем, но метод нужен по диаграмме.
        pass
