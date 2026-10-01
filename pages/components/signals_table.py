"""Компонент таблицы сигналов главного окна."""

from __future__ import annotations

from typing import List

from utils.models import Signal


class SignalsTable:
    """
    Page Object компонента «таблица сигналов».

    Колонки по ТЗ: ID, имя, значение, качество, время.
    """

    COLUMNS = ("id", "name", "value", "quality", "timestamp")

    def __init__(self) -> None:
        self._rows: List[Signal] = []

    def update(self, signals: List[Signal]) -> None:
        """Обновляет «отображаемые» строки после refresh."""
        self._rows = list(signals)

    @property
    def rows(self) -> List[Signal]:
        return list(self._rows)

    def row_count(self) -> int:
        return len(self._rows)

    def signal_ids(self) -> List[int]:
        return sorted(row.id for row in self._rows)

    def expect_all_columns_filled(self) -> None:
        """Проверяет, что у каждой строки заполнены все колонки таблицы."""
        for signal in self._rows:
            assert signal.name, f"Пустое имя у сигнала id={signal.id}"
            assert isinstance(signal.value, float), (
                f"value должен быть числом, id={signal.id}"
            )
            assert signal.quality, f"Пустое качество у сигнала id={signal.id}"
            assert signal.timestamp, f"Пустое время у сигнала id={signal.id}"

            for field in self.COLUMNS:
                assert hasattr(signal, field), f"Нет поля '{field}' у сигнала"
