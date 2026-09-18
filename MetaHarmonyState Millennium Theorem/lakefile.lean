import Lake
open Lake System

package «harmony_development» where
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩
  ]

require mathlib from git
  "https://github.com"

@[default_target]
lean_lib «HarmonyDevelopment» where
  srcDir := "src"
  modules := #[
    `QumranAxis,
    `MonopoleCoupling,
    `NavierStokesFdl,
    `RiemannHypothesis,     -- Задачи тысячелетия Клэя 
    `P_vs_NP,               -- переведены в строгий
    `YangMills,             -- машинно-проверяемый
    `HodgeConjecture,       -- формат компилятора
    `BirchSwinnertonDyer   -- Lean 4
  ]
