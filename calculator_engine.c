#include "calculator_engine.h"
#include "expression_parser.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <float.h>

// Mathematical constants
const double CALC_PI = M_PI;
const double CALC_E = M_E;
const double CALC_PHI = 1.6180339887498948482;
const double CALC_SQRT2 = M_SQRT2;
const double CALC_LN2 = M_LN2;
const double CALC_LN10 = M_LN10;

// Helper function to create result
static calc_result_t make_result(double value, calc_error_t error) {
    calc_result_t result;
    result.value = value;
    result.error = error;
    result.has_error = (error != CALC_SUCCESS);
    return result;
}

// Core arithmetic operations
calc_result_t calc_add(double a, double b) {
    double result = a + b;
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_subtract(double a, double b) {
    double result = a - b;
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_multiply(double a, double b) {
    double result = a * b;
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_divide(double a, double b) {
    if (b == 0.0) {
        return make_result(0.0, CALC_ERROR_DIVISION_BY_ZERO);
    }
    double result = a / b;
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_power(double base, double exponent) {
    // Handle special cases
    if (base == 0.0 && exponent < 0.0) {
        return make_result(0.0, CALC_ERROR_DIVISION_BY_ZERO);
    }
    if (base < 0.0 && !calc_is_integer(exponent)) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }

    double result = pow(base, exponent);
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_sqrt(double x) {
    if (x < 0.0) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    return make_result(sqrt(x), CALC_SUCCESS);
}

calc_result_t calc_cbrt(double x) {
    return make_result(cbrt(x), CALC_SUCCESS);
}

calc_result_t calc_nthroot(double x, int n) {
    if (n == 0) {
        return make_result(0.0, CALC_ERROR_DIVISION_BY_ZERO);
    }
    if (n % 2 == 0 && x < 0.0) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }

    double result = pow(x, 1.0 / n);
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

// Trigonometric functions
calc_result_t calc_sin(double x, bool degrees) {
    if (degrees) {
        x = calc_deg_to_rad(x);
    }
    return make_result(sin(x), CALC_SUCCESS);
}

calc_result_t calc_cos(double x, bool degrees) {
    if (degrees) {
        x = calc_deg_to_rad(x);
    }
    return make_result(cos(x), CALC_SUCCESS);
}

calc_result_t calc_tan(double x, bool degrees) {
    if (degrees) {
        x = calc_deg_to_rad(x);
    }

    // Check for undefined values (odd multiples of π/2)
    double normalized = fmod(x, M_PI);
    if (fabs(normalized - M_PI/2) < 1e-15 || fabs(normalized + M_PI/2) < 1e-15) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }

    return make_result(tan(x), CALC_SUCCESS);
}

calc_result_t calc_sec(double x, bool degrees) {
    calc_result_t cos_result = calc_cos(x, degrees);
    if (cos_result.has_error) {
        return cos_result;
    }
    if (fabs(cos_result.value) < 1e-15) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    return make_result(1.0 / cos_result.value, CALC_SUCCESS);
}

calc_result_t calc_csc(double x, bool degrees) {
    calc_result_t sin_result = calc_sin(x, degrees);
    if (sin_result.has_error) {
        return sin_result;
    }
    if (fabs(sin_result.value) < 1e-15) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    return make_result(1.0 / sin_result.value, CALC_SUCCESS);
}

calc_result_t calc_cot(double x, bool degrees) {
    calc_result_t tan_result = calc_tan(x, degrees);
    if (tan_result.has_error) {
        return tan_result;
    }
    if (fabs(tan_result.value) < 1e-15) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    return make_result(1.0 / tan_result.value, CALC_SUCCESS);
}

// Inverse trigonometric functions
calc_result_t calc_asin(double x, bool degrees) {
    if (x < -1.0 || x > 1.0) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    double result = asin(x);
    if (degrees) {
        result = calc_rad_to_deg(result);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_acos(double x, bool degrees) {
    if (x < -1.0 || x > 1.0) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    double result = acos(x);
    if (degrees) {
        result = calc_rad_to_deg(result);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_atan(double x, bool degrees) {
    double result = atan(x);
    if (degrees) {
        result = calc_rad_to_deg(result);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_atan2(double y, double x, bool degrees) {
    double result = atan2(y, x);
    if (degrees) {
        result = calc_rad_to_deg(result);
    }
    return make_result(result, CALC_SUCCESS);
}

// Hyperbolic functions
calc_result_t calc_sinh(double x) {
    double result = sinh(x);
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_cosh(double x) {
    double result = cosh(x);
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_tanh(double x) {
    return make_result(tanh(x), CALC_SUCCESS);
}

calc_result_t calc_sech(double x) {
    calc_result_t cosh_result = calc_cosh(x);
    if (cosh_result.has_error) {
        return cosh_result;
    }
    return make_result(1.0 / cosh_result.value, CALC_SUCCESS);
}

calc_result_t calc_csch(double x) {
    if (x == 0.0) {
        return make_result(0.0, CALC_ERROR_DIVISION_BY_ZERO);
    }
    calc_result_t sinh_result = calc_sinh(x);
    if (sinh_result.has_error) {
        return sinh_result;
    }
    return make_result(1.0 / sinh_result.value, CALC_SUCCESS);
}

calc_result_t calc_coth(double x) {
    if (x == 0.0) {
        return make_result(0.0, CALC_ERROR_DIVISION_BY_ZERO);
    }
    return make_result(coth(x), CALC_SUCCESS);
}

// Logarithmic functions
calc_result_t calc_log(double x) {
    if (x <= 0.0) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    return make_result(log(x), CALC_SUCCESS);
}

calc_result_t calc_log10(double x) {
    if (x <= 0.0) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    return make_result(log10(x), CALC_SUCCESS);
}

calc_result_t calc_log2(double x) {
    if (x <= 0.0) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    return make_result(log2(x), CALC_SUCCESS);
}

calc_result_t calc_logb(double x, double base) {
    if (x <= 0.0 || base <= 0.0 || base == 1.0) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    return make_result(log(x) / log(base), CALC_SUCCESS);
}

// Exponential functions
calc_result_t calc_exp(double x) {
    double result = exp(x);
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_exp10(double x) {
    double result = pow(10.0, x);
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_exp2(double x) {
    double result = pow(2.0, x);
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

// Special functions
calc_result_t calc_factorial(int n) {
    if (n < 0) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    if (n > 170) { // Factorial of 171 overflows double
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }

    double result = 1.0;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_gamma(double x) {
    if (x <= 0 && calc_is_integer(x)) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }
    double result = tgamma(x);
    if (!calc_is_finite(result)) {
        return make_result(0.0, CALC_ERROR_OVERFLOW);
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_abs(double x) {
    return make_result(fabs(x), CALC_SUCCESS);
}

calc_result_t calc_floor(double x) {
    return make_result(floor(x), CALC_SUCCESS);
}

calc_result_t calc_ceil(double x) {
    return make_result(ceil(x), CALC_SUCCESS);
}

calc_result_t calc_round(double x) {
    return make_result(round(x), CALC_SUCCESS);
}

calc_result_t calc_mod(double a, double b) {
    if (b == 0.0) {
        return make_result(0.0, CALC_ERROR_DIVISION_BY_ZERO);
    }
    return make_result(fmod(a, b), CALC_SUCCESS);
}

// Combinatorics
calc_result_t calc_permutation(int n, int r) {
    if (n < 0 || r < 0 || r > n) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }

    double result = 1.0;
    for (int i = n; i > n - r; i--) {
        result *= i;
        if (!calc_is_finite(result)) {
            return make_result(0.0, CALC_ERROR_OVERFLOW);
        }
    }
    return make_result(result, CALC_SUCCESS);
}

calc_result_t calc_combination(int n, int r) {
    if (n < 0 || r < 0 || r > n) {
        return make_result(0.0, CALC_ERROR_DOMAIN_ERROR);
    }

    // Use symmetry property: C(n,r) = C(n, n-r)
    if (r > n - r) {
        r = n - r;
    }

    double result = 1.0;
    for (int i = 0; i < r; i++) {
        result = result * (n - i) / (i + 1);
        if (!calc_is_finite(result)) {
            return make_result(0.0, CALC_ERROR_OVERFLOW);
        }
    }
    return make_result(result, CALC_SUCCESS);
}

// Number theory
calc_result_t calc_gcd(int a, int b) {
    a = abs(a);
    b = abs(b);

    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return make_result((double)a, CALC_SUCCESS);
}

calc_result_t calc_lcm(int a, int b) {
    if (a == 0 || b == 0) {
        return make_result(0.0, CALC_SUCCESS);
    }

    calc_result_t gcd_result = calc_gcd(a, b);
    if (gcd_result.has_error) {
        return gcd_result;
    }

    double result = (abs(a) * abs(b)) / gcd_result.value;
    return make_result(result, CALC_SUCCESS);
}

// Complex number operations
calc_complex_t calc_complex_add(calc_complex_t a, calc_complex_t b) {
    calc_complex_t result;
    result.real = a.real + b.real;
    result.imag = a.imag + b.imag;
    return result;
}

calc_complex_t calc_complex_multiply(calc_complex_t a, calc_complex_t b) {
    calc_complex_t result;
    result.real = a.real * b.real - a.imag * b.imag;
    result.imag = a.real * b.imag + a.imag * b.real;
    return result;
}

calc_complex_t calc_complex_divide(calc_complex_t a, calc_complex_t b) {
    calc_complex_t result;
    double denominator = b.real * b.real + b.imag * b.imag;

    if (denominator == 0.0) {
        result.real = INFINITY;
        result.imag = INFINITY;
        return result;
    }

    result.real = (a.real * b.real + a.imag * b.imag) / denominator;
    result.imag = (a.imag * b.real - a.real * b.imag) / denominator;
    return result;
}

double calc_complex_magnitude(calc_complex_t z) {
    return sqrt(z.real * z.real + z.imag * z.imag);
}

double calc_complex_phase(calc_complex_t z, bool degrees) {
    double phase = atan2(z.imag, z.real);
    if (degrees) {
        phase = calc_rad_to_deg(phase);
    }
    return phase;
}

// Memory operations
void calc_memory_store(calc_state_t* state, double value) {
    if (state) {
        state->memory = value;
    }
}

void calc_memory_add(calc_state_t* state, double value) {
    if (state) {
        state->memory += value;
    }
}

void calc_memory_subtract(calc_state_t* state, double value) {
    if (state) {
        state->memory -= value;
    }
}

double calc_memory_recall(calc_state_t* state) {
    return state ? state->memory : 0.0;
}

void calc_memory_clear(calc_state_t* state) {
    if (state) {
        state->memory = 0.0;
    }
}

// State management
calc_state_t* calc_create_state(void) {
    calc_state_t* state = malloc(sizeof(calc_state_t));
    if (state) {
        calc_reset_state(state);
    }
    return state;
}

void calc_destroy_state(calc_state_t* state) {
    if (state) {
        free(state);
    }
}

void calc_reset_state(calc_state_t* state) {
    if (state) {
        state->memory = 0.0;
        state->last_result = 0.0;
        state->angle_in_degrees = true;
        state->precision = 10;
        strcpy(state->last_expression, "");
    }
}

// Utility functions
const char* calc_error_string(calc_error_t error) {
    switch (error) {
        case CALC_SUCCESS: return "Success";
        case CALC_ERROR_INVALID_INPUT: return "Invalid input";
        case CALC_ERROR_DIVISION_BY_ZERO: return "Division by zero";
        case CALC_ERROR_DOMAIN_ERROR: return "Domain error";
        case CALC_ERROR_OVERFLOW: return "Overflow error";
        case CALC_ERROR_UNDERFLOW: return "Underflow error";
        case CALC_ERROR_MEMORY_ERROR: return "Memory error";
        case CALC_ERROR_INVALID_FUNCTION: return "Invalid function";
        case CALC_ERROR_PARSE_ERROR: return "Parse error";
        default: return "Unknown error";
    }
}

bool calc_is_finite(double x) {
    return isfinite(x);
}

bool calc_is_integer(double x) {
    return x == floor(x);
}

double calc_deg_to_rad(double degrees) {
    return degrees * M_PI / 180.0;
}

double calc_rad_to_deg(double radians) {
    return radians * 180.0 / M_PI;
}

// Main evaluation function (uses expression parser)
calc_result_t calc_evaluate(const char* expression, calc_state_t* state) {
    if (!expression || !state) {
        return make_result(0.0, CALC_ERROR_INVALID_INPUT);
    }

    // Store expression for reference
    strncpy(state->last_expression, expression, sizeof(state->last_expression) - 1);
    state->last_expression[sizeof(state->last_expression) - 1] = '\0';

    // Use expression parser to evaluate
    parse_result_t parse_result = parse_expression(expression, state);

    if (parse_result.error != PARSE_SUCCESS) {
        return make_result(0.0, CALC_ERROR_PARSE_ERROR);
    }

    state->last_result = parse_result.value;
    return make_result(parse_result.value, CALC_SUCCESS);
}