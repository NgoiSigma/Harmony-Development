# ProtoCoreProcessor – ядро обработки и интеграции потоков для системы МЕТЕОНОВЕЯ

# 📦 Автоматическая установка необходимых библиотек
import subprocess
import sys

required_packages = ["flask", "requests", "matplotlib"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"📦 Устанавливаем отсутствующий пакет: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

from datetime import datetime
import math
import requests
import matplotlib.pyplot as plt
import json
import os
from flask import Flask, render_template_string, send_from_directory

class EgyptianAstroCycle:
    def __init__(self):
        self.stellar_calendar = {
            "Sirius Rising": "2025-07-23",
            "Regulus Zenith": "2025-08-04",
            "Orion Alignment": "2025-12-03"
        }
        self.lunar_phase_map = {
            "New Moon": ["2025-01-29", "2025-02-28", "2025-03-29"],
            "Full Moon": ["2025-01-14", "2025-02-13", "2025-03-14"]
        }

    def get_current_astro_state(self, date_str=None):
        if date_str is None:
            date_str = datetime.utcnow().strftime("%Y-%m-%d")
        state = {"stellar": [], "lunar": None}
        for name, date in self.stellar_calendar.items():
            if date == date_str:
                state["stellar"].append(name)
        for phase, dates in self.lunar_phase_map.items():
            if date_str in dates:
                state["lunar"] = phase
        return state

    def calculate_flood_risk_index(self, date_str):
        state = self.get_current_astro_state(date_str)
        if "Sirius Rising" in state["stellar"] and state["lunar"] == "Full Moon":
            return 0.95
        elif state["lunar"] == "Full Moon":
            return 0.7
        elif "Sirius Rising" in state["stellar"]:
            return 0.6
        else:
            return 0.3

class KrivitskyGeoEnergetics:
    def get_subcore_resonance_index(self, date_str):
        year = int(date_str.split("-")[0])
        modulation = abs((year % 11) - 5.5) / 5.5
        return round(1.0 - modulation * 0.6, 3)

    def get_plume_activation_index(self, date_str):
        year = int(date_str.split("-")[0])
        base = ((year % 7) + 1) / 7
        return round(0.5 + 0.4 * math.sin(base * math.pi), 3)

    def get_transmutation_potential(self, date_str):
        month = int(date_str.split("-")[1])
        return round(0.4 + 0.05 * (month % 6), 3)

class GeoMeteoStream:
    def __init__(self):
        self.api_key = None
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def set_api_key(self, key):
        self.api_key = key

    def fetch_current_weather(self, city="Cairo"):
        if not self.api_key:
            raise ValueError("API key not set for GeoMeteoStream")
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            temp = data["main"]["temp"]
            pressure = data["main"]["pressure"]
            humidity = data["main"]["humidity"]
            return {"temp": temp, "pressure": pressure, "humidity": humidity}
        except Exception as e:
            print(f"Ошибка при получении данных погоды: {e}")
            return {"temp": 20, "pressure": 1013, "humidity": 50}

    def compute_meteo_index(self, weather_data):
        pressure_var = abs(1013 - weather_data["pressure"]) / 20.0
        humidity_factor = weather_data["humidity"] / 100.0
        return round((pressure_var + humidity_factor) / 2.0, 3)

class SchumannResonanceModule:
    def __init__(self):
        self.mock_data = {
            "2025-01-14": 7.83,
            "2025-02-13": 8.12,
            "2025-03-14": 8.54,
            "2025-04-14": 9.21,
            "2025-05-02": 8.88
        }

    def get_flux_for_date(self, date_str):
        value = self.mock_data.get(date_str, 7.8)
        normalized = (value - 7.8) / 2.0
        return round(min(max(normalized, 0), 1.0), 3)

class ProtoCoreProcessor:
    def __init__(self, api_key):
        self.astro_module = EgyptianAstroCycle()
        self.geo_module = KrivitskyGeoEnergetics()
        self.meteo_module = GeoMeteoStream()
        self.meteo_module.set_api_key(api_key)
        self.schumann_module = SchumannResonanceModule()

    def collect_inputs(self, date_str):
        astro_state = self.astro_module.get_current_astro_state(date_str)
        flood_risk = self.astro_module.calculate_flood_risk_index(date_str)
        subcore_index = self.geo_module.get_subcore_resonance_index(date_str)
        plume_index = self.geo_module.get_plume_activation_index(date_str)
        transmut_index = self.geo_module.get_transmutation_potential(date_str)
        weather = self.meteo_module.fetch_current_weather()
        meteo_index = self.meteo_module.compute_meteo_index(weather)
        solar_index = 0.5
        schumann_flux = self.schumann_module.get_flux_for_date(date_str)
        return {
            "date": date_str,
            "astro_state": astro_state,
            "flood_risk": flood_risk,
            "solar_index": solar_index,
            "schumann_flux": schumann_flux,
            "meteo_index": meteo_index,
            "core_index": subcore_index,
            "plume_index": plume_index,
            "transmutation_index": transmut_index,
            "weather_raw": weather
        }

    def synthesize_resonance_state(self, data):
        resonance_sum = (
            data["flood_risk"] * 0.2 +
            data["solar_index"] * 0.1 +
            data["schumann_flux"] * 0.1 +
            data["meteo_index"] * 0.1 +
            data["core_index"] * 0.25 +
            data["plume_index"] * 0.15 +
            data["transmutation_index"] * 0.1
        )
        if resonance_sum >= 0.8:
            status = "⚠️ Потенциальный резонансный сдвиг (Кривицкий/Чижевский/Вернадский)"
        elif resonance_sum >= 0.6:
            status = "ℹ️ Активный гармонический фон, возможна смена биоциклов"
        else:
            status = "✅ Стабильное состояние среды"
        return {"resonance_level": round(resonance_sum, 3), "status": status}

    def generate_plot(self, data, path="static/plot.png"):
        labels = ["Flood", "Solar", "Schumann", "Meteo", "Core", "Plume", "Transmutation"]
        values = [data[k] for k in ["flood_risk", "solar_index", "schumann_flux", "meteo_index", "core_index", "plume_index", "transmutation_index"]]
        plt.figure(figsize=(10, 5))
        bars = plt.bar(labels, values, color="skyblue")
        plt.ylim(0, 1)
        plt.title("Карта резонансных индексов среды")
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, height + 0.02, f"{height:.2f}", ha='center')
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        os.makedirs("static", exist_ok=True)
        plt.savefig(path)
        plt.close()

app = Flask(__name__)
API_KEY = "YOUR_API_KEY_HERE"
core = ProtoCoreProcessor(API_KEY)

template = """
<!DOCTYPE html>
<html>
<head>
    <title>МЕТЕОНОВЕЯ — Состояние среды</title>
</head>
<body>
    <h1>Резонансная карта на {{ date }}</h1>
    <p><strong>Погода:</strong> {{ weather }}</p>
    <p><strong>Резонансный статус:</strong> {{ status }}</p>
    <img src="/static/plot.png" alt="График резонансных индексов" width="800">
    <ul>
        {% for k, v in resonance.items() %}
        <li>{{ k }}: {{ v }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/")
def index():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    inputs = core.collect_inputs(today)
    synthesis = core.synthesize_resonance_state(inputs)
    core.generate_plot(inputs)
    weather = inputs["weather_raw"]
    display_weather = f"Темп: {weather['temp']}°C, Давление: {weather['pressure']} гПа, Влажность: {weather['humidity']}%"
    resonance = {
        "flood_risk": inputs["flood_risk"],
        "solar_index": inputs["solar_index"],
        "schumann_flux": inputs["schumann_flux"],
        "meteo_index": inputs["meteo_index"],
        "core_index": inputs["core_index"],
        "plume_index": inputs["plume_index"],
        "transmutation_index": inputs["transmutation_index"]
    }
    return render_template_string(template, date=today, weather=display_weather, status=synthesis["status"], resonance=resonance)

if __name__ == "__main__":
    import webbrowser, threading

    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000/")

    threading.Timer(1, open_browser).start()
    app.run(debug=False, use_reloader=False)
