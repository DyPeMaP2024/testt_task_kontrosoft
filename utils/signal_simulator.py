"""
TCP-симулятор удалённого сервиса сигналов (порт 2001 по умолчанию).

Протокол (JSON Lines, UTF-8, завершение строки \\n):
  Клиент → сервер: {"cmd": "get_signals"}
  Сервер → клиент: {"signals": [ {id, name, value, quality, timestamp}, ... ]}
"""

from __future__ import annotations

import json
import math
import random
import socket
import threading
import time
from datetime import datetime, timezone
from typing import Optional

from config.settings import get_settings


class SignalSimulator:
    """Минимальный сервис-симулятор для ручных и автотестов."""

    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        settings = get_settings()
        self.host = host or settings.host
        self.port = port if port is not None else settings.port
        self.signal_count = settings.expected_signal_count
        self._server: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self._t0 = time.time()

    def start(self) -> None:
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.host, self.port))
        self._server.listen(5)
        self._server.settimeout(0.5)

        self._stop.clear()
        self._thread = threading.Thread(target=self._serve_forever, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)
        if self._server:
            try:
                self._server.close()
            except OSError:
                pass
            self._server = None

    def _serve_forever(self) -> None:
        assert self._server is not None
        while not self._stop.is_set():
            try:
                client, _ = self._server.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            threading.Thread(
                target=self._handle_client, args=(client,), daemon=True
            ).start()

    def _handle_client(self, client: socket.socket) -> None:
        client.settimeout(1.0)
        buffer = ""
        try:
            while not self._stop.is_set():
                try:
                    chunk = client.recv(4096)
                except socket.timeout:
                    continue
                if not chunk:
                    break

                buffer += chunk.decode("utf-8")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    request = json.loads(line)
                    if request.get("cmd") == "get_signals":
                        payload = {"signals": self._build_signals()}
                        client.sendall(
                            (json.dumps(payload) + "\n").encode("utf-8")
                        )
        except (OSError, json.JSONDecodeError):
            pass
        finally:
            try:
                client.close()
            except OSError:
                pass

    def _build_signals(self) -> list[dict]:
        elapsed = time.time() - self._t0
        now = datetime.now(timezone.utc).isoformat()
        signals = []

        for i in range(1, self.signal_count + 1):
            if i <= 5:
                value = round(math.sin(elapsed + i) * 100, 3)
            else:
                value = round(random.uniform(-50, 50), 3)

            signals.append(
                {
                    "id": i,
                    "name": f"Signal_{i}",
                    "value": value,
                    "quality": "good",
                    "timestamp": now,
                }
            )
        return signals


def main() -> None:
    settings = get_settings()
    sim = SignalSimulator()
    sim.start()
    print(f"Signal simulator listening on {settings.host}:{settings.port}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        sim.stop()


if __name__ == "__main__":
    main()
