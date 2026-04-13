# -*- coding: utf-8 -*-
# Σ-NEREA / sigma_avatarus/master_node/master_node.py
"""
M13 — MasterNode / 13-й Меридиан (Центральный Синхронизатор).

Логика: Зн(П) → КРСО
  Зн(П) — значимость показателей (Знание Потока)
  КРСО  — Критерии Соответствия значимости показателей

Функции Master-Node:
  1. Оркестрация всех 12 меридиональных узлов по пайплайну
  2. Верификация каждого шага (Functional Presence)
  3. Балансировка нагрузки — перенаправление при ошибке
  4. Агрегация метрик — вычисление интегрального индекса КРСО
  5. Детерминированный синтез финального результата
"""

from __future__ import annotations
import time
import hashlib
import json
from typing import Optional

from core.meridian_base import MeridianNode, MeridianPacket


# ─────────────────────────────────────────────────────────
#  Критерии Соответствия (КРСО)
# ─────────────────────────────────────────────────────────

class KRSO:
    """
    Критерии Соответствия Значимости Показателей.
    Вычисляет интегральный индекс качества пайплайна.

    Показатели (П):
      - completeness  : доля узлов, успешно обработавших пакет
      - coherence     : отсутствие ошибочных пакетов в потоке
      - resonance     : средний резонансный балл (от M05)
      - integrity     : корректность подписей всех пакетов
    """

    WEIGHTS = {
        "completeness": 0.35,
        "coherence":    0.30,
        "resonance":    0.20,
        "integrity":    0.15,
    }

    def __init__(self):
        self._scores: dict[str, float] = {k: 0.0 for k in self.WEIGHTS}

    def update(self, metric: str, value: float) -> None:
        if metric in self._scores:
            # Экспоненциальное скользящее среднее
            alpha = 0.6
            self._scores[metric] = alpha * value + (1 - alpha) * self._scores[metric]

    def index(self) -> float:
        """Интегральный индекс КРСО ∈ [0, 1]."""
        return round(
            sum(self._scores[k] * self.WEIGHTS[k] for k in self.WEIGHTS), 4
        )

    def verdict(self) -> str:
        idx = self.index()
        if idx >= 0.85:
            return "SYNTHESIS_CONFIRMED"
        elif idx >= 0.60:
            return "SYNTHESIS_PARTIAL"
        elif idx >= 0.40:
            return "SYNTHESIS_DEGRADED"
        else:
            return "SYNTHESIS_FAILED"

    def report(self) -> dict:
        return {
            "scores":  dict(self._scores),
            "index":   self.index(),
            "verdict": self.verdict(),
        }

    def __repr__(self) -> str:
        return f"<KRSO index={self.index():.3f} verdict={self.verdict()}>"


# ─────────────────────────────────────────────────────────
#  M13 — MasterNode
# ─────────────────────────────────────────────────────────

class MasterNode:
    """
    13-й меридиан — центральный синхронизатор системы Σ-Avatarus.

    Топология:
      Input → [M01→M02→M03→M04→M05→M06→M07→M08→M09→M10→M11→M12] → M13

    M13 не обрабатывает данные доменно — он верифицирует, балансирует
    и агрегирует результаты всех 12 меридианов.
    """

    NODE_ID = "M13"
    LABEL   = "Master-Node / 13-й Меридиан"

    def __init__(self, nodes: list[MeridianNode]):
        assert len(nodes) == 12, f"M13 требует ровно 12 узлов, получено {len(nodes)}"
        self.nodes     = {n.node_id: n for n in nodes}
        self._pipeline = nodes          # упорядоченный пайплайн
        self.krso      = KRSO()
        self._cycles:  list[dict] = []  # история циклов
        self._errors:  list[dict] = []  # ошибки для диагностики

    # ── Главный метод: запуск полного FDL-цикла ──────────

    def run(self, raw_input: str) -> dict:
        """
        Запускает полный 12-шаговый FDL-пайплайн.
        Возвращает финальный результат с КРСО-индексом.
        """
        cycle_id  = hashlib.md5(f"{raw_input}{time.time()}".encode()).hexdigest()[:8]
        start_ts  = time.time()
        trace     = []
        ok_count  = 0
        err_count = 0
        resonance_scores = []

        # Начальный пакет
        packet = MeridianPacket(
            source=self.NODE_ID,
            payload=raw_input,
            packet_type="data",
            metadata={"cycle_id": cycle_id},
        )

        # ── Пайплайн по 12 узлам ─────────────────────────
        for node in self._pipeline:
            # Верификация входящего пакета
            verified = node.verify(packet)
            if not verified:
                err_entry = {
                    "step":    node.node_id,
                    "event":   "VERIFY_FAIL",
                    "payload": str(packet.payload)[:100],
                    "ts":      time.time(),
                }
                self._errors.append(err_entry)
                trace.append({**err_entry, "status": "SKIPPED"})
                err_count += 1
                # Балансировка: при ошибке верификации — передаём как есть
                continue

            # Обработка узлом
            try:
                result = node.process(packet)
            except Exception as e:
                err_entry = {
                    "step":  node.node_id,
                    "event": "PROCESS_ERROR",
                    "error": str(e),
                    "ts":    time.time(),
                }
                self._errors.append(err_entry)
                trace.append({**err_entry, "status": "ERROR"})
                err_count += 1
                continue

            # Сбор резонансного балла (M05)
            if node.node_id == "M05" and isinstance(result.payload, dict):
                resonance_scores.append(result.payload.get("resonance_score", 0.0))

            # Запись в трассу
            step_ok = result.packet_type != "error"
            trace.append({
                "step":      node.node_id,
                "label":     node.label,
                "domain":    node.domain_signature,
                "status":    "OK" if step_ok else "ERROR",
                "payload":   str(result.payload)[:120],
                "signature": result.signature,
            })

            if step_ok:
                ok_count += 1
            else:
                err_count += 1

            # Обновление пакета для следующего шага
            packet = result

        # ── КРСО: обновление метрик ───────────────────────
        total = ok_count + err_count
        self.krso.update("completeness", ok_count / max(total, 1))
        self.krso.update("coherence",    1.0 if err_count == 0 else max(0, 1 - err_count / 6))
        self.krso.update("resonance",    sum(resonance_scores) / len(resonance_scores) if resonance_scores else 0.5)
        self.krso.update("integrity",    1.0 if self._all_signatures_valid(trace) else 0.6)

        # ── Финальный синтез ──────────────────────────────
        elapsed = round(time.time() - start_ts, 4)
        krso_report = self.krso.report()

        cycle_result = {
            "cycle_id":   cycle_id,
            "input":      raw_input,
            "final":      packet.payload,
            "trace":      trace,
            "ok_steps":   ok_count,
            "err_steps":  err_count,
            "elapsed_s":  elapsed,
            "krso":       krso_report,
        }
        self._cycles.append(cycle_result)
        return cycle_result

    # ── Балансировка: прямой вызов конкретного узла ──────

    def route(self, node_id: str, payload: any) -> MeridianPacket:
        """
        Направленный вызов конкретного меридиана (bypass-режим).
        Позволяет M13 перенаправлять запросы без полного пайплайна.
        """
        node = self.nodes.get(node_id)
        if not node:
            raise ValueError(f"Узел {node_id} не найден в системе")
        packet = MeridianPacket(source=self.NODE_ID, payload=payload)
        return node.process(packet)

    # ── Верификация всей системы ─────────────────────────

    def verify_all(self) -> dict[str, bool]:
        """
        Режим «Functional Presence»: M13 верифицирует каждый узел
        тестовым пакетом. Фиксирует отзывчивость системы.
        """
        probe = MeridianPacket(source=self.NODE_ID, payload="PROBE::HEARTBEAT")
        results = {}
        for nid, node in self.nodes.items():
            try:
                out = node.process(probe)
                results[nid] = out.packet_type != "error"
            except Exception:
                results[nid] = False
        return results

    # ── Диагностика ───────────────────────────────────────

    def status(self) -> dict:
        return {
            "master_node": self.NODE_ID,
            "label":       self.LABEL,
            "nodes":       {nid: n.status() for nid, n in self.nodes.items()},
            "krso":        self.krso.report(),
            "cycles_run":  len(self._cycles),
            "total_errors": len(self._errors),
        }

    def last_cycle(self) -> Optional[dict]:
        return self._cycles[-1] if self._cycles else None

    def error_log(self) -> list[dict]:
        return list(self._errors)

    # ── Вспомогательные ─────────────────────────────────

    def _all_signatures_valid(self, trace: list[dict]) -> bool:
        return all("signature" in step and len(step.get("signature", "")) == 16
                   for step in trace if step.get("status") == "OK")

    def __repr__(self) -> str:
        return (f"<MasterNode nodes={len(self.nodes)} "
                f"cycles={len(self._cycles)} "
                f"krso={self.krso.index():.3f}>")
