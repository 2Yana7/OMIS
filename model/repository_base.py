from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from .entities import Sensor, Level, StorageRecord, Report, Forecast


T = TypeVar("T")
ID = TypeVar("ID")




class Repository(ABC, Generic[T, ID]):
 

    @abstractmethod
    def save(self, obj: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def load(self, identifier: ID) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, identifier: ID) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError




class SensorRepository(Repository[Sensor, int], ABC):
    pass


class LevelRepository(Repository[Level, int], ABC):
    pass


class StorageRepository(Repository[StorageRecord, int], ABC):
    
    pass


class ReportRepository(Repository[Report, int], ABC):
    pass


class ForecastRepository(Repository[Forecast, int], ABC):
    pass
