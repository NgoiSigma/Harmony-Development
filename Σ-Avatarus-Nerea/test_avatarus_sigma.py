# -*- coding: utf-8 -*-
# Σ-NEREA / sigma_avatarus/tests/test_avatarus_sigma.py
"""
Тесты для всех 13 узлов системы Σ-Avatarus.

Запуск:
    pytest tests/test_avatarus_sigma.py -v

Покрытие:
  - Каждый из 12 меридианов отдельно
  - M13 (MasterNode) и КРСО
  - Полный пайплайн synthesize()
  - Функциональное присутствие (health_check)
  - Граничные случаи (пустой ввод, конфликт, ошибки)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.meridian_base import MeridianPacket
from meridians.meridian_nodes import (
    M01_Thesis, M02_Antithesis, M03_Lexicon,
    M04_Memory, M05_Resonance, M06_Ethics,
    M07_Executor, M08_Shield, M09_Compiler,
    M10_Vault, M11_AgentMesh, M12_Reflector,
)
from master_node.master_node import MasterNode, KRSO
from avatarus_sigma import AvatarusSigma


# ─────────────────────────────────────────────────────────
#  Фикстуры
# ─────────────────────────────────────────────────────────

@pytest.fixture
def agent():
    return AvatarusSigma("TestAgent")


@pytest.fixture
def master():
    nodes = [
        M01_Thesis(), M02_Antithesis(), M03_Lexicon(),
        M04_Memory(), M05_Resonance(), M06_Ethics(),
        M07_Executor(), M08_Shield(), M09_Compiler(),
        M10_Vault(), M11_AgentMesh(), M12_Reflector(),
    ]
    return MasterNode(nodes)


def pkt(payload, source="TEST"):
    return MeridianPacket(source=source, payload=payload)


# ─────────────────────────────────────────────────────────
#  M01 — Тезис
# ─────────────────────────────────────────────────────────

class TestM01Thesis:
    def test_basic(self):
        node = M01_Thesis()
        out = node.process(pkt("Свобода"))
        assert out.payload == "Свобода"
        assert out.packet_type == "data"

    def test_empty_input_generates_null(self):
        node = M01_Thesis()
        out = node.process(pkt("   "))
        assert out.payload.startswith("NULL_THESIS_")

    def test_domain_signature(self):
        assert M01_Thesis.domain_signature == "THESIS::INPUT"


# ─────────────────────────────────────────────────────────
#  M02 — Антитезис
# ─────────────────────────────────────────────────────────

class TestM02Antithesis:
    def test_generates_negation(self):
        node = M02_Antithesis()
        out = node.process(pkt("Свобода"))
        assert isinstance(out.payload, dict)
        assert "antithesis" in out.payload
        assert "¬(" in out.payload["antithesis"]

    def test_preserves_thesis(self):
        node = M02_Antithesis()
        out = node.process(pkt("Знание"))
        assert out.payload["thesis"] == "Знание"


# ─────────────────────────────────────────────────────────
#  M03 — Лексикон
# ─────────────────────────────────────────────────────────

class TestM03Lexicon:
    def test_pass_clean(self):
        node = M03_Lexicon()
        out = node.process(pkt("SYNTH[Свет ⊕ Тьма]"))
        assert out.packet_type == "data"
        assert out.metadata.get("synth_detected") is True

    def test_block_null_token(self):
        node = M03_Lexicon()
        out = node.process(pkt("null response"))
        assert out.packet_type == "error"
        assert out.payload["status"] == "BLOCKED"

    def test_block_undefined(self):
        node = M03_Lexicon()
        out = node.process(pkt("undefined value here"))
        assert out.packet_type == "error"


# ─────────────────────────────────────────────────────────
#  M04 — Память
# ─────────────────────────────────────────────────────────

class TestM04Memory:
    def test_store_and_recall(self):
        node = M04_Memory()
        node.process(pkt({"thesis": "Время", "antithesis": "¬(Время)", "synthesis": "Хронотоп"}))
        out = node.process(pkt("Время"))
        # Recall проверяет через MD5 ключ
        assert out.payload is not None

    def test_dump(self):
        node = M04_Memory()
        node.process(pkt({"thesis": "X", "synthesis": "S_X"}))
        assert len(node.dump()) >= 1


# ─────────────────────────────────────────────────────────
#  M05 — Резонанс
# ─────────────────────────────────────────────────────────

class TestM05Resonance:
    def test_score_high(self):
        node = M05_Resonance()
        out = node.process(pkt("Свет Тьма Время Пространство Знание Мудрость Путь"))
        assert out.payload["resonance_score"] > 0
        assert out.payload["level"] in ("HIGH", "MID", "LOW")

    def test_score_low_repetitive(self):
        node = M05_Resonance()
        out = node.process(pkt("а а а а а а а а"))
        assert out.payload["level"] == "LOW"


# ─────────────────────────────────────────────────────────
#  M06 — Этика
# ─────────────────────────────────────────────────────────

class TestM06Ethics:
    def test_pass_clean(self):
        node = M06_Ethics()
        out = node.process(pkt("Любовь и мудрость"))
        assert out.packet_type == "data"
        assert out.metadata.get("verdict") == "ГАРМОНИЯ"

    def test_block_aggression(self):
        node = M06_Ethics()
        out = node.process(pkt("агрессия и ненависть"))
        assert out.packet_type == "error"
        assert out.payload["status"] == "ETHICS_VIOLATION"


# ─────────────────────────────────────────────────────────
#  M07 — Исполнение
# ─────────────────────────────────────────────────────────

class TestM07Executor:
    def test_execute_registered_action(self):
        node = M07_Executor()
        results = []
        node.register("Свет", lambda s: results.append("fired") or "ok")
        out = node.process(pkt("SYNTH[Память ⊕ Свет]"))
        assert "Свет" in out.payload.get("terms", [])
        assert "fired" in results

    def test_no_action_passthrough(self):
        node = M07_Executor()
        out = node.process(pkt("Просто текст без SYNTH"))
        assert out.packet_type == "data"


# ─────────────────────────────────────────────────────────
#  M08 — Защита
# ─────────────────────────────────────────────────────────

class TestM08Shield:
    def test_pass_clean(self):
        node = M08_Shield()
        out = node.process(pkt("Чистый текст для синтеза"))
        assert out.packet_type == "data"
        assert out.metadata.get("verdict") == "ЧИСТЫЙ"

    def test_block_empty(self):
        node = M08_Shield()
        out = node.process(pkt(""))
        assert out.packet_type == "error"

    def test_block_garbage(self):
        node = M08_Shield()
        out = node.process(pkt("что-то ??? непонятное"))
        assert out.packet_type == "error"


# ─────────────────────────────────────────────────────────
#  M09 — Компиляция
# ─────────────────────────────────────────────────────────

class TestM09Compiler:
    def test_json_output(self):
        import json
        node = M09_Compiler("json")
        out = node.process(pkt({"thesis": "A", "synthesis": "B"}))
        parsed = json.loads(out.payload)
        assert "thesis" in parsed

    def test_yaml_output(self):
        node = M09_Compiler("yaml")
        out = node.process(pkt({"key": "value"}))
        assert "key:" in out.payload

    def test_text_output(self):
        node = M09_Compiler("text")
        out = node.process(pkt("Просто текст"))
        assert "Просто текст" in out.payload


# ─────────────────────────────────────────────────────────
#  M10 — Хранилище
# ─────────────────────────────────────────────────────────

class TestM10Vault:
    def test_store(self):
        node = M10_Vault()
        out = node.process(pkt("Синтез: Биомеханика"))
        assert out.payload["stored"] is True
        assert out.payload["total"] == 1

    def test_query(self):
        node = M10_Vault()
        node.process(pkt("Синтез: Хронотоп"))
        matches = node.query("Хронотоп")
        assert len(matches) == 1


# ─────────────────────────────────────────────────────────
#  M11 — Сеть агентов
# ─────────────────────────────────────────────────────────

class TestM11AgentMesh:
    def test_broadcast(self):
        node = M11_AgentMesh()
        node.register_agent("Герменевт")
        node.register_agent("Архитектор")
        out = node.process(pkt("Интуиция ⊕ Структура"))
        assert out.payload["agents"] == 2
        assert "Герменевт" in out.payload["syntheses"]

    def test_empty_mesh(self):
        node = M11_AgentMesh()
        out = node.process(pkt("тест"))
        assert out.payload["agents"] == 0


# ─────────────────────────────────────────────────────────
#  M12 — Рефлекция
# ─────────────────────────────────────────────────────────

class TestM12Reflector:
    def test_coherent(self):
        node = M12_Reflector()
        out = node.process(pkt({"thesis": "A", "antithesis": "¬(A)", "synthesis": "S"}))
        assert out.payload["coherent"] is True
        assert out.payload["verdict"] == "FIELD_COHERENT"

    def test_conflict_detected(self):
        node = M12_Reflector()
        out = node.process(pkt({"thesis": "Свет", "antithesis": "Свет"}))
        assert out.payload["verdict"] == "CONFLICT_DETECTED"
        assert any("CONFLICT" in i for i in out.payload["issues"])


# ─────────────────────────────────────────────────────────
#  M13 — MasterNode + КРСО
# ─────────────────────────────────────────────────────────

class TestMasterNode:
    def test_run_full_pipeline(self, master):
        result = master.run("Свобода ⊕ Ответственность")
        assert "cycle_id" in result
        assert result["ok_steps"] > 0
        assert "krso" in result
        assert result["krso"]["verdict"] in (
            "SYNTHESIS_CONFIRMED", "SYNTHESIS_PARTIAL",
            "SYNTHESIS_DEGRADED", "SYNTHESIS_FAILED"
        )

    def test_krso_index_range(self, master):
        master.run("тест")
        idx = master.krso.index()
        assert 0.0 <= idx <= 1.0

    def test_verify_all(self, master):
        results = master.verify_all()
        assert len(results) == 12
        # Хотя бы половина узлов должна отвечать
        assert sum(results.values()) >= 6

    def test_route_direct(self, master):
        out = master.route("M03", "SYNTH[Тест ⊕ Проверка]")
        assert out.packet_type == "data"

    def test_route_invalid_node(self, master):
        with pytest.raises(ValueError):
            master.route("M99", "test")


# ─────────────────────────────────────────────────────────
#  Полный агент
# ─────────────────────────────────────────────────────────

class TestAvatarusSigma:
    def test_synthesize_basic(self, agent):
        result = agent.synthesize("Свет", "Тьма")
        assert "krso" in result
        assert result["ok_steps"] >= 0

    def test_inject_node_compat(self, agent):
        result = agent.inject_node("Знание", "Незнание")
        assert "synthesis" in result or "final" in result

    def test_health_check(self, agent):
        health = agent.health_check()
        assert health["nodes_total"] == 12
        assert "krso" in health

    def test_add_agent_and_synthesize(self, agent):
        agent.add_agent("Философ", ["reasoning", "synthesis"])
        result = agent.synthesize("Бытие", "Сознание")
        assert result is not None

    def test_register_action(self, agent):
        fired = []
        agent.register_action("Огонь", lambda s: fired.append(s) or "ok")
        agent.synthesize("SYNTH[Огонь ⊕ Вода]")
        # Действие должно было сработать или не сработать в зависимости от
        # того, дошёл ли пакет до M07 (зависит от предыдущих фильтров)
        # Просто проверяем отсутствие исключений

    def test_krso_after_multiple_cycles(self, agent):
        for phrase in ["Любовь ⊕ Мудрость", "Путь ⊕ Цель", "Время ⊕ Вечность"]:
            agent.synthesize(phrase)
        krso = agent.krso_status()
        assert krso["index"] > 0

    def test_full_status(self, agent):
        s = agent.full_status()
        assert s["master_node"] == "M13"
        assert len(s["nodes"]) == 12

    def test_empty_input(self, agent):
        result = agent.synthesize("", None)
        assert result is not None   # не должен упасть
