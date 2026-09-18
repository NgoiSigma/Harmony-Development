import Lake
open Lake System

package «harmony_development» where
  leanOptions := #[
    `pp.unicode.fun, true
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «HarmonyDevelopment» where
  -- Указываем текущую директорию как корень модулей, так как файлы лежат там
  srcDir := "."
  modules := #[
    `QumranAxis,
    `MonopoleCoupling,
    `NavierStokesFdl,
    `RiemannHypothesis,
    `P_vs_NP,
    `YangMills,
    `HodgeConjecture,
    `BirchSwinnertonDyer,
    `Main
  ]
