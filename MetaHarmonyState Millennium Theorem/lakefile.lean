import Lake
open Lake System

package «harmony_development» where
  -- Настройки пакета
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩ -- Включение красивого вывода юникода
  ]

require mathlib from git
  "https://github.com"

@[default_target]
lean_lib «HarmonyDevelopment» where
  -- Корневая библиотека проекта
  srcDir := "src"
