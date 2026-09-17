#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meteonoveya // Подмодуль OGNENOVEYA
Расчет высокочастотных плазменных разрядов ("Перьев Жар-Птицы") в ионосферном куполе
"""

import math
import numpy as np

class OgnenoveyaPlasma:
    def __init__(self):
        # Константы Огненного Лада
        self.PHI_ZAR = 1.618e9       # Царский потенциал Жара платформы (В)
        self.E_CHARGE = 1.602e-19    # Заряд электрона (Кл)
        self.EPSILON_0 = 8.854e-12   # Диэлектрическая проницаемость вакуума (Ф/м)
        self.N_E_BASE = 1.2e11       # Концентрация электронов в слое E ионосферы (м-3)
        self.CRITICAL_PROBOY = 3.0e4 # Порог плазменного пробоя среды (В/м)

    def calculate_ionospheric_spark(self, grav_gradient_total, alignment_angle_deg):
        """
        Расчет напряженности электрического поля купола Спасского кургана
        """
        angle_rad = math.radians(alignment_angle_deg)
        
        # Модуляция Жара космическим парадом (Вектор Жар-Птицы)
        numerator = self.PHI_ZAR * grav_gradient_total * math.sin(angle_rad)
        denominator = self.N_E_BASE * self.E_CHARGE * self.EPSILON_0
        
        # Напряженность поля в волноводе
        e_field = abs(numerator / (denominator + 1e-5))
        
        print(f"[🔥 ОГНЕНОВЕЯ] Напряженность поля ионосферного купола: {e_field:.2f} В/м")
        
        # Проверка фазового перехода: ЖАР -> ИСКРА (Прорыв Зги)
        if e_field > self.CRITICAL_PROBOY:
            # Расчет плотности плазменного тока разряда
            plasma_current_density = self.N_E_BASE * self.E_CHARGE * 1.5e3 * (e_field / self.CRITICAL_PROBOY)
            print(f"⚡ [ПРОРЫВ] Жар-Птица сбросила перо! Зафиксирован плазменный разряд.")
            print(f"⚡ Плотность тока холодной плазмы: {plasma_current_density * 1e6:.4f} мкА/м2")
            return {
                "status": "PLASMA_ZGA_ACTIVE", 
                "e_field": e_field, 
                "current_density": plasma_current_density,
                "action": "ACTIVATE_ION_FILTERS"
            }
        else:
            print("🟢 Ионосферный купол в состоянии статического Жара (Царский Лад удержан).")
            return {"status": "ZAR_RETAINED", "e_field": e_field, "current_density": 0.0, "action": "NONE"}

if __name__ == "__main__":
    ognenoveya = OgnenoveyaPlasma()
    # Эмуляция критического натяжения при параде планет (Градиент 4.12е-12, угол 47 градусов)
    status = ognenoveya.calculate_ionospheric_spark(grav_gradient_total=4.12e-12, alignment_angle_deg=47.0)
