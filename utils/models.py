"""Модели данных сигналов."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Signal:
    id: int
    name: str
    value: float
    quality: str
    timestamp: str
