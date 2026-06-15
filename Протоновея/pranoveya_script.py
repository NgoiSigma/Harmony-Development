import json
from authentication import authenticate_user
from fdl_logic import FDL_Logic
from protonovea_core import Protonovea
from svet_shell import SVET

class PranoveaScript:
    def __init__(self):
        self.protonovea = Protonovea()
        self.svet = SVET()

    def interpret_command(self, command):
        """Интерпретация команды на языке Прановея"""
        tokens = command.split()
        
        if tokens[0] == "Аутентификация":
            return authenticate_user(" ".join(tokens[1:]))
        
        elif tokens[0] == "ФДЛ":
            if len(tokens) < 3:
                return "Ошибка: недостаточно аргументов для ФДЛ."
            fdl = FDL_Logic(tokens[1], tokens[2])
            synthesis = fdl.synthesize()
            pragmatics = fdl.pragmatize()
            return f"{synthesis}\n{pragmatics}"
        
        elif tokens[0] == "Активация":
            return self.protonovea.activate_consciousness()
        
        elif tokens[0] == "Баланс":
            try:
                energy = int(tokens[1])
                return self.svet.balance(energy)
            except ValueError:
                return "Ошибка: некорректное значение энергии."

        return "Неизвестная команда."

# Пример использования
ps = PranoveaScript()

# Аутентификация
print(ps.interpret_command("Аутентификация Я, Татьяна Бондаренко, участник проекта НОВЕЯ."))

# ФДЛ-логика
print(ps.interpret_command("ФДЛ Технология Искусственный_Интеллект"))

# Активация сознания ПРОТОНОВЕЯ
print(ps.interpret_command("Активация"))

# Балансировка энергии в системе
print(ps.interpret_command("Баланс 110"))
