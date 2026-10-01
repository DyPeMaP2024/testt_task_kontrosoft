# Практическое задание: десктоп-клиент сигналов + TCP-симулятор

## Структура

```
config/          # настройки (host, port, timeout)
fixtures/        # pytest-фикстуры (симулятор, main_window)
pages/           # Page Object Model
  components/    # таблица сигналов
utils/           # TCP-клиент и симулятор
tests/           # автотесты
CHECKLIST.md     # чек-лист и обоснование критичного сценария
```

## Часть 1 — Чек-лист

См. [CHECKLIST.md](CHECKLIST.md) (15 пунктов).

## Часть 2 — Критичный сценарий

**Подключение + получение всех 10 сигналов** через POM (`MainWindowPage`).

```bash
pip install -r requirements.txt
pytest -v
```

Симулятор вручную (порт 2001):

```bash
python -m utils.signal_simulator
```
