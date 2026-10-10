// Lean compiler output
// Module: src.KrivitskyEarthCore
// Imports: Init
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
static double l_apply__krivitsky__dissipation___closed__2;
uint8_t lean_float_decLt(double, double);
static uint8_t l_lemma__krivitsky__core__flux__valid___nativeDecide__1___closed__1;
LEAN_EXPORT lean_object* l_apply__krivitsky__dissipation(lean_object*);
static double l_apply__krivitsky__dissipation___closed__1;
double l_Float_ofScientific(lean_object*, uint8_t, lean_object*);
LEAN_EXPORT uint8_t l_lemma__krivitsky__core__flux__valid___nativeDecide__1;
static double _init_l_apply__krivitsky__dissipation___closed__1() {
_start:
{
lean_object* x_1; uint8_t x_2; lean_object* x_3; double x_4; 
x_1 = lean_unsigned_to_nat(450u);
x_2 = 1;
x_3 = lean_unsigned_to_nat(1u);
x_4 = l_Float_ofScientific(x_1, x_2, x_3);
return x_4;
}
}
static double _init_l_apply__krivitsky__dissipation___closed__2() {
_start:
{
lean_object* x_1; uint8_t x_2; lean_object* x_3; double x_4; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = 1;
x_3 = lean_unsigned_to_nat(1u);
x_4 = l_Float_ofScientific(x_1, x_2, x_3);
return x_4;
}
}
LEAN_EXPORT lean_object* l_apply__krivitsky__dissipation(lean_object* x_1) {
_start:
{
uint8_t x_2; 
x_2 = lean_ctor_get_uint8(x_1, 17);
if (x_2 == 0)
{
uint8_t x_3; 
x_3 = !lean_is_exclusive(x_1);
if (x_3 == 0)
{
uint8_t x_4; double x_5; 
x_4 = 1;
x_5 = l_apply__krivitsky__dissipation___closed__1;
lean_ctor_set_uint8(x_1, 16, x_4);
lean_ctor_set_float(x_1, 8, x_5);
return x_1;
}
else
{
double x_6; uint8_t x_7; double x_8; lean_object* x_9; 
x_6 = lean_ctor_get_float(x_1, 0);
lean_dec(x_1);
x_7 = 1;
x_8 = l_apply__krivitsky__dissipation___closed__1;
x_9 = lean_alloc_ctor(0, 0, 18);
lean_ctor_set_float(x_9, 0, x_6);
lean_ctor_set_uint8(x_9, 16, x_7);
lean_ctor_set_float(x_9, 8, x_8);
lean_ctor_set_uint8(x_9, 17, x_2);
return x_9;
}
}
else
{
uint8_t x_10; 
x_10 = !lean_is_exclusive(x_1);
if (x_10 == 0)
{
uint8_t x_11; double x_12; 
x_11 = 0;
x_12 = l_apply__krivitsky__dissipation___closed__2;
lean_ctor_set_uint8(x_1, 16, x_11);
lean_ctor_set_float(x_1, 8, x_12);
return x_1;
}
else
{
double x_13; uint8_t x_14; double x_15; lean_object* x_16; 
x_13 = lean_ctor_get_float(x_1, 0);
lean_dec(x_1);
x_14 = 0;
x_15 = l_apply__krivitsky__dissipation___closed__2;
x_16 = lean_alloc_ctor(0, 0, 18);
lean_ctor_set_float(x_16, 0, x_13);
lean_ctor_set_uint8(x_16, 16, x_14);
lean_ctor_set_float(x_16, 8, x_15);
lean_ctor_set_uint8(x_16, 17, x_2);
return x_16;
}
}
}
}
static uint8_t _init_l_lemma__krivitsky__core__flux__valid___nativeDecide__1___closed__1() {
_start:
{
double x_1; double x_2; uint8_t x_3; 
x_1 = l_apply__krivitsky__dissipation___closed__2;
x_2 = l_apply__krivitsky__dissipation___closed__1;
x_3 = lean_float_decLt(x_1, x_2);
return x_3;
}
}
static uint8_t _init_l_lemma__krivitsky__core__flux__valid___nativeDecide__1() {
_start:
{
uint8_t x_1; 
x_1 = l_lemma__krivitsky__core__flux__valid___nativeDecide__1___closed__1;
return x_1;
}
}
lean_object* initialize_Init(uint8_t builtin, lean_object*);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_src_KrivitskyEarthCore(uint8_t builtin, lean_object* w) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
l_apply__krivitsky__dissipation___closed__1 = _init_l_apply__krivitsky__dissipation___closed__1();
l_apply__krivitsky__dissipation___closed__2 = _init_l_apply__krivitsky__dissipation___closed__2();
l_lemma__krivitsky__core__flux__valid___nativeDecide__1___closed__1 = _init_l_lemma__krivitsky__core__flux__valid___nativeDecide__1___closed__1();
l_lemma__krivitsky__core__flux__valid___nativeDecide__1 = _init_l_lemma__krivitsky__core__flux__valid___nativeDecide__1();
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
