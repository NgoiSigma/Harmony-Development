# -*- coding: utf-8 -*-
# Σ-NEREA / sigma_avatarus/config/settings.py
"""
Конфигурация системы Σ-Avatarus.
Централизованные параметры для всех 13 узлов.
"""

# ─── Идентификация системы ───────────────────────────
SYSTEM_NAME    = "Σ-Avatarus"
SYSTEM_VERSION = "1.0.0"
PROTOCOL       = "NEBI-ULA"
RESONANCE_FREQ = 432.0

# ─── API ─────────────────────────────────────────────
API_HOST = "0.0.0.0"
API_PORT = 8000

# ─── Пороги КРСО ─────────────────────────────────────
KRSO_CONFIRMED = 0.85   # SYNTHESIS_CONFIRMED
KRSO_PARTIAL   = 0.60   # SYNTHESIS_PARTIAL
KRSO_DEGRADED  = 0.40   # SYNTHESIS_DEGRADED
# ниже — SYNTHESIS_FAILED

# ─── Параметры КРСО ──────────────────────────────────
KRSO_WEIGHTS = {
    "completeness": 0.35,
    "coherence":    0.30,
    "resonance":    0.20,
    "integrity":    0.15,
}
KRSO_EMA_ALPHA = 0.6    # Экспоненциальное скользящее среднее

# ─── Узлы и топология ───────────────────────────────
NODE_COUNT         = 12   # периферийных
MASTER_NODE_ID     = "M13"
PIPELINE_ORDER     = [
    "M01","M02","M03","M04","M05","M06",
    "M07","M08","M09","M10","M11","M12",
]

# ─── Лимиты ──────────────────────────────────────────
MAX_PAYLOAD_LEN   = 4096    # символов
MAX_TRACE_ENTRIES = 1000    # записей истории
SIGNATURE_LEN     = 16      # символов hex

# ─── Путь к данным ───────────────────────────────────
VAULT_FILE        = "data/avatarus_vault.json"
LOG_FILE          = "logs/avatarus.log"
