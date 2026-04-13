# -*- coding: utf-8 -*-
# Σ-NEREA / sigma_avatarus/interfaces/api_server.py
"""
REST API для Σ-Avatarus.

Endpoints:
  POST /synthesize          — запуск FDL-цикла
  POST /inject              — inject_node (совместимость с NEREA)
  GET  /health              — Functional Presence / КРСО
  GET  /krso                — текущий КРСО-индекс
  GET  /status              — полный статус системы
  GET  /cycle/last          — результат последнего цикла
  GET  /vault/search?q=...  — поиск по хранилищу
  POST /agent/register      — регистрация агента в M11
  POST /action/register     — регистрация действия в M07

Запуск:
  uvicorn interfaces.api_server:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from avatarus_sigma import AvatarusSigma


app = FastAPI(
    title="Σ-Avatarus API",
    description="FDL 13-узловой пайплайн · NEREA · Σ-NGOI",
    version="1.0.0",
)

# Глобальный экземпляр агента
_agent = AvatarusSigma("Σ-Avatarus-API")


# ── Схемы запросов ─────────────────────────────────────

class SynthesizeRequest(BaseModel):
    thesis: str
    antithesis: Optional[str] = None


class InjectRequest(BaseModel):
    thesis: str
    antithesis: str


class AgentRequest(BaseModel):
    name: str
    capabilities: Optional[List[str]] = None


# ── Endpoints ──────────────────────────────────────────

@app.get("/")
def root():
    return {
        "system":  "Σ-Avatarus",
        "version": AvatarusSigma.VERSION,
        "status":  "OPERATIONAL",
        "nodes":   12,
        "master":  "M13 / КРСО",
    }


@app.post("/synthesize")
def synthesize(req: SynthesizeRequest):
    """Запуск полного FDL-пайплайна через все 12 меридианов."""
    try:
        result = _agent.synthesize(req.thesis, req.antithesis)
        return {
            "cycle_id":  result["cycle_id"],
            "input":     result["input"],
            "final":     str(result["final"])[:500],
            "ok_steps":  result["ok_steps"],
            "err_steps": result["err_steps"],
            "krso":      result["krso"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/inject")
def inject(req: InjectRequest):
    """Совместимый endpoint (inject_node из оригинального NEREA)."""
    try:
        result = _agent.inject_node(req.thesis, req.antithesis)
        return {
            "synthesis": str(result.get("final", ""))[:300],
            "verdict":   result.get("krso", {}).get("verdict", "UNKNOWN"),
            "krso_index": result.get("krso", {}).get("index", 0),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    """Functional Presence: проверка всех 12 узлов + КРСО."""
    return _agent.health_check()


@app.get("/krso")
def krso():
    """Текущий КРСО-индекс и вердикт."""
    return _agent.krso_status()


@app.get("/status")
def status():
    """Полный статус системы через M13."""
    s = _agent.full_status()
    # Сжимаем для ответа
    return {
        "master_node": s["master_node"],
        "krso":        s["krso"],
        "cycles_run":  s["cycles_run"],
        "total_errors": s["total_errors"],
        "nodes": {
            nid: {"label": nd["label"], "domain": nd["domain_signature"]}
            for nid, nd in s["nodes"].items()
        },
    }


@app.get("/cycle/last")
def last_cycle():
    """Результат последнего FDL-цикла."""
    cycle = _agent.last_cycle()
    if not cycle:
        return {"message": "Нет завершённых циклов"}
    return {
        "cycle_id":  cycle["cycle_id"],
        "input":     cycle["input"],
        "krso":      cycle["krso"],
        "ok_steps":  cycle["ok_steps"],
        "err_steps": cycle["err_steps"],
        "elapsed_s": cycle["elapsed_s"],
    }


@app.get("/vault/search")
def vault_search(q: str = ""):
    """Поиск по DataVault (M10)."""
    if not q:
        raise HTTPException(status_code=400, detail="Параметр q обязателен")
    results = _agent.vault_search(q)
    return {"query": q, "count": len(results), "entries": results[:20]}


@app.post("/agent/register")
def register_agent(req: AgentRequest):
    """Регистрация агента в AgentMesh (M11)."""
    _agent.add_agent(req.name, req.capabilities)
    return {"registered": req.name, "capabilities": req.capabilities}
