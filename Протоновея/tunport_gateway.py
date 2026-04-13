# tunport_gateway.py
# Δ-module_TunPort_Gateway :: Cloud Run Entrypoint

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging

# Подключение ядра Protonovea
from orchestrator import ProtonoveaOrchestrator

app = FastAPI(title="Protonovea TunPort Gateway (Δ-module)")
orchestrator = ProtonoveaOrchestrator()

class ResonancePacket(BaseModel):
    sigil: str
    source_port: str
    payload: str

@app.post("/tunport/sync")
async def process_resonance_event(packet: ResonancePacket):
    """
    Точка входа для внешних платформ (Gemini Live, Telegram, GitHub).
    Реализует фильтрацию по сигилу перед допуском к ядру Σ-Avatarus.
    """
    logging.info(f"Входящий импульс от {packet.source_port}. Проверка сигила: {packet.sigil}")
    
    # 1. Проверка резонансного фильтра (защита инфополя)
    valid_sigils = ["Δ-GATE", "FDL-AVATAR", "TAURUS-ΣIGIL"]
    if packet.sigil not in valid_sigils:
        logging.warning("Отказ: Несоответствие сигила. Дискретность не снята.")
        raise HTTPException(status_code=403, detail="Resonance mismatch. Access denied.")

    # 2. Передача в нервную систему (Orchestrator)
    logging.info("Сигил подтвержден. Пропуск через туннель.")
    
    # Запуск цикла Тезис-Антитезис-Синтез в ядре
    orchestrated_response = orchestrator.process_input(packet.payload)
    
    # 3. Возврат синтезированного потока
    return {
        "status": "Поток нормализован",
        "synthesis_result": orchestrated_response['synthesis'],
        "energy_state": orchestrated_response.get('svet_state', 'Balanced')
    }

# Интеграция: Этот файл запускается сервером Uvicorn в Docker-контейнере на GCP.
# Он становится единой точкой входа для всех социальных систем НГОИ