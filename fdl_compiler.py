""" FDL Compiler — преобразователь FDL-языка в исполняемую логическую структуру (AST + runtime)
Фаза: интерпретация резонансных блоков, проверка обратимости, инициация откликов
Дополнение: внедрение семантического антидота, экспорта в различные формы, включая токены, действия, код
"""

import json
from typing import List, Dict

class FDLBlock:
    def __init__(self, block_id: str, structure: Dict):
        self.block_id = block_id
        self.structure = structure

    def __repr__(self):
        return f"FDLBlock<{self.block_id}>"

    def is_resonant(self) -> bool:
        # Резонансная проверка — базовая логика соответствия полей
        return all(key in self.structure for key in ["замысел", "форма", "поток"])

    def export(self, mode="token") -> Dict:
        # Экспорт в различные формы: токен, действие, код
        if mode == "token":
            return {
                "FDL-TOKEN": {
                    "ZAMYSEL": self.structure.get("замысел"),
                    "FORMA": self.structure.get("форма"),
                    "POTOK": self.structure.get("поток")
                }
            }
        elif mode == "code":
            return {
                "code_snippet": f"# FDL код для: {self.structure.get('замысел')}\nprint(\"{self.structure.get('поток')}\")"
            }
        elif mode == "praxis":
            return {
                "action": f"initiate_{self.structure.get('форма')}_flow"
            }
        else:
            return self.structure

class FDLCompiler:
    def __init__(self):
        self.blocks: List[FDLBlock] = []
        self.errors: List[str] = []

    def parse(self, source: str):
        current = {}
        block_id = "block_0"
        for line in source.strip().splitlines():
            if ':' in line:
                key, val = line.strip().split(':', 1)
                current[key.strip()] = val.strip()
        self.blocks.append(FDLBlock(block_id, current))

    def validate(self):
        for block in self.blocks:
            required_fields = ["замысел", "форма", "поток"]
            for field in required_fields:
                if field not in block.structure:
                    self.errors.append(f"{block.block_id}: отсутствует поле '{field}'")

    def compile(self, export_mode="token"):
        if self.errors:
            return None
        return json.dumps([b.export(mode=export_mode) for b in self.blocks], ensure_ascii=False, indent=2)

    def report(self):
        if self.errors:
            return {"status": "ошибки", "errors": self.errors}
        return {"status": "готово", "blocks": len(self.blocks)}

# Пример использования
if __name__ == '__main__':
    source = """
    замысел: протестировать систему
    форма: логический анализ
    поток: от агента к ядру
    сигнал: обратная связь
    отклик: лог печати
    контур: проверка синтаксиса
    """

    compiler = FDLCompiler()
    compiler.parse(source)
    compiler.validate()
    result = compiler.compile(export_mode="token")
    print(result if result else compiler.report())