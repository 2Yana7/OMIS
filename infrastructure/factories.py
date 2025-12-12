from __future__ import annotations

from typing import Any, Dict, Type

from model import (
    InMemorySensorRepository,
    InMemoryLevelRepository,
    InMemoryStorageRepository,
    InMemoryForecastRepository,
    InMemoryReportRepository,
)
from controllers import (
    DataCollectionController,
    AnalysisController,
    DecisionSupportController,
    InterfaceController,
    LevelManager,
    JournalManager,
)
from .container import DependencyContainer


class RepositoryFactory:
  

    def __init__(self, container: DependencyContainer) -> None:
        self._container = container
        self._repo_types: Dict[str, Any] = {
            "sensor": InMemorySensorRepository,
            "level": InMemoryLevelRepository,
            "storage": InMemoryStorageRepository,
            "forecast": InMemoryForecastRepository,
            "report": InMemoryReportRepository,
        }

    def create(self, key: str) -> Any:
        if key not in self._repo_types:
            raise KeyError(f"Неизвестный тип репозитория: {key}")
        repo = self._repo_types[key]()
        self._container.register(f"repo:{key}", repo)
        return repo

    def switch(self, key: str, new_repo: Any) -> None:
        self._container.register(f"repo:{key}", new_repo)

    def check_links(self) -> bool:
        required = ["sensor", "level", "storage", "forecast", "report"]
        for r in required:
            if f"repo:{r}" not in self._container._instances:
                return False
        return True


class ControllerFactory:
 

    def __init__(self, container: DependencyContainer) -> None:
        self._container = container
        self._controllers: Dict[str, Any] = {}

    def create(self, key: str) -> Any:
        if key in self._controllers:
            return self._controllers[key]

        journal = self._container.resolve(JournalManager)

        if key == "data":
            ctrl = DataCollectionController(
                sensor_repository=self._container.resolve("repo:sensor"),
                storage_repository=self._container.resolve("repo:storage"),
                journal=journal,
            )
        elif key == "analysis":
            ctrl = AnalysisController(
                storage_repository=self._container.resolve("repo:storage"),
                forecast_repository=self._container.resolve("repo:forecast"),
                journal=journal,
            )
        elif key == "decision":
            ctrl = DecisionSupportController(
                forecast_repository=self._container.resolve("repo:forecast"),
                report_repository=self._container.resolve("repo:report"),
                journal=journal,
            )
        elif key == "interface":
            level_manager = self._container.resolve(LevelManager)
            analysis = self.create("analysis")
            decision = self.create("decision")
            ctrl = InterfaceController(
                level_manager=level_manager,
                analysis_controller=analysis,
                decision_controller=decision,
                journal=journal,
            )
        else:
            raise KeyError(f"Неизвестный тип контроллера: {key}")

        self._controllers[key] = ctrl
        return ctrl

    def get_list(self) -> Dict[str, Any]:
        return dict(self._controllers)

    def recreate(self, key: str) -> Any:
        if key in self._controllers:
            del self._controllers[key]
        return self.create(key)
