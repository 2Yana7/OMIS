from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class LogEntry:
 
    timestamp: datetime
    level: str
    message: str


class JournalManager:
  

    def __init__(self) -> None:
        self._entries: List[LogEntry] = []

    def add_entry(self, message: str, level: str = "INFO") -> None:
        entry = LogEntry(timestamp=datetime.now(), level=level, message=message)
        self._entries.append(entry)

    def view_history(self) -> List[LogEntry]:
        return list(self._entries)

    def clear_history(self) -> None:
        self._entries.clear()
