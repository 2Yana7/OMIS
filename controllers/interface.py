from __future__ import annotations

from typing import List, Optional

from model import Level, Report
from .analysis import AnalysisController
from .decision_support import DecisionSupportController
from .level_manager import LevelManager
from .journal import JournalManager


class InterfaceController:
    """
    «КонтроллерИнтерфейса».

    Представляет интерфейсную подсистему на уровне логики (без GUI).
    Методы диаграммы:
        - показатьСценарии()
        - показатьРезультаты()
        - обновитьИнтерфейс()
        - обработатьВыборПользователя()
    """

    def __init__(
        self,
        level_manager: LevelManager,
        analysis_controller: AnalysisController,
        decision_controller: DecisionSupportController,
        journal: Optional[JournalManager] = None,
    ) -> None:
        self._levels = level_manager
        self._analysis = analysis_controller
        self._decision = decision_controller
        self._journal = journal or JournalManager()
        self._last_results: List[Report] = []

    def show_scenarios(self) -> List[str]:
        """
        показатьСценарии()

        Возвращает список доступных сценариев использования платформы.
        """
        scenarios = [
            "monitoring",          # сценарий мониторинга
            "level_testing",       # тестирование уровня
            "historical_analysis", # исторический анализ
        ]
        self._journal.add_entry(
            f"Запрошен список сценариев: {scenarios}",
            level="INFO",
        )
        return scenarios

    def show_results(self) -> List[Report]:
        """
        показатьРезультаты()

        Возвращает список последних сформированных отчётов.
        """
        self._journal.add_entry(
            f"Запрошены результаты: {len(self._last_results)} отчётов",
            level="INFO",
        )
        return list(self._last_results)

    def update_interface(self) -> None:
        """
        обновитьИнтерфейс()

        Заглушка для обновления визуальной части интерфейса.
        Здесь просто пишем запись в журнал.
        """
        self._journal.add_entry("Интерфейс обновлён", level="INFO")

    def handle_user_choice(self, scenario: str, level_id: Optional[int] = None) -> None:
        """
        обработатьВыборПользователя()

        Реализует простую логику:
            - пользователь выбирает сценарий,
            - при необходимости выбирается уровень,
            - запускается анализ/прогноз/формирование отчёта.
        """
        self._journal.add_entry(
            f"Выбран сценарий '{scenario}' (уровень={level_id})",
            level="INFO",
        )

        if scenario == "level_testing" and level_id is not None:
            level: Optional[Level] = next(
                (lvl for lvl in self._levels.get_levels() if lvl.level_id == level_id),
                None,
            )
            if level is None:
                self._journal.add_entry(
                    f"Уровень с id={level_id} не найден",
                    level="ERROR",
                )
                return

            # Анализ → прогноз → отчёт
            self._analysis.analyze_data(level)
            forecast = self._analysis.create_forecast(level)
            report = self._decision.form_report(forecast, author="designer")
            self._decision.check_correctness()

            self._last_results.append(report)
            self._journal.add_entry(
                f"Сценарий 'level_testing' завершён, отчёт #{report.report_id}",
                level="INFO",
            )

        elif scenario == "monitoring":
            # В простом варианте только логируем выбор.
            self._journal.add_entry("Сценарий мониторинга активирован", level="INFO")

        elif scenario == "historical_analysis":
            self._journal.add_entry(
                "Сценарий исторического анализа активирован",
                level="INFO",
            )

        else:
            self._journal.add_entry(
                f"Неизвестный сценарий: {scenario}",
                level="WARN",
            )
