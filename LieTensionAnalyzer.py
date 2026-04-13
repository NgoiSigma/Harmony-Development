# Σ-FDL::ΔΨ-Monitoring Module — Сейсмограф смыслов
# Модель "напряжения лжи" в социальной системе управления

from typing import List, Dict
import numpy as np

class LieTensionAnalyzer:
    def __init__(self):
        self.official_narratives: List[str] = []
        self.detected_events: List[Dict] = []
        self.contradictions: List[str] = []

    def add_narrative(self, statement: str):
        self.official_narratives.append(statement)

    def register_event(self, event: Dict):
        # event format: {'region': str, 'type': str, 'intensity': float, 'description': str}
        self.detected_events.append(event)

    def detect_contradiction(self, contradiction: str):
        self.contradictions.append(contradiction)

    def compute_tension_index(self) -> float:
        # Tension Index (TI): proxy for "pressure of falsehood"
        N = len(self.official_narratives)
        C = len(self.contradictions)
        E = sum([e['intensity'] for e in self.detected_events])
        
        if N == 0:
            return 0.0

        TI = (C * 1.5 + E) / N  # weight contradictions higher than events
        return round(TI, 3)

    def identify_hotspots(self) -> Dict[str, float]:
        region_scores = {}
        for event in self.detected_events:
            region = event['region']
            intensity = event['intensity']
            region_scores[region] = region_scores.get(region, 0) + intensity

        return dict(sorted(region_scores.items(), key=lambda item: item[1], reverse=True))

    def status_report(self) -> Dict:
        return {
            "Tension Index": self.compute_tension_index(),
            "Top Hotspots": self.identify_hotspots(),
            "Contradictions": self.contradictions[-5:]
        }

# Пример использования
monitor = LieTensionAnalyzer()
monitor.add_narrative("Конфликт будет решён дипломатически без ущерба для населения")
monitor.register_event({"region": "Юг Украины", "type": "военные действия", "intensity": 8.5, "description": "Обострение боёв"})
monitor.detect_contradiction("Отчёты независимых СМИ противоречат заявлениям о деэскалации")
monitor.register_event({"region": "Израиль-Газа", "type": "удар по инфраструктуре", "intensity": 7.2, "description": "Атака на жилой сектор"})

# Вывод результатов
print(monitor.status_report())
