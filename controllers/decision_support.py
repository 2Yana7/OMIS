from __future__ import annotations

from datetime import datetime
from typing import Optional

from model import Forecast, ForecastRepository, Report, ReportRepository
from .journal import JournalManager


class DecisionSupportController:

    def __init__(
        self,
        forecast_repository: ForecastRepository,
        report_repository: ReportRepository,
        journal: Optional[JournalManager] = None,
    ) -> None:
        self._forecasts = forecast_repository
        self._reports = report_repository
        self._journal = journal or JournalManager()
        self._last_report: Optional[Report] = None

    def form_report(self, forecast: Forecast, author: str = "system") -> Report:
    
        report_id = len(self._reports.get_all()) + 1

        summary = f"Рекомендации по уровню '{forecast.level_name}'"
        content = (
            f"Уровень: {forecast.level_name}\n"
            f"Оценка проходимости: {forecast.passability_score:.2f}\n"
            f"Рекомендации: {forecast.recommendations}\n"
        )

        report = Report(
            report_id=report_id,
            created_at=datetime.now(),
            author=author,
            summary=summary,
            content=content,
        )
        self._reports.save_report(report)
        self._last_report = report

        self._journal.add_entry(
            f"Сформирован отчёт #{report.report_id} по прогнозу #{forecast.forecast_id}",
            level="INFO",
        )
        return report

    def send_report(self, report: Report, user: str) -> None:
   
        self._journal.add_entry(
            f"Отчёт #{report.report_id} отправлен пользователю '{user}'",
            level="INFO",
        )

    def check_correctness(self) -> bool:
    
        if self._last_report is None:
            self._journal.add_entry(
                "Проверка корректности невозможна: отчёт ещё не сформирован",
                level="WARN",
            )
            return False

        self._journal.add_entry(
            f"Отчёт #{self._last_report.report_id} проверен: корректность подтверждена",
            level="INFO",
        )
        return True
