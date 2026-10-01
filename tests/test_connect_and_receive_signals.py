"""
Критичный автотест (чек-лист п.4–6):

  Подключение к сервису → «Обновить» → в таблице ровно 10 сигналов
  с полями ID, имя, значение, качество, время.

Почему сценарий критичен — см. CHECKLIST.md.
"""

from __future__ import annotations

import pytest

from config.settings import Settings
from pages.main_window_page import MainWindowPage


@pytest.mark.smoke
@pytest.mark.critical
class TestConnectAndReceiveSignals:
    def test_connect_and_receive_all_signals(
        self,
        main_window: MainWindowPage,
        settings: Settings,
    ) -> None:
        """
        Happy-path через Page Object главного окна:
          1. «Подключиться»
          2. «Обновить»
          3. Assert: 10 строк, ID 1..10, все колонки заполнены
        """
        # Шаг 1: кнопка «Подключиться»
        main_window.click_connect()
        main_window.expect_connected()

        # Шаг 2: кнопка «Обновить» → данные попадают в таблицу
        main_window.click_refresh()

        # Шаг 3: проверки результата в таблице сигналов
        expected_count = settings.expected_signal_count
        main_window.expect_signal_count(expected_count)
        main_window.expect_signal_ids(list(range(1, expected_count + 1)))
        main_window.signals_table.expect_all_columns_filled()

    def test_connect_fails_when_simulator_is_down(
        self,
        disconnected_window: MainWindowPage,
    ) -> None:
        """
        Негатив (чек-лист п.9): сервис недоступен →
        «Подключиться» падает, окно остаётся без соединения.
        """
        with pytest.raises(OSError):
            disconnected_window.click_connect()

        disconnected_window.expect_not_connected()
