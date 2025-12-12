from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class LogEntry:
    """
    Класс «ЗаписьЖурнала» с диаграммы.

    Атрибуты:
        timestamp: время записи (время).
        level: уровень сообщения (уровень), например: INFO / WARN / ERROR.
        message: текст сообщения (сообщение).
    """
    timestamp: datetime
    level: str
    message: str


class JournalManager:
    """
    «МенеджерЖурнала».

    Отвечает за добавление записей в журнал, просмотр истории и очистку.
    Методы диаграммы:
        - добавитьЗапись(сообщение: string)
        - просмотретьИсторию(): list
        - очиститьИсторию()
    """

    def __init__(self) -> None:
        self._entries: List[LogEntry] = []

    def add_entry(self, message: str, level: str = "INFO") -> None:
        """добавитьЗапись(сообщение: string)"""
        entry = LogEntry(timestamp=datetime.now(), level=level, message=message)
        self._entries.append(entry)

    def view_history(self) -> List[LogEntry]:
        """просмотретьИсторию(): list"""
        return list(self._entries)

    def clear_history(self) -> None:
        """очиститьИсторию()"""
        self._entries.clear()
