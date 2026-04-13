# -*- coding: utf-8 -*-
# Σ-NEREA / sigma_avatarus/meridians/meridian_nodes.py
"""
12 меридианных узлов системы Σ-Avatarus.

Каждый узел отвечает за свой функциональный домен:
  M01  — Тезис (входящий импульс)
  M02  — Антитезис (инверсия / критика)
  M03  — Лексикон (семантический контроль)
  M04  — Память (архетипическое хранилище)
  M05  — Резонанс (частотный анализ синтеза)
  M06  — Этика (Decision Matrix / LexiconGuard)
  M07  — Исполнение (SynapticExecutor)
  M08  — Защита (SemanticShield)
  M09  — Компиляция (FDLCompiler → JSON/YAML/Graph)
  M10  — Хранилище (DataVault)
  M11  — Сеть агентов (AgentMesh)
  M12  — Рефлекция (SigmaReflector / обратная связь)
"""

from __future__ import annotations
import re
import json
import time
import hashlib
from typing import Any

from core.meridian_base import MeridianNode, MeridianPacket


# ─────────────────────────────────────────
#  M01 — ТЕЗИС
# ─────────────────────────────────────────
class M01_Thesis(MeridianNode):
    """Принимает первичный импульс, формирует тезис для ФДЛ-цикла."""

    domain_signature = "THESIS::INPUT"

    def __init__(self):
        super().__init__("M01", "Тезис")

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        raw = str(packet.payload)
        thesis = raw.strip() if raw.strip() else f"NULL_THESIS_{int(time.time())}"
        self._emit_log("THESIS_FORMED", thesis[:80])
        return MeridianPacket(
            source=self.node_id,
            payload=thesis,
            packet_type="data",
            metadata={"domain": self.domain_signature, "original": raw},
        )


# ─────────────────────────────────────────
#  M02 — АНТИТЕЗИС
# ─────────────────────────────────────────
class M02_Antithesis(MeridianNode):
    """Генерирует антитезис: формально-символическое отрицание тезиса."""

    domain_signature = "ANTITHESIS::INVERSION"

    def __init__(self):
        super().__init__("M02", "Антитезис")

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        thesis = str(packet.payload)
        antithesis = f"¬({thesis})"
        self._emit_log("ANTITHESIS_GENERATED", antithesis[:80])
        return MeridianPacket(
            source=self.node_id,
            payload={"thesis": thesis, "antithesis": antithesis},
            packet_type="data",
            metadata={"domain": self.domain_signature},
        )


# ─────────────────────────────────────────
#  M03 — ЛЕКСИКОН
# ─────────────────────────────────────────
class M03_Lexicon(MeridianNode):
    """
    Семантический контроль: проверяет лексику на соответствие FDL-словарю.
    Блокирует пустые, мусорные или конфликтные конструкции.
    """

    domain_signature = "LEXICON::SEMANTIC_CONTROL"

    _BLOCKED = re.compile(
        r"\b(null|none|undefined|error|nan|inf|fault)\b", re.IGNORECASE
    )
    _SYNTH_OK = re.compile(r"SYNTH\[.+\]")

    def __init__(self):
        super().__init__("M03", "Лексикон")

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        text = str(packet.payload)

        # Блокировка мусора
        if self._BLOCKED.search(text):
            self._emit_log("BLOCKED", text[:80])
            return MeridianPacket(
                source=self.node_id,
                payload={"status": "BLOCKED", "reason": "forbidden_token", "original": text},
                packet_type="error",
                metadata={"domain": self.domain_signature},
            )

        # Нормализация SYNTH-конструкции
        synth_match = self._SYNTH_OK.search(text)
        normalized = synth_match.group(0) if synth_match else text.strip()

        self._emit_log("LEXICON_PASS", normalized[:80])
        return MeridianPacket(
            source=self.node_id,
            payload=normalized,
            packet_type="data",
            metadata={"domain": self.domain_signature, "synth_detected": bool(synth_match)},
        )


# ─────────────────────────────────────────
#  M04 — ПАМЯТЬ
# ─────────────────────────────────────────
class M04_Memory(MeridianNode):
    """
    Архетипическое хранилище: сохраняет и извлекает пары (тезис, синтез),
    обогащая контекст активными образами.
    """

    domain_signature = "MEMORY::ARCHAI_STORE"

    def __init__(self):
        super().__init__("M04", "Память")
        self._store: dict[str, str] = {}   # thesis_hash → synthesis

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        data = packet.payload

        # Режим записи
        if isinstance(data, dict) and "synthesis" in data:
            key = hashlib.md5(str(data.get("thesis", "")).encode()).hexdigest()[:8]
            self._store[key] = data["synthesis"]
            self._emit_log("STORED", f"key={key}")
            return MeridianPacket(
                source=self.node_id,
                payload={**data, "memory_key": key},
                packet_type="data",
                metadata={"domain": self.domain_signature},
            )

        # Режим запроса: ищем похожий тезис
        query = str(data)
        key   = hashlib.md5(query.encode()).hexdigest()[:8]
        recall = self._store.get(key)
        self._emit_log("RECALL", f"key={key} hit={recall is not None}")
        return MeridianPacket(
            source=self.node_id,
            payload={"query": query, "recall": recall},
            packet_type="data",
            metadata={"domain": self.domain_signature},
        )

    def dump(self) -> dict:
        return dict(self._store)


# ─────────────────────────────────────────
#  M05 — РЕЗОНАНС
# ─────────────────────────────────────────
class M05_Resonance(MeridianNode):
    """
    Частотный анализ синтеза.
    Вычисляет «резонансный балл» — метрику семантической плотности
    через подсчёт уникальных смысловых единиц.
    """

    domain_signature = "RESONANCE::FREQUENCY_ANALYSIS"

    def __init__(self):
        super().__init__("M05", "Резонанс")

    def _score(self, text: str) -> float:
        words  = text.split()
        unique = len(set(w.lower() for w in words))
        return round(unique / max(len(words), 1), 4)

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        text  = str(packet.payload)
        score = self._score(text)
        level = "HIGH" if score > 0.7 else "MID" if score > 0.4 else "LOW"
        self._emit_log("RESONANCE", f"score={score} level={level}")
        return MeridianPacket(
            source=self.node_id,
            payload={"text": text, "resonance_score": score, "level": level},
            packet_type="data",
            metadata={"domain": self.domain_signature},
        )


# ─────────────────────────────────────────
#  M06 — ЭТИКА
# ─────────────────────────────────────────
class M06_Ethics(MeridianNode):
    """
    Decision Matrix: фильтр деструктивных, аморальных и дисгармоничных паттернов.
    Реализует LexiconGuard второго уровня (после M03).
    """

    domain_signature = "ETHICS::DECISION_MATRIX"

    _IMMORAL = re.compile(
        r"\b(ненависть|агрессия|уничтож|манипуляц|эксплуатац|hate|destroy|manipulat)\b",
        re.IGNORECASE,
    )

    def __init__(self):
        super().__init__("M06", "Этика")

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        text = str(packet.payload)
        if self._IMMORAL.search(text):
            self._emit_log("ETHICS_BLOCK", text[:80])
            return MeridianPacket(
                source=self.node_id,
                payload={"status": "ETHICS_VIOLATION", "original": text},
                packet_type="error",
                metadata={"domain": self.domain_signature},
            )
        self._emit_log("ETHICS_PASS", text[:60])
        return MeridianPacket(
            source=self.node_id,
            payload=text,
            packet_type="data",
            metadata={"domain": self.domain_signature, "verdict": "ГАРМОНИЯ"},
        )


# ─────────────────────────────────────────
#  M07 — ИСПОЛНЕНИЕ
# ─────────────────────────────────────────
class M07_Executor(MeridianNode):
    """
    SynapticExecutor: запускает зарегистрированные действия
    при обнаружении паттерна SYNTH[…] в потоке данных.
    """

    domain_signature = "EXECUTOR::SYNAPTIC_ACTION"

    def __init__(self):
        super().__init__("M07", "Исполнение")
        self._actions: dict[str, callable] = {}

    def register(self, key: str, fn: callable) -> None:
        self._actions[key] = fn

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        text = str(packet.payload)
        match = re.search(r"SYNTH\[(.+?)\]", text)
        if match:
            terms = [t.strip() for t in match.group(1).split("⊕")]
            fired = {}
            for term in terms:
                if term in self._actions:
                    fired[term] = self._actions[term](text)
            self._emit_log("EXECUTED", str(fired))
            return MeridianPacket(
                source=self.node_id,
                payload={"input": text, "fired": fired, "terms": terms},
                packet_type="data",
                metadata={"domain": self.domain_signature},
            )
        self._emit_log("NO_ACTION", text[:60])
        return MeridianPacket(
            source=self.node_id,
            payload=text,
            packet_type="data",
            metadata={"domain": self.domain_signature},
        )


# ─────────────────────────────────────────
#  M08 — ЗАЩИТА
# ─────────────────────────────────────────
class M08_Shield(MeridianNode):
    """
    SemanticShield: финальный барьер перед синтезом.
    Отклоняет повреждённые, неполные и галлюцинаторные конструкции.
    """

    domain_signature = "SHIELD::SEMANTIC_GUARD"

    _GARBAGE = re.compile(r"(\?\?\?|!!!|\?\!|undefined|NaN|<error>)", re.IGNORECASE)

    def __init__(self):
        super().__init__("M08", "Защита")

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        text = str(packet.payload)
        if not text.strip() or len(text) < 3:
            self._emit_log("SHIELD_BLOCK", "empty_payload")
            return MeridianPacket(
                source=self.node_id,
                payload={"status": "SHIELD_EMPTY"},
                packet_type="error",
                metadata={"domain": self.domain_signature},
            )
        if self._GARBAGE.search(text):
            self._emit_log("SHIELD_BLOCK", text[:60])
            return MeridianPacket(
                source=self.node_id,
                payload={"status": "SHIELD_GARBAGE", "original": text},
                packet_type="error",
                metadata={"domain": self.domain_signature},
            )
        self._emit_log("SHIELD_PASS", text[:60])
        return MeridianPacket(
            source=self.node_id,
            payload=text,
            packet_type="data",
            metadata={"domain": self.domain_signature, "verdict": "ЧИСТЫЙ"},
        )


# ─────────────────────────────────────────
#  M09 — КОМПИЛЯЦИЯ
# ─────────────────────────────────────────
class M09_Compiler(MeridianNode):
    """
    FDLCompiler: сериализует данные диалогического поля
    в JSON, YAML или текстовый форматы для экспорта.
    """

    domain_signature = "COMPILER::FDL_SERIALIZER"

    def __init__(self, output_format: str = "json"):
        super().__init__("M09", "Компиляция")
        self.output_format = output_format  # json | yaml | text

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        data = packet.payload
        try:
            if self.output_format == "json":
                compiled = json.dumps(
                    data if isinstance(data, dict) else {"value": str(data)},
                    ensure_ascii=False, indent=2
                )
            elif self.output_format == "yaml":
                d = data if isinstance(data, dict) else {"value": str(data)}
                compiled = "\n".join(f"{k}: {v}" for k, v in d.items())
            else:
                compiled = str(data)
            self._emit_log("COMPILED", f"format={self.output_format}")
            return MeridianPacket(
                source=self.node_id,
                payload=compiled,
                packet_type="data",
                metadata={"domain": self.domain_signature, "format": self.output_format},
            )
        except Exception as e:
            self._emit_log("COMPILE_ERROR", str(e))
            return MeridianPacket(
                source=self.node_id,
                payload={"status": "COMPILE_ERROR", "error": str(e)},
                packet_type="error",
                metadata={"domain": self.domain_signature},
            )


# ─────────────────────────────────────────
#  M10 — ХРАНИЛИЩЕ
# ─────────────────────────────────────────
class M10_Vault(MeridianNode):
    """
    DataVault: персистентное хранилище синтезов.
    Логирует все завершённые FDL-циклы с временными метками.
    """

    domain_signature = "VAULT::DATA_PERSISTENCE"

    def __init__(self):
        super().__init__("M10", "Хранилище")
        self.entries: list[dict] = []

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        data = packet.payload
        entry = {
            "id":        hashlib.md5(str(data).encode()).hexdigest()[:8],
            "timestamp": time.time(),
            "source":    packet.source,
            "data":      data,
        }
        self.entries.append(entry)
        self._emit_log("STORED", f"id={entry['id']}")
        return MeridianPacket(
            source=self.node_id,
            payload={"stored": True, "entry_id": entry["id"], "total": len(self.entries)},
            packet_type="data",
            metadata={"domain": self.domain_signature},
        )

    def query(self, keyword: str) -> list[dict]:
        return [e for e in self.entries if keyword.lower() in str(e["data"]).lower()]


# ─────────────────────────────────────────
#  M11 — СЕТЬ АГЕНТОВ
# ─────────────────────────────────────────
class M11_AgentMesh(MeridianNode):
    """
    AgentMesh: управляет несколькими FDL-агентами,
    рассылает синтез-запросы и собирает консенсус.
    """

    domain_signature = "MESH::AGENT_NETWORK"

    def __init__(self):
        super().__init__("M11", "Сеть агентов")
        self._agents: dict[str, dict] = {}

    def register_agent(self, name: str, capabilities: list[str] = None) -> None:
        self._agents[name] = {
            "name": name,
            "capabilities": capabilities or [],
            "state": "IDLE",
        }

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        data = packet.payload
        thesis = str(data.get("thesis", data) if isinstance(data, dict) else data)
        antithesis = str(data.get("antithesis", f"¬({thesis})") if isinstance(data, dict) else f"¬({thesis})")

        results = {}
        for name in self._agents:
            self._agents[name]["state"] = "ACTIVE"
            synthesis = f"Σ[{name}]({thesis} ⊕ {antithesis})"
            results[name] = synthesis
            self._agents[name]["state"] = "IDLE"

        self._emit_log("MESH_BROADCAST", f"agents={list(self._agents.keys())}")
        return MeridianPacket(
            source=self.node_id,
            payload={"agents": len(self._agents), "syntheses": results},
            packet_type="data",
            metadata={"domain": self.domain_signature},
        )


# ─────────────────────────────────────────
#  M12 — РЕФЛЕКЦИЯ
# ─────────────────────────────────────────
class M12_Reflector(MeridianNode):
    """
    SigmaReflector: анализирует пройденный FDL-цикл,
    выявляет конфликты и формирует обратную связь для Master-Node.
    """

    domain_signature = "REFLECTOR::FEEDBACK_LOOP"

    def __init__(self):
        super().__init__("M12", "Рефлекция")

    def process(self, packet: MeridianPacket) -> MeridianPacket:
        data = packet.payload
        text = str(data)

        # Детектирование конфликта: тезис == антитезис
        conflict = False
        if isinstance(data, dict):
            t = str(data.get("thesis", ""))
            a = str(data.get("antithesis", ""))
            conflict = (t == a and bool(t))

        issues = []
        if conflict:
            issues.append("CONFLICT: тезис совпадает с антитезисом")
        if len(text) > 2000:
            issues.append("OVERLOAD: данные превышают лимит")
        if "error" in text.lower():
            issues.append("ERROR_DETECTED: ошибка в потоке")

        verdict = "CONFLICT_DETECTED" if issues else "FIELD_COHERENT"
        self._emit_log("REFLECT", f"verdict={verdict} issues={issues}")

        return MeridianPacket(
            source=self.node_id,
            payload={
                "verdict":   verdict,
                "issues":    issues,
                "coherent":  not bool(issues),
                "feedback":  f"Рефлекция M12 → {verdict}",
                "original":  data,
            },
            packet_type="data",
            metadata={"domain": self.domain_signature},
        )
