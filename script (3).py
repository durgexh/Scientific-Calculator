# Create Android integration files for the NDK
# This includes Java JNI interface and CMake build files

# Android MainActivity.java
android_main_activity = '''package com.advanced.scientificcalculator;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import android.content.SharedPreferences;
import android.view.Menu;
import android.view.MenuItem;

public class MainActivity extends AppCompatActivity {
    
    // Load native library
    static {
        System.loadLibrary("calculator");
    }
    
    private TextView displayExpression;
    private TextView displayResult;
    private TextView angleIndicator;
    private TextView memoryIndicator;
    
    private String currentExpression = "";
    private boolean isResultDisplayed = false;
    private boolean isDegreeMode = true;
    
    // Native method declarations
    public native String evaluateExpression(String expression, boolean degreeMode);
    public native void storeMemory(double value);
    public native void addMemory(double value);
    public native void subtractMemory(double value);
    public native double recallMemory();
    public native void clearMemory();
    public native String getLastError();
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        initViews();
        setupButtonListeners();
        loadSettings();
        updateDisplay();
    }
    
    private void initViews() {
        displayExpression = findViewById(R.id.display_expression);
        displayResult = findViewById(R.id.display_result);
        angleIndicator = findViewById(R.id.angle_indicator);
        memoryIndicator = findViewById(R.id.memory_indicator);
    }
    
    private void setupButtonListeners() {
        // Number buttons
        int[] numberButtons = {
            R.id.btn_0, R.id.btn_1, R.id.btn_2, R.id.btn_3, R.id.btn_4,
            R.id.btn_5, R.id.btn_6, R.id.btn_7, R.id.btn_8, R.id.btn_9
        };
        
        for (int i = 0; i < numberButtons.length; i++) {
            final int digit = i;
            findViewById(numberButtons[i]).setOnClickListener(v -> appendToExpression(String.valueOf(digit)));
        }
        
        // Operator buttons
        findViewById(R.id.btn_plus).setOnClickListener(v -> appendToExpression("+"));
        findViewById(R.id.btn_minus).setOnClickListener(v -> appendToExpression("-"));
        findViewById(R.id.btn_multiply).setOnClickListener(v -> appendToExpression("*"));
        findViewById(R.id.btn_divide).setOnClickListener(v -> appendToExpression("/"));
        findViewById(R.id.btn_power).setOnClickListener(v -> appendToExpression("^"));
        findViewById(R.id.btn_mod).setOnClickListener(v -> appendToExpression("mod("));
        
        // Function buttons
        findViewById(R.id.btn_sin).setOnClickListener(v -> appendToExpression("sin("));
        findViewById(R.id.btn_cos).setOnClickListener(v -> appendToExpression("cos("));
        findViewById(R.id.btn_tan).setOnClickListener(v -> appendToExpression("tan("));
        findViewById(R.id.btn_log).setOnClickListener(v -> appendToExpression("log("));
        findViewById(R.id.btn_ln).setOnClickListener(v -> appendToExpression("ln("));
        findViewById(R.id.btn_sqrt).setOnClickListener(v -> appendToExpression("sqrt("));
        findViewById(R.id.btn_factorial).setOnClickListener(v -> appendToExpression("factorial("));
        
        // Advanced functions
        findViewById(R.id.btn_asin).setOnClickListener(v -> appendToExpression("asin("));
        findViewById(R.id.btn_acos).setOnClickListener(v -> appendToExpression("acos("));
        findViewById(R.id.btn_atan).setOnClickListener(v -> appendToExpression("atan("));
        findViewById(R.id.btn_sinh).setOnClickListener(v -> appendToExpression("sinh("));
        findViewById(R.id.btn_cosh).setOnClickListener(v -> appendToExpression("cosh("));
        findViewById(R.id.btn_tanh).setOnClickListener(v -> appendToExpression("tanh("));
        
        // Constants
        findViewById(R.id.btn_pi).setOnClickListener(v -> appendToExpression("π"));
        findViewById(R.id.btn_e).setOnClickListener(v -> appendToExpression("e"));
        findViewById(R.id.btn_phi).setOnClickListener(v -> appendToExpression("φ"));
        
        // Parentheses
        findViewById(R.id.btn_left_paren).setOnClickListener(v -> appendToExpression("("));
        findViewById(R.id.btn_right_paren).setOnClickListener(v -> appendToExpression(")"));
        
        // Special buttons
        findViewById(R.id.btn_decimal).setOnClickListener(v -> appendToExpression("."));
        findViewById(R.id.btn_equals).setOnClickListener(v -> calculateResult());
        findViewById(R.id.btn_clear).setOnClickListener(v -> clearAll());
        findViewById(R.id.btn_clear_entry).setOnClickListener(v -> clearEntry());
        findViewById(R.id.btn_backspace).setOnClickListener(v -> backspace());
        
        // Memory buttons
        findViewById(R.id.btn_memory_store).setOnClickListener(v -> memoryStore());
        findViewById(R.id.btn_memory_add).setOnClickListener(v -> memoryAdd());
        findViewById(R.id.btn_memory_subtract).setOnClickListener(v -> memorySubtract());
        findViewById(R.id.btn_memory_recall).setOnClickListener(v -> memoryRecall());
        findViewById(R.id.btn_memory_clear).setOnClickListener(v -> memoryClear());
        
        // Angle mode toggle
        findViewById(R.id.btn_angle_mode).setOnClickListener(v -> toggleAngleMode());
    }
    
    private void appendToExpression(String value) {
        if (isResultDisplayed && !isOperator(value) && !value.equals("(")) {
            currentExpression = value;
            isResultDisplayed = false;
        } else {
            currentExpression += value;
            isResultDisplayed = false;
        }
        updateDisplay();
    }
    
    private boolean isOperator(String value) {
        return value.equals("+") || value.equals("-") || value.equals("*") || 
               value.equals("/") || value.equals("^") || value.equals("mod(");
    }
    
    private void calculateResult() {
        if (currentExpression.isEmpty()) {
            return;
        }
        
        try {
            String result = evaluateExpression(currentExpression, isDegreeMode);
            
            if (result.startsWith("ERROR:")) {
                showError(result.substring(6));
                return;
            }
            
            displayResult.setText(result);
            isResultDisplayed = true;
            
        } catch (Exception e) {
            showError("Calculation error: " + e.getMessage());
        }
    }
    
    private void clearAll() {
        currentExpression = "";
        isResultDisplayed = false;
        updateDisplay();
    }
    
    private void clearEntry() {
        if (!currentExpression.isEmpty()) {
            // Find last number or function and remove it
            String[] parts = currentExpression.split("(?=[+\\-*/^()])|(?<=[+\\-*/^()])");
            if (parts.length > 0) {
                currentExpression = currentExpression.substring(0, 
                    currentExpression.length() - parts[parts.length - 1].length());
            }
        }
        updateDisplay();
    }
    
    private void backspace() {
        if (!currentExpression.isEmpty()) {
            currentExpression = currentExpression.substring(0, currentExpression.length() - 1);
            updateDisplay();
        }
    }
    
    private void memoryStore() {
        try {
            double value = Double.parseDouble(displayResult.getText().toString());
            storeMemory(value);
            memoryIndicator.setVisibility(View.VISIBLE);
            Toast.makeText(this, "Value stored to memory", Toast.LENGTH_SHORT).show();
        } catch (NumberFormatException e) {
            showError("Invalid number for memory operation");
        }
    }
    
    private void memoryAdd() {
        try {
            double value = Double.parseDouble(displayResult.getText().toString());
            addMemory(value);
            Toast.makeText(this, "Value added to memory", Toast.LENGTH_SHORT).show();
        } catch (NumberFormatException e) {
            showError("Invalid number for memory operation");
        }
    }
    
    private void memorySubtract() {
        try {
            double value = Double.parseDouble(displayResult.getText().toString());
            subtractMemory(value);
            Toast.makeText(this, "Value subtracted from memory", Toast.LENGTH_SHORT).show();
        } catch (NumberFormatException e) {
            showError("Invalid number for memory operation");
        }
    }
    
    private void memoryRecall() {
        double value = recallMemory();
        currentExpression += String.valueOf(value);
        updateDisplay();
    }
    
    private void memoryClear() {
        clearMemory();
        memoryIndicator.setVisibility(View.GONE);
        Toast.makeText(this, "Memory cleared", Toast.LENGTH_SHORT).show();
    }
    
    private void toggleAngleMode() {
        isDegreeMode = !isDegreeMode;
        angleIndicator.setText(isDegreeMode ? "DEG" : "RAD");
        saveSettings();
        Toast.makeText(this, isDegreeMode ? "Degree mode" : "Radian mode", Toast.LENGTH_SHORT).show();
    }
    
    private void updateDisplay() {
        displayExpression.setText(currentExpression.isEmpty() ? "0" : currentExpression);
        
        if (!isResultDisplayed) {
            displayResult.setText("0");
        }
    }
    
    private void showError(String message) {
        displayResult.setText("Error");
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }
    
    private void loadSettings() {
        SharedPreferences prefs = getSharedPreferences("CalculatorPrefs", MODE_PRIVATE);
        isDegreeMode = prefs.getBoolean("isDegreeMode", true);
        angleIndicator.setText(isDegreeMode ? "DEG" : "RAD");
    }
    
    private void saveSettings() {
        SharedPreferences prefs = getSharedPreferences("CalculatorPrefs", MODE_PRIVATE);
        prefs.edit().putBoolean("isDegreeMode", isDegreeMode).apply();
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }
    
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        
        if (id == R.id.action_history) {
            // Open history activity
            return true;
        } else if (id == R.id.action_settings) {
            // Open settings activity
            return true;
        } else if (id == R.id.action_about) {
            // Show about dialog
            return true;
        }
        
        return super.onOptionsItemSelected(item);
    }
}'''

# JNI Native bridge implementation
jni_bridge_c = '''#include <jni.h>
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
}'''

# CMakeLists.txt for building the native library
cmake_lists = '''cmake_minimum_required(VERSION 3.18.1)

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
)'''

# Application.mk for NDK build configuration
application_mk = '''APP_ABI := arm64-v8a armeabi-v7a x86_64 x86
APP_PLATFORM := android-21
APP_STL := c++_shared
APP_CPPFLAGS := -std=c++17 -fexceptions -frtti
APP_OPTIM := release
APP_STRIP_MODE := --strip-unneeded'''

# Android.mk for alternative build system
android_mk = '''LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := calculator
LOCAL_SRC_FILES := \\
    jni_bridge.c \\
    calculator_engine.c \\
    expression_parser.c \\
    math_functions.c \\
    complex_numbers.c \\
    matrix_operations.c \\
    statistics.c \\
    unit_converter.c

LOCAL_C_INCLUDES := $(LOCAL_PATH)
LOCAL_CFLAGS := -Wall -Wextra -O2 -ffast-math -DANDROID
LOCAL_LDLIBS := -llog -lm

include $(BUILD_SHARED_LIBRARY)'''

# Save all Android files
with open('MainActivity.java', 'w') as f:
    f.write(android_main_activity)

with open('jni_bridge.c', 'w') as f:
    f.write(jni_bridge_c)
    
with open('CMakeLists.txt', 'w') as f:
    f.write(cmake_lists)
    
with open('Application.mk', 'w') as f:
    f.write(application_mk)
    
with open('Android.mk', 'w') as f:
    f.write(android_mk)

print("Created Android integration files:")
print("- MainActivity.java (Android UI activity)")  
print("- jni_bridge.c (JNI native interface)")
print("- CMakeLists.txt (CMake build configuration)")
print("- Application.mk (NDK application config)")
print("- Android.mk (Alternative build config)")
print()
print("Android integration features:")
print("✓ JNI bridge for C library integration")
print("✓ Memory management for calculator state")
print("✓ Error handling and logging")
print("✓ All mathematical functions exposed to Java")
print("✓ Memory operations (store, recall, clear)")
print("✓ Angle mode switching (degrees/radians)")
print("✓ Settings persistence")
print("✓ Multi-architecture support (ARM64, ARM, x86_64, x86)")