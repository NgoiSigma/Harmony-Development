import Lake
open Lake System

package «harmony_development» where
  -- Unicode-символы для корректного отображения инвариантов FDL/Qumran в консоли
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩
  ]

/-- 
  Подключение официальной математической библиотеки Lean 4 (Mathlib).
  Она содержит топологические пространства, матрицы, тензоры и операторы ContDiff.
-/
require mathlib from git
  "https://github.com"

/-- Главная библиотека проекта, объединяющая модули воедино -/
@[default_target]
lean_lib «HarmonyDevelopment» where
  -- Путь к исходным кодам. Модули должны лежать в папке `src/`
  srcDir := "src"
  -- Список компилируемых файлов в контуре репозитория НГОИ/ММТД
  modules := #[
    `QumranAxis,
    `NavierStokesFdl
  ]
