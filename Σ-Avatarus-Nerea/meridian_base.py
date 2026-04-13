# -*- coding: utf-8 -*-
# Σ-NEREA / sigma_avatarus/core/meridian_base.py
"""
Базовый класс для всех 12 меридианных узлов системы Σ-Avatarus.

Каждый узел реализует:
  - process(payload)  → обрабатывает входящий пакет данных
  - verify(result)    → верифицирует результат соседнего узла
  - sign(data)        → подписывает выходные данные узла

Топология: 12 периферийных + 1 центральный (Master-Node / 13-й канал).
"""

from __future__ import annotations
import hashlib
import time
import json
from abc import ABC, abstractmethod
from typing import Any, Optional


# ─────────────────────────────────────────────────────────
#  Типы пакетов
# ─────────────────────────────────────────────────────────

class MeridianPacket:
    """Стандартный пакет межузлового обмена."""

    def __init__(
        self,
        source: str,
        payload: Any,
        packet_type: str = "data",
        metadata: Optional[dict] = None,
    ):
        self.source      = source
        self.payload     = payload
        self.packet_type = packet_type          # data | verify | ack | error
        self.metadata    = metadata or {}
        self.timestamp   = time.time()
        self.signature   = self._sign()

    def _sign(self) -> str:
        raw = f"{self.source}|{self.payload}|{self.timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def to_dict(self) -> dict:
        return {
            "source":      self.source,
            "payload":     self.payload,
            "type":        self.packet_type,
            "metadata":    self.metadata,
            "timestamp":   self.timestamp,
            "signature":   self.signature,
        }

    def is_valid(self) -> bool:
        """Быстрая проверка целостности пакета."""
        return self.signature == self._sign()

    def __repr__(self) -> str:
        return f"<Packet from={self.source} type={self.packet_type} sig={self.signature}>"


# ─────────────────────────────────────────────────────────
#  Базовый класс меридиана
# ─────────────────────────────────────────────────────────

class MeridianNode(ABC):
    """
    Абстрактный базовый класс для всех 12 меридианных узлов.

    Обязательные методы для реализации:
      - process(packet)  → MeridianPacket
      - domain_signature → str  (уникальная сигнатура домена)
    """

    def __init__(self, node_id: str, label: str):
        self.node_id   = node_id     # "M01" … "M12"
        self.label     = label       # человекочитаемое название
        self._log: list[dict] = []
        self._neighbors: list["MeridianNode"] = []

    # ── обязательные ────────────────────────────────────

    @property
    @abstractmethod
    def domain_signature(self) -> str:
        """Уникальная сигнатура функционального домена узла."""

    @abstractmethod
    def process(self, packet: MeridianPacket) -> MeridianPacket:
        """Обработка входящего пакета, возврат исходящего."""

    # ── верификация (по умолчанию — хэш-проверка) ───────

    def verify(self, packet: MeridianPacket) -> bool:
        """
        Верификация результата соседнего узла.
        Режим «активного присутствия»: каждый узел проверяет соседа.
        Переопределяй для доменной логики.
        """
        if not packet.is_valid():
            self._emit_log("VERIFY_FAIL", f"Corrupted packet from {packet.source}")
            return False
        if packet.payload is None:
            self._emit_log("VERIFY_FAIL", f"Null payload from {packet.source}")
            return False
        self._emit_log("VERIFY_OK", f"Packet from {packet.source} verified")
        return True

    # ── регистрация соседей ───────────────────────────────

    def register_neighbor(self, node: "MeridianNode") -> None:
        if node not in self._neighbors:
            self._neighbors.append(node)

    # ── логирование ───────────────────────────────────────

    def _emit_log(self, event: str, detail: str = "") -> None:
        entry = {
            "node":   self.node_id,
            "event":  event,
            "detail": detail,
            "ts":     time.time(),
        }
        self._log.append(entry)

    def get_log(self) -> list[dict]:
        return list(self._log)

    def status(self) -> dict:
        return {
            "node_id":          self.node_id,
            "label":            self.label,
            "domain_signature": self.domain_signature,
            "log_entries":      len(self._log),
            "neighbors":        [n.node_id for n in self._neighbors],
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.node_id} label={self.label}>"
