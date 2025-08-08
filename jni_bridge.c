#include <jni.h>
#include <string.h>
#include <android/log.h>
#include "calculator_engine.h"

#define LOG_TAG "CalculatorNative"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)

// Global calculator state
static calc_state_t* g_calc_state = NULL;

// Initialize calculator state
JNIEXPORT void JNICALL
Java_com_advanced_scientificcalculator_MainActivity_initCalculator(JNIEnv *env, jobject thiz) {
    if (g_calc_state == NULL) {
        g_calc_state = calc_create_state();
        if (g_calc_state == NULL) {
            LOGE("Failed to create calculator state");
        } else {
            LOGI("Calculator state initialized");
        }
    }
}

// Cleanup calculator state
JNIEXPORT void JNICALL
Java_com_advanced_scientificcalculator_MainActivity_destroyCalculator(JNIEnv *env, jobject thiz) {
    if (g_calc_state != NULL) {
        calc_destroy_state(g_calc_state);
        g_calc_state = NULL;
        LOGI("Calculator state destroyed");
    }
}

// Evaluate mathematical expression
JNIEXPORT jstring JNICALL
Java_com_advanced_scientificcalculator_MainActivity_evaluateExpression(JNIEnv *env, jobject thiz, 
                                                                        jstring expression, 
                                                                        jboolean degree_mode) {
    if (g_calc_state == NULL) {
        Java_com_advanced_scientificcalculator_MainActivity_initCalculator(env, thiz);
    }

    // Get C string from Java string
    const char *expr_str = (*env)->GetStringUTFChars(env, expression, NULL);
    if (expr_str == NULL) {
        return (*env)->NewStringUTF(env, "ERROR: Invalid expression");
    }

    // Set angle mode
    g_calc_state->angle_in_degrees = degree_mode;

    // Evaluate expression
    calc_result_t result = calc_evaluate(expr_str, g_calc_state);

    // Release the string
    (*env)->ReleaseStringUTFChars(env, expression, expr_str);

    // Prepare result string
    char result_str[256];

    if (result.has_error) {
        snprintf(result_str, sizeof(result_str), "ERROR: %s", 
                calc_error_string(result.error));
        LOGE("Calculation error: %s", calc_error_string(result.error));
    } else {
        // Format result with appropriate precision
        if (result.value == (long long)result.value && fabs(result.value) < 1e15) {
            // Integer result
            snprintf(result_str, sizeof(result_str), "%.0f", result.value);
        } else if (fabs(result.value) >= 1e10 || (fabs(result.value) < 1e-4 && result.value != 0)) {
            // Scientific notation
            snprintf(result_str, sizeof(result_str), "%.10e", result.value);
        } else {
            // Regular decimal
            snprintf(result_str, sizeof(result_str), "%.10g", result.value);
        }

        LOGI("Calculation result: %s = %s", expr_str, result_str);
    }

    return (*env)->NewStringUTF(env, result_str);
}

// Memory operations
JNIEXPORT void JNICALL
Java_com_advanced_scientificcalculator_MainActivity_storeMemory(JNIEnv *env, jobject thiz, 
                                                                jdouble value) {
    if (g_calc_state != NULL) {
        calc_memory_store(g_calc_state, value);
        LOGI("Memory stored: %f", value);
    }
}

JNIEXPORT void JNICALL
Java_com_advanced_scientificcalculator_MainActivity_addMemory(JNIEnv *env, jobject thiz, 
                                                              jdouble value) {
    if (g_calc_state != NULL) {
        calc_memory_add(g_calc_state, value);
        LOGI("Memory added: %f", value);
    }
}

JNIEXPORT void JNICALL
Java_com_advanced_scientificcalculator_MainActivity_subtractMemory(JNIEnv *env, jobject thiz, 
                                                                   jdouble value) {
    if (g_calc_state != NULL) {
        calc_memory_subtract(g_calc_state, value);
        LOGI("Memory subtracted: %f", value);
    }
}

JNIEXPORT jdouble JNICALL
Java_com_advanced_scientificcalculator_MainActivity_recallMemory(JNIEnv *env, jobject thiz) {
    if (g_calc_state != NULL) {
        double value = calc_memory_recall(g_calc_state);
        LOGI("Memory recalled: %f", value);
        return value;
    }
    return 0.0;
}

JNIEXPORT void JNICALL
Java_com_advanced_scientificcalculator_MainActivity_clearMemory(JNIEnv *env, jobject thiz) {
    if (g_calc_state != NULL) {
        calc_memory_clear(g_calc_state);
        LOGI("Memory cleared");
    }
}

// Get last error message
JNIEXPORT jstring JNICALL
Java_com_advanced_scientificcalculator_MainActivity_getLastError(JNIEnv *env, jobject thiz) {
    // This could be expanded to track more detailed error information
    return (*env)->NewStringUTF(env, "No error");
}

// JNI_OnLoad - called when library is loaded
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* vm, void* reserved) {
    LOGI("Calculator native library loaded");
    return JNI_VERSION_1_6;
}

// JNI_OnUnload - called when library is unloaded
JNIEXPORT void JNICALL JNI_OnUnload(JavaVM* vm, void* reserved) {
    if (g_calc_state != NULL) {
        calc_destroy_state(g_calc_state);
        g_calc_state = NULL;
    }
    LOGI("Calculator native library unloaded");
}