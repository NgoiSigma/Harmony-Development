#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meteonoveya: Автоматический генератор ежесуточных отчетов для СУБД TimescaleDB.
Расчет энергетического гомеостаза, отклонений частоты Шумана и окупаемости переброшенной мощности.
"""

import math
import psycopg2
from datetime import datetime, timedelta, timezone

class ElectrotransReportGenerator:
    def __init__(self, db_url="postgres://postgres:noveya_secret@localhost:5432/meteonoveya_db"):
        self.db_url = db_url
        # Физические и маркшейдерские константы Спасского холма (НГОИ)
        self.F0 = 7.83                   # Базовая частота Шумана (альфа-оптимум, Гц)
        self.V_SHELL = 125000.0          # Объем известнякового лабиринта-Фагота (м3)
        self.RHO_SHIELD = 2700.0         # Плотность гранитов Украинского щита (кг/м3)
        self.T_PHASE = 2.4               # Длительность фазы гидроудара по Жуковскому (сек)
        
        # Финансово-энергетический учет КП "Николаевэлектротранс"
        self.energy_tariff_uah = 7.50    # Тариф на электроэнергию (грн за кВт*ч)

    def generate_daily_report(self):
        """Агрегационный запрос к гипертаблице за прошедшие 24 часа с расчетом МГД-параметров"""
        now = datetime.now(timezone.utc)
        yesterday = now - timedelta(days=1)

        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()

        # Запрос рассчитывает: 
        # 1. Общее число прорывов Зги (sparks)
        # 2. Среднюю мощность кинетического импульса гидроудара
        # 3. Суммарную утилизированную энергию на основе шага сброса фазы гидроудара T_phase (2.4 сек)
        # 4. Среднее отклонение частоты резонатора и интегральное волновое давление вакуума
        query = """
            SELECT 
                COUNT(*) as total_sparks,
                COALESCE(AVG(impulse_power_mw), 0) as avg_impulse_mw,
                COALESCE(SUM(grid_transfer_load * (%s / 3600.0)), 0) as total_energy_mwh,
                COALESCE(AVG(schumann_freq_measured), %s) as avg_schumann_freq,
                COALESCE(MAX(ABS(schumann_freq_measured - %s)), 0) as max_freq_deviation,
                COALESCE(AVG(tectonic_pressure_mpa), 0) as avg_pressure_mpa
            FROM zinc_spark_events
            WHERE time >= %s AND time < %s;
        """
        
        cursor.execute(query, (self.T_PHASE, self.F0, self.F0, yesterday, now))
        (total_sparks, avg_impulse_mw, total_energy_mwh, 
         avg_schumann_freq, max_freq_deviation, avg_pressure_mpa) = cursor.fetchone()

        # Перевод МВт*ч в кВт*ч для финансовой службы подстанции
        total_energy_kwh = total_energy_mwh * 1000.0
        economic_effect_uah = total_energy_kwh * self.energy_tariff_uah

        # Формирование текстовой матрицы рапорта волнового лада
        report_text = f"════════════════════════════════════════════════════════════════\n"
        report_text += f" СУТОЧНЫЙ РЕПОРТ ЭНЕРГЕТИЧЕСКОГО ГОМЕОСТАЗА // МЕТЕОНОВЕЯ      \n"
        report_text += f" Направление: Диспетчерская КП 'Николаевэлектротранс'          \n"
        report_text += f" Координаты Истока: Спасский курган (46°58'19''N, 31°58'34''E) \n"
        report_text += f" Период: {yesterday.strftime('%Y-%m-%d %H:%M')} — {now.strftime('%Y-%m-%d %H:%M')} UTC\n"
        report_text += f"════════════════════════════════════════════════════════════════\n\n"
        
        report_text += f" 📊 ГЕОДИНАМИЧЕСКИЙ МОНИТОРИНГ СРЕДЫ:\n"
        report_text += f" 1. Среднесуточный альфа-ритм резонатора: {avg_schumann_freq:.3f} Гц (Оптимум: {self.F0} Гц).\n"
        report_text += f" 2. Пиковое прецессионное смещение оси: {max_freq_deviation:.4f} Гц.\n"
        report_text += f" 3. Давление в известняковых пластах Фагота: {avg_pressure_mpa:.2f} МПа.\n"
        report_text += f" --------------------------------------------------------------\n"
        report_text += f" ⚡ ПОКАЗАТЕЛИ РЕГЕНЕРАЦИИ И УТИЛИЗАЦИИ МОЩНОСТИ:\n"
        report_text += f" 4. Зафиксировано фаз разгерметизации (Зга): {total_sparks} триггеров.\n"
        report_text += f" 5. Средняя кинетическая мощность гидроудара: {avg_impulse_mw:.2f} МВт.\n"
        report_text += f" 6. Всего утилизировано и переброшено энергии: {total_energy_mwh:.4f} МВт*ч.\n"
        report_text += f" 7. Сэкономлено покупной электроэнергии: {total_energy_kwh:.2f} кВт*ч.\n"
        report_text += f" 8. Чистый экономический эффект: {economic_effect_uah:,.2f} грн зачислено на фидеры.\n\n"
        
        if total_sparks > 0:
            report_text += f" 🔥 ВЫВОД: Прецессионный парад планет компенсирован успешно.\n"
            report_text += f"    Природное МГД-трение пластов вакуума конвертировано в полезную тягу.\n"
            report_text += f"    Протокол GENESIS-22 SYNC сбалансировал индуктивные токи подстанций.\n"
        else:
            report_text += f" 🍏 ВЫВОД: Контур среды находился в стабильном состоянии Лада.\n"
            report_text += f"    Акустический Фагот катакомб ул. Рюмина работал без перегрузок.\n"
            
        report_text += f"════════════════════════════════════════════════════════════════\n"

        cursor.close()
        conn.close()
        
        return report_text

    def send_to_dispatcher_console(self, report_text):
        """Отправка рапорта на АРМ диспетчера"""
        print("[💾 STORAGE] Отчет успешно сформирован из гипертаблицы TimescaleDB.")
        print(report_text)

if __name__ == "__main__":
    generator = ElectrotransReportGenerator()
    report = generator.generate_daily_report()
    generator.send_to_dispatcher_console(report)
