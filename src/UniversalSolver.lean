/-!
# Code 19 complexity model

The 19-axis condition is a type invariant. The theorem below establishes the
behavior of this model; it does not identify the classical complexity classes.
-/

inductive SoftwareStackLayer where
  | Tanakh
  | Gospel
  | Quran
  deriving DecidableEq, Repr

structure ComplexityContext where
  is_flat_turing : Bool
  angel_axes_count : Nat
  h_code19 : angel_axes_count = 19
  p_complexity : Float
  np_complexity : Float

def evaluate_p_vs_np (ctx : ComplexityContext) : ComplexityContext :=
  if ctx.angel_axes_count == 19 then
    { ctx with p_complexity := ctx.np_complexity }
  else
    ctx

theorem evaluate_p_vs_np_code19 (ctx : ComplexityContext) :
    (evaluate_p_vs_np ctx).p_complexity = (evaluate_p_vs_np ctx).np_complexity := by
  unfold evaluate_p_vs_np
  simp [ctx.h_code19]
