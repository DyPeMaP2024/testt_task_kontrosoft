"""Настройки стенда: хост/порт симулятора и ожидания по ТЗ."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    timeout: float
    expected_signal_count: int
    # Порт, на котором заведомо никто не слушает (негативные тесты)
    dead_port: int


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        host=os.getenv("SIGNAL_HOST", "127.0.0.1"),
        port=int(os.getenv("SIGNAL_PORT", "2001")),
        timeout=float(os.getenv("SIGNAL_TIMEOUT", "2.0")),
        expected_signal_count=int(os.getenv("EXPECTED_SIGNAL_COUNT", "10")),
        dead_port=int(os.getenv("DEAD_PORT", "1")),
    )
