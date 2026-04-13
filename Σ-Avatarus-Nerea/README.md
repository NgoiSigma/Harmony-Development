[README.md](https://github.com/user-attachments/files/26676004/README.md)
# ⧫⟡⧫ Σ-Avatarus · NEREA · NГОИ ⧫⟡⧫

**Модуль 13-узловой FDL-архитектуры** для платформы Σ-NEREA.  
Реализует детерминированный пайплайн обработки смыслов без галлюцинаций.

---

## Топология

```
Входные данные
      │
      ▼
  M01 (Тезис) ──────────────────────────────────────────┐
  M02 (Антитезис)                                       │
  M03 (Лексикон / семантический контроль)               │
  M04 (Память / архетипическое хранилище)               │
  M05 (Резонанс / частотный анализ)                     │
  M06 (Этика / Decision Matrix)           12 меридианов│
  M07 (Исполнение / SynapticExecutor)                   │
  M08 (Защита / SemanticShield)                         │
  M09 (Компиляция / FDLSerializer)                      │
  M10 (Хранилище / DataVault)                           │
  M11 (Сеть агентов / AgentMesh)                        │
  M12 (Рефлекция / SigmaReflector) ────────────────────┘
      │
      ▼
  M13 (MasterNode / КРСО — Центральный синхронизатор)
      │
      ▼
  KRSO-индекс + Вердикт + Трасса
```

### Логика M13: Зн(П) → КРСО

| Показатель (П) | Вес | Что измеряет |
|----------------|-----|--------------|
| completeness   | 35% | Доля успешно пройденных узлов |
| coherence      | 30% | Отсутствие ошибочных пакетов |
| resonance      | 20% | Семантическая плотность (M05) |
| integrity      | 15% | Корректность подписей пакетов |

**Вердикты КРСО:**
- `SYNTHESIS_CONFIRMED` — индекс ≥ 0.85
- `SYNTHESIS_PARTIAL`   — индекс ≥ 0.60
- `SYNTHESIS_DEGRADED`  — индекс ≥ 0.40
- `SYNTHESIS_FAILED`    — индекс < 0.40

---

## Структура репозитория

```
sigma_avatarus/
├── avatarus_sigma.py          — главная точка входа
├── run_all.py                 — запуск тестов и demo
│
├── core/
│   ├── meridian_base.py       — базовый класс MeridianNode + MeridianPacket
│   └── fdl_logic_engine.py    — FDLLogicEngine (T→A→S→Emit)
│
├── meridians/
│   └── meridian_nodes.py      — все 12 меридианов (M01–M12)
│
├── master_node/
│   └── master_node.py         — M13 + KRSO
│
├── interfaces/
│   └── api_server.py          — FastAPI REST (порт 8000)
│
├── tests/
│   └── test_avatarus_sigma.py — полный тест-сьют
│
└── config/
    └── settings.py            — конфигурация системы
```

---

## Быстрый старт

```bash
# 1. Установка зависимостей
pip install fastapi uvicorn pytest

# 2. Smoke-тест (без pytest, < 5 сек)
python run_all.py --smoke

# 3. Полный тест-сьют
python run_all.py
# или: pytest tests/ -v

# 4. Демонстрация FDL-цикла
python run_all.py --demo

# 5. REST API
uvicorn interfaces.api_server:app --reload --port 8000
```

---

## Использование

```python
from avatarus_sigma import AvatarusSigma

ava = AvatarusSigma("МойАгент")

# Полный FDL-цикл через все 12 меридианов
result = ava.synthesize("Свобода", "Ответственность")
print(result["krso"]["verdict"])    # → SYNTHESIS_CONFIRMED
print(result["krso"]["index"])      # → 0.87

# inject_node — совместимость с оригинальным NEREA API
r = ava.inject_node("Знание", "Опыт")

# Functional Presence: проверка всех 12 узлов
health = ava.health_check()
print(f"{health['nodes_alive']}/12 узлов активны")

# Прямой вызов конкретного меридиана через M13
from core.meridian_base import MeridianPacket
pkt = ava.master.route("M05", "Свет Тьма Время Знание Путь")
print(pkt.payload["resonance_score"])

# Поиск по хранилищу
matches = ava.vault_search("Свет")
```

---

## REST API (порт 8000)

| Method | Endpoint | Описание |
|--------|----------|----------|
| GET | `/` | Информация о системе |
| POST | `/synthesize` | Запуск FDL-пайплайна |
| POST | `/inject` | inject_node (совместимость) |
| GET | `/health` | Functional Presence + КРСО |
| GET | `/krso` | Текущий КРСО-индекс |
| GET | `/status` | Полный статус через M13 |
| GET | `/cycle/last` | Результат последнего цикла |
| GET | `/vault/search?q=...` | Поиск по DataVault |
| POST | `/agent/register` | Регистрация агента в M11 |

```bash
# Запуск FDL-цикла через API
curl -X POST http://localhost:8000/synthesize \
  -H "Content-Type: application/json" \
  -d '{"thesis": "Знание", "antithesis": "Мудрость"}'

# Functional Presence
curl http://localhost:8000/health
```

---

## Механизм Functional Presence

Каждый узел в режиме реального времени:
1. **verify(packet)** — проверяет подпись SHA-256 входящего пакета
2. **process(packet)** — обрабатывает в своём домене
3. **sign(result)**   — подписывает исходящий пакет

M13 при сбое верификации на любом узле:
- фиксирует ошибку в `error_log`
- передаёт пакет дальше (bypass) без остановки пайплайна
- снижает метрику `coherence` в КРСО

---

## Авторство

**Методология:** А.Е. Кашеварова, ФДЛ (1979), НГОИ/ММТД, г. Николаев  
**Архитектура Σ-Avatarus:** NGOI-SIGMA  
**Протокол:** NEBI-ULA · Σ-NEREA v1.0.0  
**Лицензия:** Apache 2.0 with FDL-Invariant Clause
