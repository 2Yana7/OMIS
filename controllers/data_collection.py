from __future__ import annotations

from datetime import datetime
from typing import Optional

from model import Sensor, SensorRepository, StorageRecord, StorageRepository
from .journal import JournalManager


class DataCollectionController:


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
      
        self._active = True
        self._journal.add_entry("Сенсоры инициализированы", level="INFO")

    def collect_data(self, level_id: Optional[int] = None) -> None:
     
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
       
        self._journal.add_entry(f"Событие: {event}", level="INFO")

    def finish_collection(self) -> None:
     
        self._active = False
        self._journal.add_entry("Сбор данных остановлен", level="INFO")
