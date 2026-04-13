# -*- coding: utf-8 -*-
# Σ-NEREA / sigma_avatarus/avatarus_sigma.py
"""
AvatarusSigma — главная точка входа модуля Σ-Avatarus.

Собирает все 12 меридиональных узлов + Master-Node (M13),
предоставляя единый API для работы с FDL-пайплайном.

Использование:
    from sigma_avatarus import AvatarusSigma

    ava = AvatarusSigma()
    result = ava.synthesize("Свобода", "Ответственность")
    print(result["krso"]["verdict"])   # → SYNTHESIS_CONFIRMED
"""

from meridians.meridian_nodes import (
    M01_Thesis, M02_Antithesis, M03_Lexicon,
    M04_Memory, M05_Resonance, M06_Ethics,
    M07_Executor, M08_Shield, M09_Compiler,
    M10_Vault, M11_AgentMesh, M12_Reflector,
)
from master_node.master_node import MasterNode, KRSO
from core.meridian_base import MeridianPacket


class AvatarusSigma:
    """
    Σ-Avatarus: агент-оболочка с 13-узловой FDL-архитектурой.

    Топология:
      M01 (Тезис) → M02 (Антитезис) → M03 (Лексикон) →
      M04 (Память) → M05 (Резонанс) → M06 (Этика) →
      M07 (Исполнение) → M08 (Защита) → M09 (Компиляция) →
      M10 (Хранилище) → M11 (Сеть агентов) → M12 (Рефлекция)
                              ↑
                         M13 (Master-Node / КРСО)
    """

    VERSION = "1.0.0"

    def __init__(self, name: str = "Σ-Avatarus", compiler_format: str = "json"):
        self.name = name

        # Создание 12 узлов
        self.m01 = M01_Thesis()
        self.m02 = M02_Antithesis()
        self.m03 = M03_Lexicon()
        self.m04 = M04_Memory()
        self.m05 = M05_Resonance()
        self.m06 = M06_Ethics()
        self.m07 = M07_Executor()
        self.m08 = M08_Shield()
        self.m09 = M09_Compiler(output_format=compiler_format)
        self.m10 = M10_Vault()
        self.m11 = M11_AgentMesh()
        self.m12 = M12_Reflector()

        # Упорядоченный пайплайн
        self._pipeline = [
            self.m01, self.m02, self.m03, self.m04,
            self.m05, self.m06, self.m07, self.m08,
            self.m09, self.m10, self.m11, self.m12,
        ]

        # Регистрация соседей (кольцевая верификация)
        for i, node in enumerate(self._pipeline):
            node.register_neighbor(self._pipeline[(i + 1) % 12])
            node.register_neighbor(self._pipeline[(i - 1) % 12])

        # Master-Node
        self.master = MasterNode(self._pipeline)

    # ── Основной API ────────────────────────────────────

    def synthesize(self, thesis: str, antithesis: str = None) -> dict:
        """
        Запускает полный FDL-цикл через все 12 меридианов.
        Если antithesis не передан — M02 сгенерирует его автоматически.
        """
        raw = thesis if antithesis is None else f"{thesis} ⊕ {antithesis}"
        return self.master.run(raw)

    def inject_node(self, thesis: str, antithesis: str) -> dict:
        """
        Совместимый с оригинальным NEREA интерфейс.
        Аналог AvatarusSigma.inject_node() из core/fdl_core.py.
        """
        return self.synthesize(thesis, antithesis)

    def query_memory(self, query: str) -> dict:
        """Прямой запрос к архетипическому хранилищу (M04)."""
        pkt = MeridianPacket(source="API", payload=query)
        return self.m04.process(pkt).payload

    def vault_search(self, keyword: str) -> list[dict]:
        """Поиск по DataVault (M10)."""
        return self.m10.query(keyword)

    def register_action(self, key: str, fn) -> None:
        """Регистрация действия в SynapticExecutor (M07)."""
        self.m07.register(key, fn)

    def add_agent(self, name: str, capabilities: list[str] = None) -> None:
        """Добавление агента в AgentMesh (M11)."""
        self.m11.register_agent(name, capabilities)

    def health_check(self) -> dict:
        """
        Functional Presence: M13 верифицирует все 12 узлов.
        Возвращает карту работоспособности системы.
        """
        node_health = self.master.verify_all()
        krso        = self.master.krso.report()
        return {
            "system":      self.name,
            "version":     self.VERSION,
            "nodes_alive": sum(node_health.values()),
            "nodes_total": 12,
            "nodes":       node_health,
            "krso":        krso,
        }

    def krso_status(self) -> dict:
        """Текущий статус КРСО-индекса."""
        return self.master.krso.report()

    def last_cycle(self) -> dict | None:
        """Результат последнего FDL-цикла."""
        return self.master.last_cycle()

    def full_status(self) -> dict:
        """Полный статус системы через M13."""
        return self.master.status()

    def __repr__(self) -> str:
        return (
            f"<AvatarusSigma name={self.name!r} "
            f"v={self.VERSION} master={self.master}>"
        )
