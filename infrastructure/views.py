from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from model import Level, Report
from controllers import InterfaceController, LevelManager, JournalManager


class View(ABC):
    

    def __init__(self, journal: JournalManager) -> None:
        self._visible: bool = False
        self._journal = journal

    @abstractmethod
    def show(self) -> None:
        self._visible = True

    @abstractmethod
    def update(self) -> None:
        ...

    def hide(self) -> None:
        self._visible = False
        self._journal.add_entry(
            f"{self.__class__.__name__} скрыто",
            level="INFO",
        )


class LevelsView(View):


    def __init__(self, level_manager: LevelManager, journal: JournalManager) -> None:
        super().__init__(journal)
        self._level_manager = level_manager
        self._cached_levels: List[Level] = []

    def show(self) -> None:
        self._visible = True
        self._cached_levels = self._level_manager.get_levels()
        self._journal.add_entry(
            f"Показано представление уровней ({len(self._cached_levels)} уровней)",
            level="INFO",
        )

    def update(self) -> None:
        self._cached_levels = self._level_manager.get_levels()
        self._journal.add_entry("Список уровней обновлён", level="INFO")

    def display_levels(self) -> List[Level]:
        if not self._visible:
            self.show()
        return list(self._cached_levels)

    def show_level_details(self, level_id: int) -> Level | None:
        for lvl in self._cached_levels:
            if lvl.level_id == level_id:
                self._journal.add_entry(
                    f"Показаны детали уровня id={level_id}",
                    level="INFO",
                )
                return lvl
        self._journal.add_entry(
            f"Уровень id={level_id} не найден в представлении",
            level="WARN",
        )
        return None

    def create_new_level(self, data: dict) -> Level:
        level = self._level_manager.create_level(data)
        self.update()
        self._journal.add_entry(
            f"Создан новый уровень id={level.level_id} через представление",
            level="INFO",
        )
        return level


class RecommendationsView(View):
  

    def __init__(self, journal: JournalManager) -> None:
        super().__init__(journal)
        self._last_text: str = ""

    def show(self) -> None:
        self._visible = True
        self._journal.add_entry("Показано представление рекомендаций", level="INFO")

    def update(self) -> None:
        self._journal.add_entry(
            "Представление рекомендаций обновлено",
            level="INFO",
        )

    def show_recommendations(self, text: str) -> None:
        self._last_text = text
        if not self._visible:
            self.show()
        self._journal.add_entry(
            f"Новые рекомендации: {text}",
            level="INFO",
        )

    def refresh_tips(self) -> None:
        self.update()


class ReportsView(View):
   

    def __init__(self, interface_controller: InterfaceController, journal: JournalManager) -> None:
        super().__init__(journal)
        self._interface = interface_controller
        self._last_report: Report | None = None

    def show(self) -> None:
        self._visible = True
        reports = self._interface.show_results()
        if reports:
            self._last_report = reports[-1]
        self._journal.add_entry(
            f"Показано представление отчётов (всего {len(reports)})",
            level="INFO",
        )

    def update(self) -> None:
        reports = self._interface.show_results()
        if reports:
            self._last_report = reports[-1]
        self._journal.add_entry("Список отчётов обновлён", level="INFO")

    def show_report(self, report: Report) -> None:
        self._last_report = report
        if not self._visible:
            self.show()
        self._journal.add_entry(
            f"Показан отчёт #{report.report_id}",
            level="INFO",
        )

    def export_report(self, fmt: str = "txt") -> str:
        if self._last_report is None:
            self._journal.add_entry(
                "Экспорт отчёта невозможен: отчёт не выбран",
                level="WARN",
            )
            return ""
        exported = self._last_report.export(fmt)
        self._journal.add_entry(
            f"Отчёт #{self._last_report.report_id} экспортирован в формат {fmt}",
            level="INFO",
        )
        return exported

