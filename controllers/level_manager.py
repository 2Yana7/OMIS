from __future__ import annotations

from typing import Dict, List, Optional

from model import Level, LevelRepository


class LevelManager:
    """
    «МенеджерУровней».

    Обёртка над репозиторием уровней.
    Методы диаграммы:
        - создатьУровень(данные)
        - редактироватьУровень(ид)
        - сохранитьУровень(уровень)
        - получитьСписокУровней()
        - удалитьУровень(ид)
    """

    def __init__(self, level_repository: LevelRepository) -> None:
        self._levels = level_repository

    def create_level(self, data: Dict) -> Level:
        """
        создатьУровень(данные)

        Ожидает словарь вида:
            {
                "id": int,
                "name": str,
                "difficulty": float,
                "parameters": dict[str, float],
                "description": str,
            }
        """
        level = Level(
            level_id=data["id"],
            name=data["name"],
            difficulty=float(data.get("difficulty", 0.0)),
            parameters=dict(data.get("parameters", {})),
            description=data.get("description", ""),
        )
        self._levels.save(level)
        return level

    def edit_level(self, level_id: int, updates: Dict) -> Optional[Level]:
        """
        редактироватьУровень(ид)

        Обновляет поля уровня по переданному словарю updates.
        """
        level = self._levels.load(level_id)
        if level is None:
            return None

        if "name" in updates:
            level.name = updates["name"]
        if "difficulty" in updates:
            level.difficulty = float(updates["difficulty"])
        if "parameters" in updates:
            level.parameters = dict(updates["parameters"])
        if "description" in updates:
            level.description = updates["description"]

        self._levels.save(level)
        return level

    def save_level(self, level: Level) -> None:
        """сохранитьУровень(уровень)"""
        self._levels.save(level)

    def get_levels(self) -> List[Level]:
        """получитьСписокУровней()"""
        return self._levels.get_all()

    def delete_level(self, level_id: int) -> None:
        """удалитьУровень(ид)"""
        self._levels.delete(level_id)
