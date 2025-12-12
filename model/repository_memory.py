from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from .entities import Sensor, Level, StorageRecord, Report, Forecast
from .repository_base import (
    SensorRepository,
    LevelRepository,
    StorageRepository,
    ReportRepository,
    ForecastRepository,
)


# ====== РЕАЛИЗАЦИИ РЕПОЗИТОРИЕВ (in-memory) ======


class InMemorySensorRepository(SensorRepository):
    """
    РеализацияРепозиторияСенсоров.

    Хранит сенсоры в памяти (dict).
    """

    def __init__(self) -> None:
        self._storage: Dict[int, Sensor] = {}

    # Базовые методы Repository

    def save(self, obj: Sensor) -> None:
        self._storage[obj.sensor_id] = obj

    def load(self, identifier: int) -> Optional[Sensor]:
        return self._storage.get(identifier)

    def delete(self, identifier: int) -> None:
        self._storage.pop(identifier, None)

    def get_all(self) -> List[Sensor]:
        return list(self._storage.values())

    # Методы с диаграммы:
    # добавитьСенсор, получитьСенсор, обновитьСенсор

    def add_sensor(self, sensor: Sensor) -> None:
        """добавитьСенсор(сенсор: Сенсор)"""
        self.save(sensor)

    def get_sensor(self, sensor_id: int) -> Optional[Sensor]:
        """получитьСенсор(id: int)"""
        return self.load(sensor_id)

    def update_sensor(self, sensor: Sensor) -> None:
        """обновитьСенсор(сенсор: Сенсор)"""
        self.save(sensor)


class InMemoryLevelRepository(LevelRepository):
    """
    РеализацияРепозиторияУровней.

    Хранит уровни в памяти (dict).
    """

    def __init__(self) -> None:
        self._storage: Dict[int, Level] = {}

    def save(self, obj: Level) -> None:
        self._storage[obj.level_id] = obj

    def load(self, identifier: int) -> Optional[Level]:
        return self._storage.get(identifier)

    def delete(self, identifier: int) -> None:
        self._storage.pop(identifier, None)

    def get_all(self) -> List[Level]:
        return list(self._storage.values())

    # Методы с диаграммы:
    # добавитьУровень, получитьУровень, обновитьУровень

    def add_level(self, level: Level) -> None:
        """добавитьУровень(уровень: Уровень)"""
        self.save(level)

    def get_level(self, level_id: int) -> Optional[Level]:
        """получитьУровень(id: int)"""
        return self.load(level_id)

    def update_level(self, level: Level) -> None:
        """обновитьУровень(уровень: Уровень)"""
        self.save(level)


class InMemoryStorageRepository(StorageRepository):
    """
    РеализацияРепозиторияХранилища.

    Хранит записи в списке.
    Для идентификатора используем индекс в списке.
    """

    def __init__(self) -> None:
        self._records: List[StorageRecord] = []

    def save(self, obj: StorageRecord) -> None:
        self._records.append(obj)

    def load(self, identifier: int) -> Optional[StorageRecord]:
        if 0 <= identifier < len(self._records):
            return self._records[identifier]
        return None

    def delete(self, identifier: int) -> None:
        if 0 <= identifier < len(self._records):
            self._records.pop(identifier)

    def get_all(self) -> List[StorageRecord]:
        return list(self._records)

    # Методы с диаграммы:
    # сохранитьЗапись(запись), получитьИсторию(идСенсора), очиститьСтарыеДанные()

    def save_record(self, record: StorageRecord) -> None:
        """сохранитьЗапись(запись: ЗаписьХранилища)"""
        self.save(record)

    def get_history(self, sensor_id: int) -> List[StorageRecord]:
        """получитьИсторию(идСенсора: int)"""
        return [r for r in self._records if r.sensor_id == sensor_id]

    def clear_old(self, before: datetime) -> None:
        """очиститьСтарыеДанные() — удаляет записи старше указанного времени."""
        self._records = [r for r in self._records if r.timestamp >= before]


class InMemoryReportRepository(ReportRepository):
    """
    РеализацияРепозиторияОтчётов.
    """

    def __init__(self) -> None:
        self._storage: Dict[int, Report] = {}

    def save(self, obj: Report) -> None:
        self._storage[obj.report_id] = obj

    def load(self, identifier: int) -> Optional[Report]:
        return self._storage.get(identifier)

    def delete(self, identifier: int) -> None:
        self._storage.pop(identifier, None)

    def get_all(self) -> List[Report]:
        return list(self._storage.values())

    # Методы с диаграммы:
    # сохранитьОтчёт, получитьОтчёт, очиститьСтарые, найтиПоАвтору

    def save_report(self, report: Report) -> None:
        """сохранитьОтчёт(отчёт: Отчёт)"""
        self.save(report)

    def get_report(self, report_id: int) -> Optional[Report]:
        """получитьОтчёт(id: int)"""
        return self.load(report_id)

    def clear_old(self, before: datetime) -> None:
        """очиститьСтарые() — удаляет отчёты старше указанного времени."""
        to_delete = [
            r_id for r_id, r in self._storage.items()
            if r.created_at < before
        ]
        for r_id in to_delete:
            self.delete(r_id)

    def find_by_author(self, author: str) -> List[Report]:
        """найтиПоАвтору(автор: string): list"""
        return [r for r in self._storage.values() if r.author == author]


class InMemoryForecastRepository(ForecastRepository):
    """
    РеализацияРепозиторияПрогнозов.
    """

    def __init__(self) -> None:
        self._storage: Dict[int, Forecast] = {}

    def save(self, obj: Forecast) -> None:
        self._storage[obj.forecast_id] = obj

    def load(self, identifier: int) -> Optional[Forecast]:
        return self._storage.get(identifier)

    def delete(self, identifier: int) -> None:
        self._storage.pop(identifier, None)

    def get_all(self) -> List[Forecast]:
        return list(self._storage.values())

    # Методы с диаграммы:
    # сохранитьПрогноз, получитьПрогноз, очиститьСтарые

    def save_forecast(self, forecast: Forecast) -> None:
        """сохранитьПрогноз(прогноз: Прогноз)"""
        self.save(forecast)

    def get_forecast(self, forecast_id: int) -> Optional[Forecast]:
        """получитьПрогноз(id: int)"""
        return self.load(forecast_id)

    def clear_old(self, before: datetime) -> None:
        """очиститьСтарые() — удаляет прогнозы старше указанного времени."""
        to_delete = [
            f_id for f_id, f in self._storage.items()
            if f.created_at < before
        ]
        for f_id in to_delete:
            self.delete(f_id)
