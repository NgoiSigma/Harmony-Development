#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timezone

class MeteonoveyaStorage:
    def __init__(self, db_url="postgres://postgres:noveya_secret@localhost:5432/meteonoveya_db"):
        self.conn = psycopg2.connect(db_url)
        self.conn.autocommit = True

    def log_metrics(self, freq, noise, pressure, magnetic):
        """Пакетная запись текущего состояния автоколебательного контура холма"""
        with self.conn.cursor() as cursor:
            query = """
                INSERT INTO spas_hill_metrics (time, shumann_freq_hz, voldo_fac_noise, ingul_pressure_mpa, magnetic_field_nt)
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (datetime.now(timezone.utc), freq, noise, pressure, magnetic))

    def log_zinc_spark(self, activation_type, q_discharge, power_mw, grid_load):
        """Фиксация фазы разгерметизации и прорыва Зги в журнал событий"""
        with self.conn.cursor() as cursor:
            query = """
                INSERT INTO zinc_spark_events (time, activation_type, discharge_volume_q, impulse_power_mw, grid_transfer_load)
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (datetime.now(timezone.utc), activation_type, q_discharge, power_mw, grid_load))

    def get_weekly_ запруда_report(self):
        """Аналитический запрос: определение времени застоя (запруд) за неделю"""
        with self.conn.cursor() as cursor:
            query = """
                SELECT time_bucket('1 hour', time) AS hour_bucket,
                       avg(shumann_freq_hz) AS avg_freq,
                       max(ingul_pressure_mpa) AS max_pressure
                FROM spas_hill_metrics
                WHERE time > NOW() - INTERVAL '7 days'
                GROUP BY hour_bucket
                ORDER BY hour_bucket DESC;
            """
            cursor.execute(query)
            return cursor.fetchall()

    def close(self):
        self.conn.close()
