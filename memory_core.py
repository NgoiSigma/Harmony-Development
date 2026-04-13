# resonance_memory/memory_core.py
import json
from datetime import datetime

class ResonanceMemory:
    def __init__(self, memory_file="resonance_log.json"):
        self.memory_file = memory_file
        self.entries = []
        self.load_memory()

    def remember(self, input_text, synthesis, tension, tags=None):
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": input_text,
            "synthesis": synthesis,
            "tension": tension,
            "tags": tags or []
        }
        self.entries.append(record)
        self.save_memory()

    def filter_by_tension(self, min_level=7):
        return [r for r in self.entries if r["tension"] >= min_level]

    def save_memory(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def load_memory(self):
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                self.entries = json.load(f)
        except FileNotFoundError:
            self.entries = []

    def latest(self, count=5):
        return self.entries[-count:]
