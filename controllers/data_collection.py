from __future__ import annotations

from datetime import datetime
from typing import Optional

from model import Sensor, SensorRepository, StorageRecord, StorageRepository
from .journal import JournalManager


class DataCollectionController:
    """
    «КонтроллерСбораДанных».

    Работает с сенсорами и подсистемой хранения.
    Методы диаграммы:
        - инициализироватьСенсоры()
        - собратьДанные(идУровня: int)
        - обработатьСобытие(событие)
        - завершитьСбор()
    """

    def __init__(
        self,
        sensor_repository: SensorRepository,
        storage_repository: StorageRepository,
        journal: Optional[JournalManager] = None,
    ) -> None:
        self._sensors = sensor_repository
        self._storage = storage_repository
        self._journal = journal or JournalManager()
        self._active: bool = False

    def initialize_sensors(self) -> None:
        """
        инициализироватьСенсоры()

        В реальной системе здесь могла бы быть инициализация подключений.
        Сейчас просто помечаем сбор как активный и пишем в журнал.
        """
        self._active = True
        self._journal.add_entry("Сенсоры инициализированы", level="INFO")

    def collect_data(self, level_id: Optional[int] = None) -> None:
        """
        собратьДанные(идУровня: int)

        Проходит по всем сенсорам, считывает значения и добавляет записи
        в хранилище. Ид уровня может использоваться для пометок/фильтрации.
        """
        if not self._active:
            self._journal.add_entry(
                "Попытка сбора данных при неинициализированных сенсорах",
                level="WARN",
            )
            return

        for sensor in self._sensors.get_all():
            value = sensor.read_value()
            record = StorageRecord(
                timestamp=datetime.now(),
                sensor_id=sensor.sensor_id,
                value=value,
                event_type=f"MEASURE_LEVEL_{level_id}" if level_id is not None else "MEASURE",
            )
            self._storage.save_record(record)
        self._journal.add_entry("Сбор данных с сенсоров завершён", level="INFO")

    def handle_event(self, event: str) -> None:
        """
        обработатьСобытие(событие)

        Заглушка для обработки произвольных событий:
        просто записывает событие в журнал.
        """
        self._journal.add_entry(f"Событие: {event}", level="INFO")

    def finish_collection(self) -> None:
        """
        завершитьСбор()

        Завершает текущую сессию сбора данных.
        """
        self._active = False
        self._journal.add_entry("Сбор данных остановлен", level="INFO")
