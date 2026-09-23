<<<<<<< HEAD
import Lake
open Lake DSL

package «harmony_development» where
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.11.0"

@[default_target]
lean_lib «HarmonyDevelopment» where
  -- Указываем текущую директорию как корень модулей, так как файлы лежат там
  srcDir := "."
=======
import Lake
open Lake DSL

package «harmony_development» where
  leanOptions := #[
    ⟨`pp.unicode.fun, true⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.11.0"

@[default_target]
lean_lib «HarmonyDevelopment» where
  -- Указываем текущую директорию как корень модулей, так как файлы лежат там
  srcDir := "."
>>>>>>> c5e96e566937d44055d4597b5a24f3e44ce223af
