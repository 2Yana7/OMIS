from __future__ import annotations
from model import Sensor

from typing import Any

from controllers import LevelManager, JournalManager
from .container import DependencyContainer
from .factories import RepositoryFactory, ControllerFactory


class SystemConfigurator:


    def __init__(self) -> None:
        self._repo_factory: RepositoryFactory | None = None
        self._ctrl_factory: ControllerFactory | None = None

    def configure(self, container: DependencyContainer) -> None:

        journal = JournalManager()
        container.register(JournalManager, journal)

        # Репозитории
        repo_factory = RepositoryFactory(container)
        self._repo_factory = repo_factory

        sensor_repo = repo_factory.create("sensor")
        sensor_repo.add_sensor(Sensor(1, "load", "%", 5, 0.7))  # нагрузка
        sensor_repo.add_sensor(Sensor(2, "completion_time", "sec", 5, 120.0))
        level_repo = repo_factory.create("level")
        storage_repo = repo_factory.create("storage")
        forecast_repo = repo_factory.create("forecast")
        report_repo = repo_factory.create("report")

        # Менеджер уровней
        level_manager = LevelManager(level_repo)
        container.register(LevelManager, level_manager)

        # Фабрика контроллеров
        ctrl_factory = ControllerFactory(container)
        self._ctrl_factory = ctrl_factory

        ctrl_factory.create("interface")

    def check_configuration(self, container: DependencyContainer) -> bool:
        if self._repo_factory is None:
            return False
        return self._repo_factory.check_links()

    def load_parameters(self, container: DependencyContainer) -> None:
  
        journal: JournalManager = container.resolve(JournalManager)
        journal.add_entry("Параметры системы загружены (заглушка)", level="INFO")

    @property
    def controller_factory(self) -> ControllerFactory:
        if self._ctrl_factory is None:
            raise RuntimeError("Конфигуратор ещё не настроен")
        return self._ctrl_factory
