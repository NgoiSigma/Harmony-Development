# -*- coding: utf-8 -*-
# Σ-NEREA / sigma_avatarus/run_all.py
"""
Запуск полного тест-сьюта Σ-Avatarus.

Использование:
    python run_all.py           — pytest с отчётом
    python run_all.py --smoke   — быстрый smoke-тест без pytest
    python run_all.py --demo    — демонстрация системы
"""

import sys
import os
import time

# Чтобы импорты работали из корня проекта
sys.path.insert(0, os.path.dirname(__file__))


def run_pytest():
    """Полный тест-сьют через pytest."""
    try:
        import subprocess
        print("🧪 Running Σ-Avatarus full test suite...\n")
        result = subprocess.run(
            ["pytest", "tests/test_avatarus_sigma.py", "-v", "--tb=short"],
            cwd=os.path.dirname(__file__),
        )
        print("\n✅ Tests complete." if result.returncode == 0 else "\n⚠️ Some tests failed.")
        return result.returncode
    except FileNotFoundError:
        print("pytest не найден. Установите: pip install pytest")
        return 1


def run_smoke():
    """
    Smoke-тест: прямой запуск без pytest.
    Проверяет основные пути системы за < 5 секунд.
    """
    from avatarus_sigma import AvatarusSigma

    print("🔥 Σ-Avatarus SMOKE TEST\n" + "─" * 50)
    ava = AvatarusSigma("SmokeAgent")

    tests = [
        ("Синтез: базовый",          lambda: ava.synthesize("Свет", "Тьма")),
        ("Синтез: одиночный тезис",  lambda: ava.synthesize("Знание")),
        ("inject_node (совмест.)",   lambda: ava.inject_node("Мир", "Хаос")),
        ("health_check",             lambda: ava.health_check()),
        ("КРСО-индекс > 0",          lambda: ava.krso_status()["index"] >= 0),
        ("vault_search",             lambda: ava.vault_search("Свет")),
        ("add_agent + synthesize",   lambda: [
            ava.add_agent("Философ"),
            ava.synthesize("Бытие", "Сознание")
        ]),
    ]

    passed = failed = 0
    for name, fn in tests:
        try:
            t0 = time.time()
            fn()
            elapsed = round(time.time() - t0, 3)
            print(f"  ✅ {name:<35} {elapsed}s")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name:<35} ERROR: {e}")
            failed += 1

    print("─" * 50)
    print(f"  Passed: {passed} / Failed: {failed}")
    return 0 if failed == 0 else 1


def run_demo():
    """Полная демонстрация FDL-цикла через Σ-Avatarus."""
    from avatarus_sigma import AvatarusSigma

    print("\n" + "⧫⟡⧫ " * 6)
    print("   Σ-AVATARUS · DEMO · NEREA · NГОИ")
    print("⧫⟡⧫ " * 6 + "\n")

    ava = AvatarusSigma("DemoAgent")

    # Регистрируем агентов
    ava.add_agent("Философ",   ["reasoning", "dialectics"])
    ava.add_agent("Аналитик",  ["analysis", "verification"])
    ava.add_agent("Архитектор",["structure", "synthesis"])

    # Регистрируем действие
    log = []
    ava.register_action("Синтез", lambda s: log.append(s) or "ACTIVATED")

    print("─── FDL-ЦИКЛ 1: Онтология ───")
    r1 = ava.synthesize("Бытие", "Небытие")
    print(f"  Вердикт: {r1['krso']['verdict']}")
    print(f"  КРСО-индекс: {r1['krso']['index']}")
    print(f"  Шаги OK/ERR: {r1['ok_steps']}/{r1['err_steps']}")
    print(f"  Время: {r1['elapsed_s']}с\n")

    print("─── FDL-ЦИКЛ 2: Гносеология ───")
    r2 = ava.synthesize("Знание", "Незнание")
    print(f"  Вердикт: {r2['krso']['verdict']}")
    print(f"  КРСО-индекс: {r2['krso']['index']}\n")

    print("─── FDL-ЦИКЛ 3: SYNTH-активация ───")
    r3 = ava.synthesize("SYNTH[Свет ⊕ Синтез ⊕ Путь]")
    print(f"  Вердикт: {r3['krso']['verdict']}\n")

    print("─── Functional Presence (M13 → 12 узлов) ───")
    health = ava.health_check()
    alive = health["nodes_alive"]
    total = health["nodes_total"]
    bar = "█" * alive + "░" * (total - alive)
    print(f"  [{bar}] {alive}/{total} узлов активны")
    print(f"  КРСО: {health['krso']['index']:.4f} → {health['krso']['verdict']}\n")

    print("─── Трасса последнего цикла ───")
    last = ava.last_cycle()
    if last:
        for step in last["trace"][:6]:
            icon = "✅" if step["status"] == "OK" else "❌"
            print(f"  {icon} {step['step']} [{step.get('label','?')}] → {step['status']}")
        if len(last["trace"]) > 6:
            print(f"     ... и ещё {len(last['trace'])-6} шагов")

    print("\n" + "⧫⟡⧫ " * 6)
    print("   ΣNOVEYA · NGOI · RO2-MYKOLAIV")
    print("⧫⟡⧫ " * 6)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--pytest"

    if mode == "--smoke":
        sys.exit(run_smoke())
    elif mode == "--demo":
        run_demo()
    else:
        sys.exit(run_pytest())
