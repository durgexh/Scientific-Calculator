cmake_minimum_required(VERSION 3.18.1)

project("calculator")

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Find required packages
find_library(log-lib log)
find_library(m-lib m)

# Add source files
add_library(
    calculator
    SHARED

    # JNI bridge
    jni_bridge.c

    # Core calculator engine
    calculator_engine.c
    expression_parser.c
    math_functions.c
    complex_numbers.c
    matrix_operations.c
    statistics.c
    unit_converter.c
)

# Include directories
target_include_directories(
    calculator 
    PRIVATE 
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Compiler flags
target_compile_options(
    calculator 
    PRIVATE 
    -Wall 
    -Wextra 
    -O2
    -ffast-math
    -DANDROID
)

# Link libraries
target_link_libraries(
    calculator
    ${log-lib}
    ${m-lib}
)

# Set properties
set_target_properties(
    calculator 
    PROPERTIES
    ANDROID_ARM_MODE arm
)