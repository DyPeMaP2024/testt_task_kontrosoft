"""Page Object главного окна приложения отображения сигналов."""

from __future__ import annotations

from pages.base_page import BasePage
from pages.components.signals_table import SignalsTable
from utils.signal_client import SignalClient


class MainWindowPage(BasePage):
    """
    Главное окно:
      - кнопка «Подключиться»
      - кнопка «Обновить»
      - таблица сигналов
    """

    def __init__(self, client: SignalClient) -> None:
        super().__init__(client)
        self.signals_table = SignalsTable()
        self._last_error: Exception | None = None

    def click_connect(self) -> None:
        """Кнопка «Подключиться»."""
        self._last_error = None
        try:
            self.client.connect()
        except OSError as exc:
            self._last_error = exc
            raise

    def click_refresh(self) -> None:
        """Кнопка «Обновить» — запрос значений и обновление таблицы."""
        signals = self.client.get_signals()
        self.signals_table.update(signals)

    def close(self) -> None:
        """Закрытие окна / разрыв соединения."""
        self.client.disconnect()

    def expect_connected(self) -> None:
        assert self.client.is_connected, (
            "Ожидали активное соединение после «Подключиться»"
        )

    def expect_not_connected(self) -> None:
        assert not self.client.is_connected, "Ожидали отсутствие соединения"

    def expect_signal_count(self, expected: int) -> None:
        actual = self.signals_table.row_count()
        assert actual == expected, (
            f"Ожидали {expected} сигналов в таблице, получили {actual}"
        )

    def expect_signal_ids(self, expected_ids: list[int]) -> None:
        actual = self.signals_table.signal_ids()
        assert actual == expected_ids, (
            f"ID сигналов должны быть {expected_ids}, получили {actual}"
        )
