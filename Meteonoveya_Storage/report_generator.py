#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meteonoveya: Автоматический генератор ежесуточных отчетов для СУБД TimescaleDB.
Расчет энергетического гомеостаза и окупаемости переброшенной мощности (МВт).
"""

import psycopg2
from datetime import datetime, timedelta, timezone

class ElectrotransReportGenerator:
    def __init__(self, db_url="postgres://postgres:noveya_secret@localhost:5432/meteonoveya_db"):
        self.db_url = db_url
        # Тариф на электроэнергию для электротранспорта (условный, в грн за кВт*ч)
        self.energy_tariff_uah = 7.50 

    def generate_daily_report(self):
        """Агрегационный запрос к гипертаблице за прошедшие 24 часа"""
        now = datetime.now(timezone.utc)
        yesterday = now - timedelta(days=1)

        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()

        # Запрос рассчитывает: общее число прорывов Зги, среднюю мощность импульса,
        # суммарную переброшенную энергию (МВт*ч) на фидеры подстанций
        query = """
            SELECT 
                COUNT(*) as total_sparks,
                COALESCE(AVG(impulse_power_mw), 0) as avg_impulse_mw,
                COALESCE(SUM(grid_transfer_load * (2.4 / 3600.0)), 0) as total_energy_mwh
            FROM zinc_spark_events
            WHERE time >= %s AND time < %s;
        """
        
        cursor.execute(query, (yesterday, now))
        total_sparks, avg_impulse_mw, total_energy_mwh = cursor.fetchone()

        # Перевод МВт*ч в кВт*ч для финансового учета
        total_energy_kwh = total_energy_mwh * 1000.0
        economic_effect_uah = total_energy_kwh * self.energy_tariff_uah

        # Формирование текстовой матрицы рапорта
        report_text = f"════════════════════════════════════════════════════════════════\n"
        report_text += f" СУТОЧНЫЙ РЕПОРТ ЭНЕРГЕТИЧЕСКОГО ГОМЕОСТАЗА // МЕТЕОНОВЕЯ      \n"
        report_text += f" Направление: Диспетчерская КП 'Николаевэлектротранс'          \n"
        report_text += f" Период: {yesterday.strftime('%Y-%m-%d %H:%M')} — {now.strftime('%Y-%m-%d %H:%M')} UTC\n"
        report_text += f"════════════════════════════════════════════════════════════════\n\n"
        report_text += f" 1. Зафиксировано фаз разгерметизации (Зга): {total_sparks} триггеров.\n"
        report_text += f" 2. Средняя кинетическая мощность гидроудара: {avg_impulse_mw:.2f} МВт.\n"
        report_text += f" 3. Всего утилизировано и переброшено энергии: {total_energy_mwh:.4f} МВт*ч.\n"
        report_text += f" 4. Сэкономлено покупной электроэнергии: {total_energy_kwh:.2f} кВт*ч.\n"
        report_text += f" 5. Суммарный экономический эффект: {economic_effect_uah:.2f} грн.\n\n"
        
        if total_sparks > 0:
            report_text += f" 🔥 ВЫВОД: Прецессионный парад планет компенсирован успешно.\n"
            report_text += f"    Природное трение пластов конвертировано в полезную тягу.\n"
        else:
            report_text += f" 🍏 ВЫВОД: Контур среды находился в стабильном состоянии Лада.\n"
            report_text += f"    Акустический Фагот катакомб ул. Рюмина работал без перегрузок.\n"
            
        report_text += f"════════════════════════════════════════════════════════════════\n"

        cursor.close()
        conn.close()
        
        return report_text

    def send_to_dispatcher_console(self, report_text):
        """Эмуляция отправки рапорта на АРМ диспетчера через сетевой сокет"""
        print("[💾 STORAGE] Отчет успешно сформирован из гипертаблицы TimescaleDB.")
        print(report_text)
        # В реальной системе здесь вызывается отправка по протоколу MQTT или Telegram-API подстанций

if __name__ == "__main__":
    generator = ElectrotransReportGenerator()
    report = generator.generate_daily_report()
    generator.send_to_dispatcher_console(report)
