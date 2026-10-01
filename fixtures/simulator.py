"""Фикстуры симулятора и Page Object главного окна."""

from __future__ import annotations

import socket
from typing import Generator

import pytest

from config.settings import Settings, get_settings
from pages.main_window_page import MainWindowPage
from utils.signal_client import SignalClient
from utils.signal_simulator import SignalSimulator


def _free_port() -> int:
    """Свободный локальный порт — тесты не конфликтуют с чужим :2001."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture
def running_simulator(settings: Settings) -> Generator[tuple[str, int], None, None]:
    """Поднимает симулятор на свободном порту на время теста."""
    host = settings.host
    port = _free_port()
    sim = SignalSimulator(host=host, port=port)
    sim.start()
    try:
        yield host, port
    finally:
        sim.stop()


@pytest.fixture
def main_window(
    running_simulator: tuple[str, int],
    settings: Settings,
) -> Generator[MainWindowPage, None, None]:
    """
    Page Object главного окна, привязанный к живому симулятору.
    После теста соединение закрывается.
    """
    host, port = running_simulator
    client = SignalClient(host=host, port=port, timeout=settings.timeout)
    page = MainWindowPage(client)
    try:
        yield page
    finally:
        page.close()


@pytest.fixture
def disconnected_window(settings: Settings) -> Generator[MainWindowPage, None, None]:
    """Главное окно без запущенного симулятора (негативные сценарии)."""
    client = SignalClient(
        host=settings.host,
        port=settings.dead_port,
        timeout=0.5,
    )
    page = MainWindowPage(client)
    try:
        yield page
    finally:
        page.close()
