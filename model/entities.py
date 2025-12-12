from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


# ====== МОДЕЛЬНЫЕ КЛАССЫ (Диаграмма классов модели) ======


@dataclass
class Sensor:
    """
    Класс «Сенсор» (Сенсор на диаграмме).

    Атрибуты:
        sensor_id: идентификатор сенсора (идСенсора).
        type: тип сенсора (тип).
        unit: единицы измерения (единицы).
        poll_frequency: частота опроса в секундах (частотаОпроса).
        value: текущее значение (значение).
    """
    sensor_id: int
    type: str
    unit: str
    poll_frequency: int
    value: float = 0.0

    def read_value(self) -> float:
        """
        считатьЗначение(): float

        Имитация чтения значения с сенсора.
        В реальной системе здесь может быть обращение к устройству / SDK / API.
        """
        return self.value


@dataclass
class Level:
    """
    Класс «Уровень» (Уровень на диаграмме).

    Атрибуты:
        level_id: идентификатор уровня (идУровня).
        name: название (название).
        difficulty: сложность уровня (сложность).
        parameters: произвольные параметры уровня (параметр: map).
        description: текстовое описание уровня (описание).
    """
    level_id: int
    name: str
    difficulty: float
    parameters: Dict[str, float]
    description: str

    def update_parameters(self, new_parameters: Dict[str, float]) -> None:
        """
        обновитьПараметры(новые: map)

        Обновляет параметры уровня.
        """
        self.parameters.update(new_parameters)

    def calculate_difficulty(self) -> float:
        """
        вычислитьСложность(): float

        Простейший пример вычисления сложности на основе параметров.
        В реальной системе сюда можно встроить более сложную формулу.
        """
        if not self.parameters:
            return self.difficulty

        avg_value = sum(self.parameters.values()) / len(self.parameters)
        self.difficulty = avg_value
        return self.difficulty


@dataclass
class StorageRecord:
    """
    Класс «ЗаписьХранилища» (ЗаписьХранилища на диаграмме).

    Описывает одну запись о значении сенсора.

    Атрибуты:
        timestamp: время фиксации (время).
        sensor_id: идентификатор сенсора (идСенсора).
        value: измеренное значение (значение).
        event_type: тип события (типСобытия).
    """
    timestamp: datetime
    sensor_id: int
    value: float
    event_type: str


@dataclass
class Report:
    """
    Класс «Отчёт» (Отчёт на диаграмме).

    Атрибуты:
        report_id: идентификатор отчёта (идОтчёта).
        created_at: дата создания (датаСоздания).
        author: автор отчёта (автор).
        summary: краткое резюме (резюме).
        content: полное содержимое отчёта (содержимое).
    """
    report_id: int
    created_at: datetime
    author: str
    summary: str
    content: str

    def export(self, fmt: str) -> str:
        """
        экспортировать(формат: string)

        Возвращает содержимое отчёта в выбранном формате.
        Здесь для простоты — просто обёртка; реализация зависит от формата.
        """
        return f"[FORMAT={fmt}] {self.content}"


@dataclass
class Forecast:
    """
    Класс «Прогноз» (Прогноз на диаграмме).

    Атрибуты:
        forecast_id: идентификатор прогноза (идПрогноза).
        level_name: строковое имя уровня (уровень).
        passability_score: оценка проходимости (оценкаПроходимости).
        recommendations: текст рекомендаций (рекомендации).
        created_at: дата создания (датаСоздания).
    """
    forecast_id: int
    level_name: str
    passability_score: float
    recommendations: str
    created_at: datetime

    @classmethod
    def from_level(
        cls,
        forecast_id: int,
        level: Level,
        recommendations: str,
        passability_score: Optional[float] = None,
    ) -> "Forecast":
        """
        создатьПрогноз(уровень: Уровень)

        Вспомогательный конструктор, который создаёт прогноз по объекту Level.
        """
        if passability_score is None:
            # Простая формула: чем выше сложность, тем ниже проходимость.
            passability_score = max(0.0, 1.0 - level.difficulty)

        return cls(
            forecast_id=forecast_id,
            level_name=level.name,
            passability_score=passability_score,
            recommendations=recommendations,
            created_at=datetime.now(),
        )
