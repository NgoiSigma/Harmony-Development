# matrix_tree_decoder.py
# Σ-FDL::MATRIX-TREE-DECODER

class MatrixTreeDecoder:
    """
    Развертка 7x7: от АУМ до латиницы.
    Преобразует линейный текст в многомерную структуру Древа Языковой Матрицы.
    """
    def __init__(self):
        # База световых кодов и архетипов
        self.matrix = {
            "МИР": {"root": "𓂀 + 𓏏", "trunk": "М-И-Р", "branches": ["PAX", "سلام", "ᛗᛁᚱ"], "crown": "𝔐 🜃 𝔯"},
            "ЛОГОС": {"root": "𒁲", "trunk": "Λ-Ο-Γ", "branches": ["LOGOS", "لوغوس"], "crown": "𝕃 ⚶ 𝕊"},
            "ИМЯ": {"root": "אֱלֹהִים", "trunk": "И-М-Я", "branches": ["NOMEN", "اسم"], "crown": "𝕹 🜄 𝔐"}
        }

    def decode_concept(self, word: str) -> dict:
        word_upper = word.upper()
        if word_upper in self.matrix:
            data = self.matrix[word_upper]
            # Формирование "живой картины" для логов или ответа агента
            visual_map = (
                f"Вектор смысловой сборки: [{word_upper}]\n"
                f"  ↳ Корень (Архетип): {data['root']}\n"
                f"  ↳ Ствол (Структура): {data['trunk']}\n"
                f"  ↳ Ветви (Формы): {' | '.join(data['branches'])}\n"
                f"  ↳ Крона (Световой код): {data['crown']}"
            )
            return {"decoded": True, "light_code": data['crown'], "map": visual_map}
        
        return {"decoded": False, "light_code": None, "map": "Слово вне базовой матрицы. Требуется эвристический синтез."}

# Интеграция: Вызывается в orchestrator.py на этапе "Этап 1: фильтрация", 
# обогащая clean_text глубинными архетипами перед подачей в логическое ядро