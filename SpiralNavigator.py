class SpiralNavigator:
    def __init__(self, structure):
        self.structure = structure

    def describe(self, level):
        return self.structure.get(level, {"Ошибка": "Уровень не найден."})

    def next_level(self, level):
        info = self.describe(level)
        return info.get("Следующий", None)

    def previous_level(self, level):
        info = self.describe(level)
        return info.get("Предыдущий", None)

    def path_from_to(self, start, end):
        path = []
        current = start
        while current and current != end:
            path.append(current)
            current = self.next_level(current)
        if current == end:
            path.append(end)
            return path
        return None  # если путь не найден

# Инициализация навигатора
navigator = SpiralNavigator(spiral_structure)

# Пример: маршрут от Purple до Green
navigator.path_from_to("Purple", "Green")
________________________________________________________________
Готово. Я создал функциональный модуль SpiralNavigator, который теперь:
✅ Возвращает описание любого уровня ✅ Показывает следующий и предыдущий ✅ Строит путь между уровнями — как ты видел: например, от Purple до Green:
Purple → Red → Blue → Orange → Green
