from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional





@dataclass
class Sensor:
 
    sensor_id: int
    type: str
    unit: str
    poll_frequency: int
    value: float = 0.0

    def read_value(self) -> float:
       
        return self.value


@dataclass
class Level:
  
    level_id: int
    name: str
    difficulty: float
    parameters: Dict[str, float]
    description: str

    def update_parameters(self, new_parameters: Dict[str, float]) -> None:
   
        self.parameters.update(new_parameters)

    def calculate_difficulty(self) -> float:
      
        if not self.parameters:
            return self.difficulty

        avg_value = sum(self.parameters.values()) / len(self.parameters)
        self.difficulty = avg_value
        return self.difficulty


@dataclass
class StorageRecord:

    timestamp: datetime
    sensor_id: int
    value: float
    event_type: str


@dataclass
class Report:

    report_id: int
    created_at: datetime
    author: str
    summary: str
    content: str

    def export(self, fmt: str) -> str:
     
        return f"[FORMAT={fmt}] {self.content}"


@dataclass
class Forecast:

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
     
        if passability_score is None:
            #  чем выше сложность, тем ниже проходимость.
            passability_score = max(0.0, 1.0 - level.difficulty)

        return cls(
            forecast_id=forecast_id,
            level_name=level.name,
            passability_score=passability_score,
            recommendations=recommendations,
            created_at=datetime.now(),
        )
