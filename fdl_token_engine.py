# fdl_token_engine.py

import hashlib
import datetime

class FDLTokenEngine:
    def __init__(self):
        self.prefix = "FDL"
        self.version = "N7Δ+"

    def generate_token(self, topic, style="core"):
        """Генерирует токен по теме и стилю"""
        base = f"{self.prefix}::{self.version}::{style.upper()}::{topic.strip().replace(' ', '_')}"
        digest = hashlib.md5(base.encode()).hexdigest()[:6].upper()
        return f"{base}::{digest}"

    def explain_token(self, token):
        """Разъясняет состав токена"""
        parts = token.split("::")
        return {
            "format": "FDL::<версия>::<стиль>::<тема>::<хеш>",
            "style": parts[2],
            "topic": parts[3].replace("_", " "),
            "checksum": parts[-1]
        }

    def log_token(self, token):
        """Формирует лог токенизации"""
        time = datetime.datetime.utcnow().isoformat()
        return f"[{time}] TOKEN: {token}"

# Пример использования
if __name__ == "__main__":
    engine = FDLTokenEngine()
    tok = engine.generate_token("громада и справедливость")
    print(tok)
    print(engine.explain_token(tok))
