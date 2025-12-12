from __future__ import annotations

from statistics import mean
from typing import Dict, List, Optional

from model import Level, StorageRecord, StorageRepository, Forecast, ForecastRepository
from .journal import JournalManager


class AnalysisController:
  

    def __init__(
        self,
        storage_repository: StorageRepository,
        forecast_repository: ForecastRepository,
        journal: Optional[JournalManager] = None,
    ) -> None:
        self._storage = storage_repository
        self._forecasts = forecast_repository
        self._journal = journal or JournalManager()
        self._last_analysis: Dict[str, float] = {}

    def analyze_data(self, level: Level) -> Dict[str, float]:
       
        records: List[StorageRecord] = self._storage.get_all()
        values = [r.value for r in records]

        stats: Dict[str, float] = {
            "records_count": float(len(records)),
            "average_value": float(mean(values)) if values else 0.0,
            "level_difficulty": float(level.difficulty),
        }

        self._last_analysis = stats
        self._journal.add_entry(
            f"Анализ завершён для уровня '{level.name}': {stats}",
            level="INFO",
        )
        return stats

    def create_forecast(self, level: Level) -> Forecast:
      
        analysis = self._last_analysis or self.analyze_data(level)

        avg_value = analysis.get("average_value", 0.0)
        difficulty = analysis.get("level_difficulty", level.difficulty)


        avg_norm = min(1.0, avg_value / 120.0)

        raw_score = 1.0 - (0.5 * difficulty + 0.5 * avg_norm)

        base_passability = max(0.0, min(1.0, raw_score))

        forecast_id = len(self._forecasts.get_all()) + 1
        recommendations = (
            "Снизить сложность уровня"
            if base_passability < 0.5
            else "Уровень сбалансирован"
        )

        forecast = Forecast.from_level(
            forecast_id=forecast_id,
            level=level,
            recommendations=recommendations,
            passability_score=base_passability,
        )
        self._forecasts.save_forecast(forecast)
        self._journal.add_entry(
            f"Создан прогноз #{forecast.forecast_id} для уровня '{level.name}'",
            level="INFO",
        )
        return forecast

    def evaluate_results(self) -> Dict[str, float]:
       
        self._journal.add_entry(
            f"Оценка результатов: {self._last_analysis}",
            level="INFO",
        )
        return dict(self._last_analysis)
