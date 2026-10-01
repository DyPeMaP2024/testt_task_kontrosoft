"""Базовый Page Object для десктоп-окна приложения."""

from __future__ import annotations

from utils.signal_client import SignalClient


class BasePage:
    def __init__(self, client: SignalClient) -> None:
        # Транспортный слой (аналог driver/page в UI-автотестах)
        self.client = client
