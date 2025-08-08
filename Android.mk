LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := calculator
LOCAL_SRC_FILES := \
    jni_bridge.c \
    calculator_engine.c \
    expression_parser.c \
    math_functions.c \
    complex_numbers.c \
    matrix_operations.c \
    statistics.c \
    unit_converter.c

LOCAL_C_INCLUDES := $(LOCAL_PATH)
LOCAL_CFLAGS := -Wall -Wextra -O2 -ffast-math -DANDROID
LOCAL_LDLIBS := -llog -lm

include $(BUILD_SHARED_LIBRARY)