import random
from datetime import datetime

class FDLTemporalTokenGenerator:
    def __init__(self):
        self.seeds = ["NEDRO", "CYCLE", "SPARK", "BLADE", "PULSE", "ROOT", "RITE", "SOW", "SPROUT", "FRUIT", "DELTA"]
        self.phases = ["∮", "⊕", "⟁", "∷", "≡", "⊂", "→"]
        self.meanings = [
            "Время — это не поток, а узор.",
            "Зерно прорастает в молчании.",
            "Жатва — это форма благодарности.",
            "Каждый цикл — форма вспоминания.",
            "Ритм не в часах, а в смысле.",
            "Момент — не точка, а событие в душе.",
            "Прошлое не уходит — оно зреет.",
            "Истинное «теперь» — всегда раскрытие.",
        ]

    def generate_token(self, index=None):
        if index is None:
            index = random.randint(100, 999)
        code = f"Σ-TEMPORAL-{index:03d}"

        part1 = f"{random.choice(self.phases)}{random.choice(self.seeds)}"
        part2 = f"{random.choice(self.seeds)}"
        part3 = f"{random.choice(self.seeds)}"

        formula = f"{code} ≡ ({part1} → {part2} → {part3}) ⊕ ⟁ΔВРЕМЯ ∷ {{ZOV ⊂ ROOT}} → {{ACTION ⊂ SPROUT}}"
        quote = random.choice(self.meanings)

        publication = f"> {quote}\n{code}: Ритм цикла — не счёт, а зов."
        return {"code": code, "formula": formula, "publication": publication}

    def generate_batch(self, n=3):
        return [self.generate_token(index=i+1) for i in range(n)]


---

📥 Пример генерации:

generator = FDLTemporalTokenGenerator()
tokens = generator.generate_batch(3)

for t in tokens:
    print(t["formula"])
    print(t["publication"])
    print("---")

