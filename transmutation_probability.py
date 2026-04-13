import math
import numpy as np
import matplotlib.pyplot as plt

# === МОДЕЛЬ: Резонансная трансмутация и накопление ресурсов ===

# === Основные параметры ===
MAX_DEPTH = 150  # км

def transmutation_probability(d, P, T, EM, E, f, phi):
    """Расчёт вероятности трансмутации"""
    term1 = math.sin((2 * math.pi * d) / MAX_DEPTH)
    term2 = P * T * EM
    term3 = E * math.sin(2 * math.pi * f + phi)
    return term1 * term2 * term3

def hydrocarbon_accumulation(probability, d):
    """Вероятность накопления углеводородов"""
    return probability * math.exp(-d / 50)

def transmutation_energy(P, T, EM):
    """Энергия трансмутации как функция давления, температуры и поля"""
    return P * T * math.log(EM)

# === Пример использования ===
example_depths = np.linspace(10, 150, 50)  # 50 точек
probabilities = []
accumulations = []
energies = []

for d in example_depths:
    P = 50 + (d / 3)         # давление
    T = 1000 + d * 4         # температура
    EM = 3 + (d / 100)       # напряжённость поля
    E = 10                   # энергия осциллятора
    f = 5                    # частота
    phi = math.pi / 4        # фазовый сдвиг

    prob = transmutation_probability(d, P, T, EM, E, f, phi)
    acc = hydrocarbon_accumulation(prob, d)
    energy = transmutation_energy(P, T, EM)

    probabilities.append(prob)
    accumulations.append(acc)
    energies.append(energy)

# === Визуализация результатов ===
plt.figure(figsize=(12, 6))

plt.subplot(1, 3, 1)
plt.plot(example_depths, probabilities, label='Transmutation Probability', color='purple')
plt.xlabel('Глубина (км)')
plt.ylabel('Вероятность')
plt.title('Резонансная трансмутация')
plt.grid(True)

plt.subplot(1, 3, 2)
plt.plot(example_depths, accumulations, label='Hydrocarbon Accumulation', color='green')
plt.xlabel('Глубина (км)')
plt.ylabel('Вероятность накопления')
plt.title('Накопление углеводородов')
plt.grid(True)

plt.subplot(1, 3, 3)
plt.plot(example_depths, energies, label='Transmutation Energy', color='orange')
plt.xlabel('Глубина (км)')
plt.ylabel('Энергия')
plt.title('Энергия трансмутации')
plt.grid(True)

plt.tight_layout()
plt.show()

# === Консольный вывод одной точки ===
def show_example_point(d=100):
    P = 50 + (d / 3)
    T = 1000 + d * 4
    EM = 3 + (d / 100)
    E = 10
    f = 5
    phi = math.pi / 4

    prob = transmutation_probability(d, P, T, EM, E, f, phi)
    acc = hydrocarbon_accumulation(prob, d)
    energy = transmutation_energy(P, T, EM)

    print("\n🌍 Пример для глубины:", d, "км")
    print("  Давление:", round(P, 2))
    print("  Температура:", round(T, 2), "K")
    print("  Напряжённость поля:", round(EM, 2))
    print("  ↳ Вероятность трансмутации:", round(prob, 3))
    print("  ↳ Накопление углеводородов:", round(acc, 3))
    print("  ↳ Энергия трансмутации:", round(energy, 1))

if __name__ == "__main__":
    show_example_point(100)
