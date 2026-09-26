import Lake
open Lake System

package «harmony_development» where
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.11.0"

@[default_target]
lean_lib «HarmonyDevelopment» where
  srcDir := "."
  modules := #[
    `Main,
    `ThreeBodyPhaseLock
  ]
