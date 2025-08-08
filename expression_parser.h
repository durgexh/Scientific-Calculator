#ifndef EXPRESSION_PARSER_H
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

#endif // EXPRESSION_PARSER_H