#ifndef CALCULATOR_ENGINE_H
#define CALCULATOR_ENGINE_H

#include <math.h>
#include <complex.h>
#include <stdbool.h>
#include <stddef.h>

// Version information
#define CALC_VERSION_MAJOR 1
#define CALC_VERSION_MINOR 0
#define CALC_VERSION_PATCH 0

// Error codes
typedef enum {
    CALC_SUCCESS = 0,
    CALC_ERROR_INVALID_INPUT,
    CALC_ERROR_DIVISION_BY_ZERO,
    CALC_ERROR_DOMAIN_ERROR,
    CALC_ERROR_OVERFLOW,
    CALC_ERROR_UNDERFLOW,
    CALC_ERROR_MEMORY_ERROR,
    CALC_ERROR_INVALID_FUNCTION,
    CALC_ERROR_PARSE_ERROR
} calc_error_t;

// Data types for different number formats
typedef struct {
    double real;
    double imag;
} calc_complex_t;

typedef struct {
    double value;
    bool has_error;
    calc_error_t error;
} calc_result_t;

// Calculator state structure
typedef struct {
    double memory;
    double last_result;
    bool angle_in_degrees;
    int precision;
    char last_expression[512];
} calc_state_t;

// Function prototypes

// Core calculator operations
calc_result_t calc_evaluate(const char* expression, calc_state_t* state);
calc_result_t calc_add(double a, double b);
calc_result_t calc_subtract(double a, double b);
calc_result_t calc_multiply(double a, double b);
calc_result_t calc_divide(double a, double b);
calc_result_t calc_power(double base, double exponent);
calc_result_t calc_sqrt(double x);
calc_result_t calc_cbrt(double x);
calc_result_t calc_nthroot(double x, int n);

// Trigonometric functions
calc_result_t calc_sin(double x, bool degrees);
calc_result_t calc_cos(double x, bool degrees);
calc_result_t calc_tan(double x, bool degrees);
calc_result_t calc_sec(double x, bool degrees);
calc_result_t calc_csc(double x, bool degrees);
calc_result_t calc_cot(double x, bool degrees);

// Inverse trigonometric functions
calc_result_t calc_asin(double x, bool degrees);
calc_result_t calc_acos(double x, bool degrees);
calc_result_t calc_atan(double x, bool degrees);
calc_result_t calc_atan2(double y, double x, bool degrees);

// Hyperbolic functions
calc_result_t calc_sinh(double x);
calc_result_t calc_cosh(double x);
calc_result_t calc_tanh(double x);
calc_result_t calc_sech(double x);
calc_result_t calc_csch(double x);
calc_result_t calc_coth(double x);

// Logarithmic functions
calc_result_t calc_log(double x);       // Natural log
calc_result_t calc_log10(double x);     // Base 10 log
calc_result_t calc_log2(double x);      // Base 2 log
calc_result_t calc_logb(double x, double base);  // Arbitrary base

// Exponential functions
calc_result_t calc_exp(double x);
calc_result_t calc_exp10(double x);
calc_result_t calc_exp2(double x);

// Special mathematical functions
calc_result_t calc_factorial(int n);
calc_result_t calc_gamma(double x);
calc_result_t calc_abs(double x);
calc_result_t calc_floor(double x);
calc_result_t calc_ceil(double x);
calc_result_t calc_round(double x);
calc_result_t calc_mod(double a, double b);

// Combinatorics
calc_result_t calc_permutation(int n, int r);
calc_result_t calc_combination(int n, int r);

// Number theory
calc_result_t calc_gcd(int a, int b);
calc_result_t calc_lcm(int a, int b);

// Complex number operations
calc_complex_t calc_complex_add(calc_complex_t a, calc_complex_t b);
calc_complex_t calc_complex_multiply(calc_complex_t a, calc_complex_t b);
calc_complex_t calc_complex_divide(calc_complex_t a, calc_complex_t b);
double calc_complex_magnitude(calc_complex_t z);
double calc_complex_phase(calc_complex_t z, bool degrees);

// Memory operations
void calc_memory_store(calc_state_t* state, double value);
void calc_memory_add(calc_state_t* state, double value);
void calc_memory_subtract(calc_state_t* state, double value);
double calc_memory_recall(calc_state_t* state);
void calc_memory_clear(calc_state_t* state);

// State management
calc_state_t* calc_create_state(void);
void calc_destroy_state(calc_state_t* state);
void calc_reset_state(calc_state_t* state);

// Utility functions
const char* calc_error_string(calc_error_t error);
bool calc_is_finite(double x);
bool calc_is_integer(double x);
double calc_deg_to_rad(double degrees);
double calc_rad_to_deg(double radians);

// Constants
extern const double CALC_PI;
extern const double CALC_E;
extern const double CALC_PHI;
extern const double CALC_SQRT2;
extern const double CALC_LN2;
extern const double CALC_LN10;

#endif // CALCULATOR_ENGINE_H