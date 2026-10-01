"""
TCP-клиент протокола JSON Lines.

Низкоуровневый транспорт: connect / refresh / disconnect.
UI-действия живут в Page Object (`pages/main_window_page.py`).
"""

from __future__ import annotations

import json
import socket
from typing import List

from utils.models import Signal


class SignalClient:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 2001,
        timeout: float = 3.0,
    ) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self._sock: socket.socket | None = None

    @property
    def is_connected(self) -> bool:
        return self._sock is not None

    def connect(self) -> None:
        if self._sock is not None:
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        try:
            sock.connect((self.host, self.port))
        except OSError:
            sock.close()
            raise
        self._sock = sock

    def disconnect(self) -> None:
        if self._sock is not None:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None

    def get_signals(self) -> List[Signal]:
        """Запрос {"cmd": "get_signals"} → список Signal."""
        if self._sock is None:
            raise RuntimeError("Not connected: call connect() first")

        request = json.dumps({"cmd": "get_signals"}) + "\n"
        self._sock.sendall(request.encode("utf-8"))

        raw = self._recv_line()
        payload = json.loads(raw)
        signals_raw = payload.get("signals")
        if not isinstance(signals_raw, list):
            raise ValueError("Invalid response: 'signals' must be a list")

        return [self._parse_signal(item) for item in signals_raw]

    def _recv_line(self) -> str:
        assert self._sock is not None
        chunks: list[bytes] = []
        while True:
            chunk = self._sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
            if b"\n" in chunk:
                break
        data = b"".join(chunks).decode("utf-8")
        line, _, _ = data.partition("\n")
        return line.strip()

    @staticmethod
    def _parse_signal(item: dict) -> Signal:
        required = ("id", "name", "value", "quality", "timestamp")
        missing = [key for key in required if key not in item]
        if missing:
            raise ValueError(f"Signal missing fields: {missing}")

        return Signal(
            id=int(item["id"]),
            name=str(item["name"]),
            value=float(item["value"]),
            quality=str(item["quality"]),
            timestamp=str(item["timestamp"]),
        )
