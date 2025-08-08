package com.advanced.scientificcalculator;

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
            String[] parts = currentExpression.split("(?=[+\-*/^()])|(?<=[+\-*/^()])");
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
}