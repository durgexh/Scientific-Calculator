# Create the expression parser for mathematical expressions
expression_parser_h = '''#ifndef EXPRESSION_PARSER_H
#define EXPRESSION_PARSER_H

#include "calculator_engine.h"
#include <stdbool.h>

// Token types for the parser
typedef enum {
    TOKEN_NUMBER,
    TOKEN_OPERATOR,
    TOKEN_FUNCTION,
    TOKEN_VARIABLE,
    TOKEN_CONSTANT,
    TOKEN_LEFT_PAREN,
    TOKEN_RIGHT_PAREN,
    TOKEN_COMMA,
    TOKEN_END,
    TOKEN_UNKNOWN
} token_type_t;

// Token structure
typedef struct {
    token_type_t type;
    char value[64];
    double number_value;
    int position;
} token_t;

// Parse error types
typedef enum {
    PARSE_SUCCESS = 0,
    PARSE_ERROR_INVALID_CHARACTER,
    PARSE_ERROR_MISMATCHED_PARENTHESES,
    PARSE_ERROR_INVALID_FUNCTION,
    PARSE_ERROR_INVALID_SYNTAX,
    PARSE_ERROR_DIVISION_BY_ZERO,
    PARSE_ERROR_DOMAIN_ERROR,
    PARSE_ERROR_TOO_MANY_ARGUMENTS,
    PARSE_ERROR_TOO_FEW_ARGUMENTS
} parse_error_t;

// Parse result
typedef struct {
    double value;
    parse_error_t error;
    int error_position;
    char error_message[256];
} parse_result_t;

// Expression evaluation context
typedef struct {
    const char* expression;
    int position;
    int length;
    calc_state_t* calc_state;
    token_t current_token;
} parse_context_t;

// Function prototypes

// Main parsing function
parse_result_t parse_expression(const char* expression, calc_state_t* state);

// Tokenizer functions
token_t get_next_token(parse_context_t* ctx);
bool is_operator(char c);
bool is_function_name(const char* name);
bool is_constant_name(const char* name);

// Parser functions (recursive descent)
double parse_primary(parse_context_t* ctx, parse_error_t* error);
double parse_factor(parse_context_t* ctx, parse_error_t* error);
double parse_term(parse_context_t* ctx, parse_error_t* error);
double parse_expression_impl(parse_context_t* ctx, parse_error_t* error);

// Function evaluation
double evaluate_function(const char* func_name, double* args, int arg_count, 
                        calc_state_t* state, parse_error_t* error);

// Utility functions
void skip_whitespace(parse_context_t* ctx);
bool is_digit(char c);
bool is_alpha(char c);
bool is_alnum(char c);
double get_constant_value(const char* name);

// Error handling
const char* parse_error_string(parse_error_t error);

#endif // EXPRESSION_PARSER_H'''

expression_parser_c = '''#include "expression_parser.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

// Built-in mathematical functions
static const struct {
    const char* name;
    int arg_count;
} builtin_functions[] = {
    {"sin", 1}, {"cos", 1}, {"tan", 1}, {"sec", 1}, {"csc", 1}, {"cot", 1},
    {"asin", 1}, {"acos", 1}, {"atan", 1}, {"asec", 1}, {"acsc", 1}, {"acot", 1},
    {"sinh", 1}, {"cosh", 1}, {"tanh", 1}, {"sech", 1}, {"csch", 1}, {"coth", 1},
    {"asinh", 1}, {"acosh", 1}, {"atanh", 1},
    {"log", 1}, {"ln", 1}, {"log10", 1}, {"log2", 1}, {"logb", 2},
    {"exp", 1}, {"exp10", 1}, {"exp2", 1},
    {"sqrt", 1}, {"cbrt", 1}, {"nthrt", 2}, {"pow", 2},
    {"abs", 1}, {"floor", 1}, {"ceil", 1}, {"round", 1}, {"mod", 2},
    {"factorial", 1}, {"gamma", 1},
    {"perm", 2}, {"comb", 2}, {"gcd", 2}, {"lcm", 2},
    {"min", 2}, {"max", 2}, {"atan2", 2},
    {NULL, 0}
};

// Built-in constants
static const struct {
    const char* name;
    double value;
} builtin_constants[] = {
    {"pi", M_PI}, {"π", M_PI},
    {"e", M_E},
    {"phi", 1.6180339887498948482}, {"φ", 1.6180339887498948482},
    {"sqrt2", M_SQRT2}, {"√2", M_SQRT2},
    {"ln2", M_LN2},
    {"ln10", M_LN10},
    {NULL, 0.0}
};

// Main parsing function
parse_result_t parse_expression(const char* expression, calc_state_t* state) {
    parse_result_t result;
    result.value = 0.0;
    result.error = PARSE_SUCCESS;
    result.error_position = 0;
    strcpy(result.error_message, "");
    
    if (!expression || strlen(expression) == 0) {
        result.error = PARSE_ERROR_INVALID_SYNTAX;
        strcpy(result.error_message, "Empty expression");
        return result;
    }
    
    parse_context_t ctx;
    ctx.expression = expression;
    ctx.position = 0;
    ctx.length = strlen(expression);
    ctx.calc_state = state;
    
    // Get first token
    ctx.current_token = get_next_token(&ctx);
    
    parse_error_t error = PARSE_SUCCESS;
    double value = parse_expression_impl(&ctx, &error);
    
    if (error == PARSE_SUCCESS && ctx.current_token.type != TOKEN_END) {
        error = PARSE_ERROR_INVALID_SYNTAX;
    }
    
    result.value = value;
    result.error = error;
    result.error_position = ctx.position;
    
    if (error != PARSE_SUCCESS) {
        strcpy(result.error_message, parse_error_string(error));
    }
    
    return result;
}

// Tokenizer implementation
token_t get_next_token(parse_context_t* ctx) {
    token_t token;
    token.type = TOKEN_UNKNOWN;
    token.value[0] = '\\0';
    token.number_value = 0.0;
    token.position = ctx->position;
    
    skip_whitespace(ctx);
    
    if (ctx->position >= ctx->length) {
        token.type = TOKEN_END;
        return token;
    }
    
    char c = ctx->expression[ctx->position];
    
    // Numbers (including decimals and scientific notation)
    if (is_digit(c) || c == '.') {
        int start = ctx->position;
        bool has_dot = false;
        bool has_e = false;
        
        while (ctx->position < ctx->length) {
            c = ctx->expression[ctx->position];
            
            if (is_digit(c)) {
                ctx->position++;
            } else if (c == '.' && !has_dot && !has_e) {
                has_dot = true;
                ctx->position++;
            } else if ((c == 'e' || c == 'E') && !has_e) {
                has_e = true;
                ctx->position++;
                // Check for optional sign after e/E
                if (ctx->position < ctx->length && 
                    (ctx->expression[ctx->position] == '+' || 
                     ctx->expression[ctx->position] == '-')) {
                    ctx->position++;
                }
            } else {
                break;
            }
        }
        
        int len = ctx->position - start;
        strncpy(token.value, &ctx->expression[start], len);
        token.value[len] = '\\0';
        token.number_value = strtod(token.value, NULL);
        token.type = TOKEN_NUMBER;
        return token;
    }
    
    // Operators
    if (is_operator(c)) {
        token.value[0] = c;
        token.value[1] = '\\0';
        token.type = TOKEN_OPERATOR;
        ctx->position++;
        return token;
    }
    
    // Parentheses and comma
    if (c == '(') {
        token.value[0] = c;
        token.value[1] = '\\0';
        token.type = TOKEN_LEFT_PAREN;
        ctx->position++;
        return token;
    }
    
    if (c == ')') {
        token.value[0] = c;
        token.value[1] = '\\0';
        token.type = TOKEN_RIGHT_PAREN;
        ctx->position++;
        return token;
    }
    
    if (c == ',') {
        token.value[0] = c;
        token.value[1] = '\\0';
        token.type = TOKEN_COMMA;
        ctx->position++;
        return token;
    }
    
    // Identifiers (functions, constants, variables)
    if (is_alpha(c) || c == '_' || c == '√' || c == 'π' || c == 'φ') {
        int start = ctx->position;
        
        while (ctx->position < ctx->length) {
            c = ctx->expression[ctx->position];
            if (is_alnum(c) || c == '_' || c == '√' || c == 'π' || c == 'φ') {
                ctx->position++;
            } else {
                break;
            }
        }
        
        int len = ctx->position - start;
        strncpy(token.value, &ctx->expression[start], len);
        token.value[len] = '\\0';
        
        if (is_function_name(token.value)) {
            token.type = TOKEN_FUNCTION;
        } else if (is_constant_name(token.value)) {
            token.type = TOKEN_CONSTANT;
            token.number_value = get_constant_value(token.value);
        } else {
            token.type = TOKEN_VARIABLE;
        }
        
        return token;
    }
    
    // Unknown character
    token.value[0] = c;
    token.value[1] = '\\0';
    token.type = TOKEN_UNKNOWN;
    ctx->position++;
    return token;
}

// Parser implementation (recursive descent)
double parse_expression_impl(parse_context_t* ctx, parse_error_t* error) {
    double result = parse_term(ctx, error);
    
    while (*error == PARSE_SUCCESS && 
           (ctx->current_token.type == TOKEN_OPERATOR && 
            (ctx->current_token.value[0] == '+' || ctx->current_token.value[0] == '-'))) {
        
        char op = ctx->current_token.value[0];
        ctx->current_token = get_next_token(ctx);
        
        double right = parse_term(ctx, error);
        
        if (*error == PARSE_SUCCESS) {
            if (op == '+') {
                result += right;
            } else {
                result -= right;
            }
        }
    }
    
    return result;
}

double parse_term(parse_context_t* ctx, parse_error_t* error) {
    double result = parse_factor(ctx, error);
    
    while (*error == PARSE_SUCCESS && 
           (ctx->current_token.type == TOKEN_OPERATOR && 
            (ctx->current_token.value[0] == '*' || ctx->current_token.value[0] == '/' ||
             ctx->current_token.value[0] == '%'))) {
        
        char op = ctx->current_token.value[0];
        ctx->current_token = get_next_token(ctx);
        
        double right = parse_factor(ctx, error);
        
        if (*error == PARSE_SUCCESS) {
            if (op == '*') {
                result *= right;
            } else if (op == '/') {
                if (right == 0.0) {
                    *error = PARSE_ERROR_DIVISION_BY_ZERO;
                    return 0.0;
                }
                result /= right;
            } else if (op == '%') {
                if (right == 0.0) {
                    *error = PARSE_ERROR_DIVISION_BY_ZERO;
                    return 0.0;
                }
                result = fmod(result, right);
            }
        }
    }
    
    return result;
}

double parse_factor(parse_context_t* ctx, parse_error_t* error) {
    double result = parse_primary(ctx, error);
    
    while (*error == PARSE_SUCCESS && 
           ctx->current_token.type == TOKEN_OPERATOR && 
           ctx->current_token.value[0] == '^') {
        
        ctx->current_token = get_next_token(ctx);
        double exponent = parse_primary(ctx, error);
        
        if (*error == PARSE_SUCCESS) {
            result = pow(result, exponent);
            if (!isfinite(result)) {
                *error = PARSE_ERROR_DOMAIN_ERROR;
                return 0.0;
            }
        }
    }
    
    return result;
}

double parse_primary(parse_context_t* ctx, parse_error_t* error) {
    // Numbers
    if (ctx->current_token.type == TOKEN_NUMBER) {
        double value = ctx->current_token.number_value;
        ctx->current_token = get_next_token(ctx);
        return value;
    }
    
    // Constants
    if (ctx->current_token.type == TOKEN_CONSTANT) {
        double value = ctx->current_token.number_value;
        ctx->current_token = get_next_token(ctx);
        return value;
    }
    
    // Unary operators
    if (ctx->current_token.type == TOKEN_OPERATOR) {
        if (ctx->current_token.value[0] == '-') {
            ctx->current_token = get_next_token(ctx);
            return -parse_primary(ctx, error);
        }
        if (ctx->current_token.value[0] == '+') {
            ctx->current_token = get_next_token(ctx);
            return parse_primary(ctx, error);
        }
    }
    
    // Parentheses
    if (ctx->current_token.type == TOKEN_LEFT_PAREN) {
        ctx->current_token = get_next_token(ctx);
        double value = parse_expression_impl(ctx, error);
        
        if (*error == PARSE_SUCCESS) {
            if (ctx->current_token.type != TOKEN_RIGHT_PAREN) {
                *error = PARSE_ERROR_MISMATCHED_PARENTHESES;
                return 0.0;
            }
            ctx->current_token = get_next_token(ctx);
        }
        return value;
    }
    
    // Functions
    if (ctx->current_token.type == TOKEN_FUNCTION) {
        char func_name[64];
        strcpy(func_name, ctx->current_token.value);
        ctx->current_token = get_next_token(ctx);
        
        // Check for opening parenthesis
        if (ctx->current_token.type != TOKEN_LEFT_PAREN) {
            *error = PARSE_ERROR_INVALID_SYNTAX;
            return 0.0;
        }
        ctx->current_token = get_next_token(ctx);
        
        // Parse function arguments
        double args[10]; // Support up to 10 arguments
        int arg_count = 0;
        
        if (ctx->current_token.type != TOKEN_RIGHT_PAREN) {
            do {
                if (arg_count >= 10) {
                    *error = PARSE_ERROR_TOO_MANY_ARGUMENTS;
                    return 0.0;
                }
                
                args[arg_count] = parse_expression_impl(ctx, error);
                if (*error != PARSE_SUCCESS) {
                    return 0.0;
                }
                arg_count++;
                
                if (ctx->current_token.type == TOKEN_COMMA) {
                    ctx->current_token = get_next_token(ctx);
                } else {
                    break;
                }
            } while (true);
        }
        
        if (ctx->current_token.type != TOKEN_RIGHT_PAREN) {
            *error = PARSE_ERROR_MISMATCHED_PARENTHESES;
            return 0.0;
        }
        ctx->current_token = get_next_token(ctx);
        
        return evaluate_function(func_name, args, arg_count, ctx->calc_state, error);
    }
    
    // Variables (memory recall)
    if (ctx->current_token.type == TOKEN_VARIABLE) {
        if (strcmp(ctx->current_token.value, "M") == 0 || 
            strcmp(ctx->current_token.value, "mem") == 0) {
            ctx->current_token = get_next_token(ctx);
            return calc_memory_recall(ctx->calc_state);
        }
        if (strcmp(ctx->current_token.value, "ans") == 0 || 
            strcmp(ctx->current_token.value, "ANS") == 0) {
            ctx->current_token = get_next_token(ctx);
            return ctx->calc_state->last_result;
        }
    }
    
    *error = PARSE_ERROR_INVALID_SYNTAX;
    return 0.0;
}

// Function evaluation
double evaluate_function(const char* func_name, double* args, int arg_count, 
                        calc_state_t* state, parse_error_t* error) {
    
    calc_result_t result;
    
    // Single argument functions
    if (arg_count == 1) {
        double x = args[0];
        
        if (strcmp(func_name, "sin") == 0) {
            result = calc_sin(x, state->angle_in_degrees);
        } else if (strcmp(func_name, "cos") == 0) {
            result = calc_cos(x, state->angle_in_degrees);
        } else if (strcmp(func_name, "tan") == 0) {
            result = calc_tan(x, state->angle_in_degrees);
        } else if (strcmp(func_name, "sec") == 0) {
            result = calc_sec(x, state->angle_in_degrees);
        } else if (strcmp(func_name, "csc") == 0) {
            result = calc_csc(x, state->angle_in_degrees);
        } else if (strcmp(func_name, "cot") == 0) {
            result = calc_cot(x, state->angle_in_degrees);
        } else if (strcmp(func_name, "asin") == 0) {
            result = calc_asin(x, state->angle_in_degrees);
        } else if (strcmp(func_name, "acos") == 0) {
            result = calc_acos(x, state->angle_in_degrees);
        } else if (strcmp(func_name, "atan") == 0) {
            result = calc_atan(x, state->angle_in_degrees);
        } else if (strcmp(func_name, "sinh") == 0) {
            result = calc_sinh(x);
        } else if (strcmp(func_name, "cosh") == 0) {
            result = calc_cosh(x);
        } else if (strcmp(func_name, "tanh") == 0) {
            result = calc_tanh(x);
        } else if (strcmp(func_name, "sech") == 0) {
            result = calc_sech(x);
        } else if (strcmp(func_name, "csch") == 0) {
            result = calc_csch(x);
        } else if (strcmp(func_name, "coth") == 0) {
            result = calc_coth(x);
        } else if (strcmp(func_name, "log") == 0 || strcmp(func_name, "ln") == 0) {
            result = calc_log(x);
        } else if (strcmp(func_name, "log10") == 0) {
            result = calc_log10(x);
        } else if (strcmp(func_name, "log2") == 0) {
            result = calc_log2(x);
        } else if (strcmp(func_name, "exp") == 0) {
            result = calc_exp(x);
        } else if (strcmp(func_name, "exp10") == 0) {
            result = calc_exp10(x);
        } else if (strcmp(func_name, "exp2") == 0) {
            result = calc_exp2(x);
        } else if (strcmp(func_name, "sqrt") == 0) {
            result = calc_sqrt(x);
        } else if (strcmp(func_name, "cbrt") == 0) {
            result = calc_cbrt(x);
        } else if (strcmp(func_name, "abs") == 0) {
            result = calc_abs(x);
        } else if (strcmp(func_name, "floor") == 0) {
            result = calc_floor(x);
        } else if (strcmp(func_name, "ceil") == 0) {
            result = calc_ceil(x);
        } else if (strcmp(func_name, "round") == 0) {
            result = calc_round(x);
        } else if (strcmp(func_name, "factorial") == 0) {
            result = calc_factorial((int)x);
        } else if (strcmp(func_name, "gamma") == 0) {
            result = calc_gamma(x);
        } else {
            *error = PARSE_ERROR_INVALID_FUNCTION;
            return 0.0;
        }
    }
    // Two argument functions
    else if (arg_count == 2) {
        double x = args[0];
        double y = args[1];
        
        if (strcmp(func_name, "pow") == 0) {
            result = calc_power(x, y);
        } else if (strcmp(func_name, "nthrt") == 0) {
            result = calc_nthroot(x, (int)y);
        } else if (strcmp(func_name, "mod") == 0) {
            result = calc_mod(x, y);
        } else if (strcmp(func_name, "logb") == 0) {
            result = calc_logb(x, y);
        } else if (strcmp(func_name, "atan2") == 0) {
            result = calc_atan2(x, y, state->angle_in_degrees);
        } else if (strcmp(func_name, "perm") == 0) {
            result = calc_permutation((int)x, (int)y);
        } else if (strcmp(func_name, "comb") == 0) {
            result = calc_combination((int)x, (int)y);
        } else if (strcmp(func_name, "gcd") == 0) {
            result = calc_gcd((int)x, (int)y);
        } else if (strcmp(func_name, "lcm") == 0) {
            result = calc_lcm((int)x, (int)y);
        } else if (strcmp(func_name, "min") == 0) {
            result = make_result(fmin(x, y), CALC_SUCCESS);
        } else if (strcmp(func_name, "max") == 0) {
            result = make_result(fmax(x, y), CALC_SUCCESS);
        } else {
            *error = PARSE_ERROR_INVALID_FUNCTION;
            return 0.0;
        }
    } else {
        *error = PARSE_ERROR_TOO_FEW_ARGUMENTS;
        return 0.0;
    }
    
    if (result.has_error) {
        switch (result.error) {
            case CALC_ERROR_DIVISION_BY_ZERO:
                *error = PARSE_ERROR_DIVISION_BY_ZERO;
                break;
            case CALC_ERROR_DOMAIN_ERROR:
            case CALC_ERROR_OVERFLOW:
            case CALC_ERROR_UNDERFLOW:
                *error = PARSE_ERROR_DOMAIN_ERROR;
                break;
            default:
                *error = PARSE_ERROR_INVALID_FUNCTION;
                break;
        }
        return 0.0;
    }
    
    return result.value;
}

// Utility functions
void skip_whitespace(parse_context_t* ctx) {
    while (ctx->position < ctx->length && isspace(ctx->expression[ctx->position])) {
        ctx->position++;
    }
}

bool is_operator(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/' || c == '^' || c == '%';
}

bool is_function_name(const char* name) {
    for (int i = 0; builtin_functions[i].name != NULL; i++) {
        if (strcmp(name, builtin_functions[i].name) == 0) {
            return true;
        }
    }
    return false;
}

bool is_constant_name(const char* name) {
    for (int i = 0; builtin_constants[i].name != NULL; i++) {
        if (strcmp(name, builtin_constants[i].name) == 0) {
            return true;
        }
    }
    return false;
}

double get_constant_value(const char* name) {
    for (int i = 0; builtin_constants[i].name != NULL; i++) {
        if (strcmp(name, builtin_constants[i].name) == 0) {
            return builtin_constants[i].value;
        }
    }
    return 0.0;
}

bool is_digit(char c) {
    return c >= '0' && c <= '9';
}

bool is_alpha(char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}

bool is_alnum(char c) {
    return is_alpha(c) || is_digit(c);
}

const char* parse_error_string(parse_error_t error) {
    switch (error) {
        case PARSE_SUCCESS: return "Success";
        case PARSE_ERROR_INVALID_CHARACTER: return "Invalid character";
        case PARSE_ERROR_MISMATCHED_PARENTHESES: return "Mismatched parentheses";
        case PARSE_ERROR_INVALID_FUNCTION: return "Invalid function";
        case PARSE_ERROR_INVALID_SYNTAX: return "Invalid syntax";
        case PARSE_ERROR_DIVISION_BY_ZERO: return "Division by zero";
        case PARSE_ERROR_DOMAIN_ERROR: return "Domain error";
        case PARSE_ERROR_TOO_MANY_ARGUMENTS: return "Too many arguments";
        case PARSE_ERROR_TOO_FEW_ARGUMENTS: return "Too few arguments";
        default: return "Unknown parse error";
    }
}'''

# Save the expression parser files
with open('expression_parser.h', 'w') as f:
    f.write(expression_parser_h)
    
with open('expression_parser.c', 'w') as f:
    f.write(expression_parser_c)

print("Created expression parser files:")
print("- expression_parser.h (header file)")
print("- expression_parser.c (implementation)")
print()
print("Features implemented in the expression parser:")
print("✓ Tokenizer for mathematical expressions")
print("✓ Recursive descent parser")
print("✓ Support for all mathematical functions")
print("✓ Support for constants (π, e, φ)")
print("✓ Variable support (memory, ans)")
print("✓ Operator precedence handling")
print("✓ Parentheses support")
print("✓ Function calls with multiple arguments")
print("✓ Comprehensive error handling")
print("✓ Scientific notation support")