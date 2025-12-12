from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from .entities import Sensor, Level, StorageRecord, Report, Forecast


T = TypeVar("T")
ID = TypeVar("ID")


# ====== БАЗОВЫЙ РЕПОЗИТОРИЙ (интерфейс «Репозиторий») ======


class Repository(ABC, Generic[T, ID]):
    """
    Интерфейс «Репозиторий» с диаграммы.

    Методы:
        сохранить(объект)
        загрузить(идентификатор)
        удалить(идентификатор)
        получитьВсе(): list
    """

    @abstractmethod
    def save(self, obj: T) -> None:
        """Сохранить объект в хранилище."""
        raise NotImplementedError

    @abstractmethod
    def load(self, identifier: ID) -> Optional[T]:
        """Загрузить объект по идентификатору."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, identifier: ID) -> None:
        """Удалить объект по идентификатору."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        """Получить список всех объектов."""
        raise NotImplementedError


# ====== СПЕЦИАЛИЗИРОВАННЫЕ РЕПОЗИТОРИИ (интерфейсы) ======


class SensorRepository(Repository[Sensor, int], ABC):
    """Интерфейс «РепозиторийСенсоров»."""
    pass


class LevelRepository(Repository[Level, int], ABC):
    """Интерфейс «РепозиторийУровней»."""
    pass


class StorageRepository(Repository[StorageRecord, int], ABC):
    """
    Интерфейс «РепозиторийХранилища».

    Для простоты считаем, что идентификатором является целое число.
    """
    pass


class ReportRepository(Repository[Report, int], ABC):
    """Интерфейс «РепозиторийОтчётов»."""
    pass


class ForecastRepository(Repository[Forecast, int], ABC):
    """Интерфейс «РепозиторийПрогнозов»."""
    pass
