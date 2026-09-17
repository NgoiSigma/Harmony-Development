#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meteonoveya Диспетчерский интерфейс ГИС верхнего уровня
Визуализация частотных пульсаций среды и точек выклинивания подземных вод (Зга)
"""

import sys
import mmap
import ctypes
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer, Qt
import pyqtgraph as pg

# Описание структуры SHM для маппинга с C++
class TelemetrySHM(ctypes.Structure):
    _fields_ = [
        ("current_shumann_freq", ctypes.c_float),
        ("target_q_discharge", ctypes.c_float),
        ("trigger_genesis_valve", ctypes.c_bool),
        ("electrotrans_grid_load", ctypes.c_float)
    ]

class MeteonoveyaUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("МЕТЕОНОВЕЯ // ГИС-ИНТЕРФЕЙС ОПЕРАТОРА СПАССКОГО ХОЛМА")
        self.setGeometry(100, 100, 1280, 800)
        self.setStyleSheet("background-color: #0b0f19; color: #d1d5db; font-family: 'Courier New';")

        # Подключение к разделяемой памяти RT-ядра
        try:
            self.shm_file = open("/dev/shm/meteonoveya_shm", "r+b")
            self.shm_mem = mmap.mmap(self.shm_file.fileno(), ctypes.sizeof(TelemetrySHM))
            print("[🟢 UI_OK] Успешное сопряжение с RT-шиной Pranoveya.")
        except FileNotFoundError:
            self.shm_mem = None
            print("[⚠️ UI_WARN] Разделяемая память не найдена. Запущена программная эмуляция.")

        # Инициализация графических компонентов
        self.init_layouts()
        
        # Таймер обновления экрана (10 Гц / 100 мс — синхронно с RT-шагом)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_telemetry)
        self.timer.start(100)

        # Буфер для графика пульсации Зги
        self.data_buffer = np.zeros(200)

    def init_layouts(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # ЛЕВАЯ ПАНЕЛЬ: Картографический ГИС-подслой и телеметрия
        left_panel = QVBoxLayout()
        
        self.lbl_title = QLabel("📍 НИКОЛАЕВСКИЙ ТЕКТОНИЧЕСКИЙ УЗЕЛ // КОНТУР ЛАДА")
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #38bdf8; padding: 10px;")
        left_panel.addWidget(self.lbl_title)

        # Панель индикаторов (Ячейки Вселенной)
        self.lbl_freq = QLabel("Частота резонатора Спасского холма: 7.83 Гц")
        self.lbl_freq.setStyleSheet("font-size: 14px; background-color: #1e293b; padding: 15px; border-radius: 5px;")
        left_panel.addWidget(self.lbl_freq)

        self.lbl_valve = QLabel("Статус запруды Ингула: ПРОТОК СТАБИЛЕН (12.5%)")
        self.lbl_valve.setStyleSheet("font-size: 14px; background-color: #1e293b; padding: 15px; border-radius: 5px;")
        left_panel.addWidget(self.lbl_valve)

        self.lbl_grid = QLabel("Тяговая сеть Николаевэлектротранса: Оптимум")
        self.lbl_grid.setStyleSheet("font-size: 14px; background-color: #1e293b; padding: 15px; border-radius: 5px;")
        left_panel.addWidget(self.lbl_grid)

        # Кнопка принудительной разгерметизации запруды (Инициация Зги)
        self.btn_trigger = QPushButton("⚡ ИНИЦИИРОВАТЬ ЦИНКОВЫЙ САЛЮТ (ГЕНЕЗИС-22)")
        self.btn_trigger.setStyleSheet("""
            QPushButton { background-color: #ef4444; color: white; font-weight: bold; padding: 15px; border-radius: 5px; }
            QPushButton:hover { background-color: #dc2626; }
        """)
        self.btn_trigger.clicked.connect(self.manual_genesis_trigger)
        left_panel.addWidget(self.btn_trigger)

        main_layout.addLayout(left_panel, stretch=1)

        # ПРАВАЯ ПАНЕЛЬ: Волновой осциллограф частоты выклинивания (Зга)
        right_panel = QVBoxLayout()
        
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#111827')
        self.plot_widget.setTitle("АКУСТИЧЕСКИЙ ОСЦИЛЛОГРАФ ПОДЗЕМНОГО ФАГОТА (ЗГА)", color="#38bdf8", size="12pt")
        self.plot_widget.setLabel('left', 'Амплитуда/Энергия импульса')
        self.plot_widget.setLabel('bottom', 'Дискретные кванты времени (Миги)')
        self.plot_curve = self.plot_widget.plot(pen=pg.mkPen(color='#10b981', width=2))
        
        right_panel.addWidget(self.plot_widget)
        main_layout.addLayout(right_panel, stretch=2)

    def manual_genesis_trigger(self):
        if self.shm_mem:
            # Запись команды прорыва напрямую на шину С++ модуля реального времени
            shm_struct = TelemetrySHM.from_buffer(self.shm_mem)
            shm_struct.trigger_genesis_valve = True
            shm_struct.target_q_discharge = 8.84
            print("[UI_ACTION] Отправлен ручной импульс прорыва запруды на ядро Pranoveya.")

    def update_telemetry(self):
        if self.shm_mem:
            self.shm_mem.seek(0)
            shm_struct = TelemetrySHM.from_buffer(self.shm_mem)
            freq = shm_struct.current_shumann_freq
            grid_load = shm_struct.electrotrans_grid_load
            valve_active = shm_struct.trigger_genesis_valve
        else:
            # Эмуляция автоколебательного цикла в отсутствие физического RT-ядра
            freq = 7.83 + 0.1 * np.sin(sys.time() if hasattr(sys, 'time') else QTimer.remainingTime(self)/100)
            grid_load = 45.2
            valve_active = False

        # Обновление текстовых матриц интерфейса
        self.lbl_freq.setText(f"Частота резонатора Спасского холма: {freq:.2f} Гц")
        
        if freq < 6.0 or valve_active:
            self.lbl_freq.setStyleSheet("font-size: 14px; background-color: #7f1d1d; color: #fca5a5; padding: 15px; border-radius: 5px;")
            self.lbl_valve.setText("Статус запруды Ингула: ГИДРОУДАР / РАЗГЕРМЕТИЗАЦИЯ (100%)")
            self.lbl_valve.setStyleSheet("font-size: 14px; background-color: #7f1d1d; color: #fca5a5; padding: 15px; border-radius: 5px;")
            # Моделирование высокочастотного цинкового всплеска (Зги) на осциллографе
            new_signal = np.random.normal(5.0, 1.0)
        else:
            self.lbl_freq.setStyleSheet("font-size: 14px; background-color: #1e293b; color: #d1d5db; padding: 15px; border-radius: 5px;")
            self.lbl_valve.setText("Статус запруды Ингула: ПРОТОК СТАБИЛЕН (12.5%)")
            self.lbl_valve.setStyleSheet("font-size: 14px; background-color: #1e293b; color: #d1d5db; padding: 15px; border-radius: 5px;")
            # Штатная пульсация альфа-оптимума
            new_signal = np.random.normal(0.2, 0.05)

        # Сдвиг буфера осциллографа
        self.data_buffer = np.roll(self.data_buffer, -1)
        self.data_buffer[-1] = new_signal
        self.plot_curve.setData(self.data_buffer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MeteonoveyaUI()
    ui.show()
    sys.exit(app.exec())
