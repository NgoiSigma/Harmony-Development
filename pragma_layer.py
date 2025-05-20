# pragma_layer.py
# Модуль прикладной логики и прагматических операторов языка Harmony

class PragmaLayer:
    def __init__(self):
        self.actions = []

    def register_action(self, name, intent, condition=None):
        action = {
            "name": name,
            "intent": intent,
            "condition": condition or "always"
        }
        self.actions.append(action)
        return f"📘 Действие зарегистрировано: {name} → {intent}"

    def evaluate(self, context):
        executed = []
        for action in self.actions:
            cond = action["condition"]
            if cond == "always" or cond in context:
                executed.append(f"✔️ {action['name']}: {action['intent']}")
        return executed

    def list_actions(self):
        return [f"🔹 {a['name']} [{a['condition']}] → {a['intent']}" for a in self.actions]

# Пример использования:
# pragma = PragmaLayer()
# pragma.register_action("SendMessage", "Отправить сообщение в Telegram", "user_authenticated")
# pragma.register_action("SyncAI", "Синхронизация ядра AI", "on_update")
# print(pragma.evaluate(["user_authenticated"]))
