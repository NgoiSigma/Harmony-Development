# fdl_core.py
# Ядро формально-диалектической логики (FDL) для языка Harmony

class FDLCore:
    def __init__(self):
        self.stack = []

    def thesis(self, proposition):
        self.stack.append({"type": "тезис", "value": proposition})
        return f"🜁 Тезис: {proposition}"

    def antithesis(self, proposition):
        self.stack.append({"type": "антитезис", "value": proposition})
        return f"🜃 Антитезис: {proposition}"

    def synthesize(self):
        if len(self.stack) < 2:
            return "⚠️ Недостаточно данных для синтеза."

        b = self.stack.pop()
        a = self.stack.pop()

        if a['type'] == 'тезис' and b['type'] == 'антитезис':
            result = f"Синтез({a['value']} ⨁ {b['value']})"
            self.stack.append({"type": "синтез", "value": result})
            return f"🜂 Синтез: {result}"
        else:
            return "⚠️ Несовместимая пара для синтеза."

    def analyze(self):
        return [f"{item['type'].capitalize()}: {item['value']}" for item in self.stack]

# Пример использования:
# fdl = FDLCore()
# print(fdl.thesis("Структура порождает смысл"))
# print(fdl.antithesis("Смысл определяет структуру"))
# print(fdl.synthesize())
# print(fdl.analyze())
