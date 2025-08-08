class AdvancedCalculator {
    constructor() {
        this.expression = '';
        this.result = '0';
        this.history = [];
        this.memory = 0;
        this.angleUnit = 'deg'; // 'deg' or 'rad'
        this.currentTab = 'basic';
        this.isResultDisplayed = false;
        
        this.constants = {
            π: Math.PI,
            e: Math.E,
            φ: (1 + Math.sqrt(5)) / 2
        };
        
        this.unitConversions = {
            length: {
                meters: 1,
                feet: 3.28084,
                inches: 39.3701,
                centimeters: 100,
                kilometers: 0.001,
                miles: 0.000621371
            },
            temperature: {
                celsius: 'base',
                fahrenheit: 'C * 9/5 + 32',
                kelvin: 'C + 273.15'
            },
            mass: {
                kilograms: 1,
                pounds: 2.20462,
                grams: 1000,
                ounces: 35.274
            }
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupTabSwitching();
        this.setupConverter();
        this.setupMatrix();
        this.updateDisplay();
        this.loadTheme();
    }
    
    setupEventListeners() {
        // Basic calculator buttons
        document.querySelectorAll('[data-action]').forEach(button => {
            button.addEventListener('click', (e) => {
                this.handleButtonClick(e.target);
            });
        });
        
        // Theme toggle
        document.getElementById('themeToggle').addEventListener('click', () => {
            this.toggleTheme();
        });
        
        // History toggle
        document.getElementById('historyToggle').addEventListener('click', () => {
            this.toggleHistory();
        });
        
        // Angle unit toggle
        document.getElementById('angleToggle').addEventListener('click', () => {
            this.toggleAngleUnit();
        });
        
        // History clear
        document.getElementById('clearHistory').addEventListener('click', () => {
            this.clearHistory();
        });
        
        // Keyboard support
        document.addEventListener('keydown', (e) => {
            this.handleKeyboard(e);
        });
        
        // Display click for copy
        document.getElementById('result').addEventListener('click', () => {
            this.copyResult();
        });
        
        // Unit conversion
        document.getElementById('fromValue').addEventListener('input', () => {
            this.performConversion();
        });
        
        document.getElementById('fromUnit').addEventListener('change', () => {
            this.performConversion();
        });
        
        document.getElementById('toUnit').addEventListener('change', () => {
            this.performConversion();
        });
        
        document.getElementById('conversionType').addEventListener('change', () => {
            this.updateUnitOptions();
        });
        
        // Statistics calculator
        document.getElementById('calculateStats').addEventListener('click', () => {
            this.calculateStatistics();
        });
        
        // Matrix calculator
        document.getElementById('matrixSize').addEventListener('change', () => {
            this.generateMatrixInputs();
        });
        
        document.querySelectorAll('[data-matrix-op]').forEach(button => {
            button.addEventListener('click', (e) => {
                this.performMatrixOperation(e.target.dataset.matrixOp);
            });
        });
    }
    
    setupTabSwitching() {
        document.querySelectorAll('.tab-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                const tabName = e.target.dataset.tab;
                this.switchTab(tabName);
            });
        });
    }
    
    switchTab(tabName) {
        // Remove active class from all tabs and content
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        // Add active class to selected tab and content
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');
        
        this.currentTab = tabName;
    }
    
    handleButtonClick(button) {
        const action = button.dataset.action;
        const value = button.dataset.value;
        
        // Add visual feedback
        button.classList.add('pressed');
        setTimeout(() => button.classList.remove('pressed'), 100);
        
        switch (action) {
            case 'number':
                this.inputNumber(value);
                break;
            case 'operator':
                this.inputOperator(value);
                break;
            case 'decimal':
                this.inputDecimal();
                break;
            case 'equals':
                this.calculate();
                break;
            case 'clear':
                this.clear();
                break;
            case 'clearEntry':
                this.clearEntry();
                break;
            case 'backspace':
                this.backspace();
                break;
            case 'function':
                this.inputFunction(value);
                break;
            case 'constant':
                this.inputConstant(value);
                break;
            case 'bracket':
                this.inputBracket(value);
                break;
            case 'memory':
                this.handleMemory(value);
                break;
        }
    }
    
    inputNumber(num) {
        if (this.isResultDisplayed) {
            this.expression = '';
            this.isResultDisplayed = false;
        }
        this.expression += num;
        this.updateDisplay();
    }
    
    inputOperator(op) {
        if (this.isResultDisplayed) {
            this.expression = this.result;
            this.isResultDisplayed = false;
        }
        
        // Handle special operators
        if (op === '^2') {
            this.expression += '^2';
        } else if (op === '^3') {
            this.expression += '^3';
        } else {
            this.expression += op;
        }
        
        this.updateDisplay();
    }
    
    inputDecimal() {
        if (this.isResultDisplayed) {
            this.expression = '0';
            this.isResultDisplayed = false;
        }
        
        // Check if current number already has decimal
        const parts = this.expression.split(/[\+\-\*\/]/);
        const currentNumber = parts[parts.length - 1];
        
        if (!currentNumber.includes('.')) {
            this.expression += '.';
        }
        
        this.updateDisplay();
    }
    
    inputFunction(func) {
        if (this.isResultDisplayed) {
            this.expression = '';
            this.isResultDisplayed = false;
        }
        
        this.expression += func + '(';
        this.updateDisplay();
    }
    
    inputConstant(constant) {
        if (this.isResultDisplayed) {
            this.expression = '';
            this.isResultDisplayed = false;
        }
        
        this.expression += constant;
        this.updateDisplay();
    }
    
    inputBracket(bracket) {
        if (this.isResultDisplayed) {
            this.expression = '';
            this.isResultDisplayed = false;
        }
        
        this.expression += bracket;
        this.updateDisplay();
    }
    
    calculate() {
        try {
            const result = this.evaluateExpression(this.expression);
            
            if (isNaN(result) || !isFinite(result)) {
                throw new Error('Invalid calculation');
            }
            
            this.result = this.formatNumber(result);
            this.addToHistory(this.expression, this.result);
            this.isResultDisplayed = true;
            this.updateDisplay();
        } catch (error) {
            this.result = 'Error';
            this.updateDisplay();
            this.showError('Invalid expression');
        }
    }
    
    evaluateExpression(expr) {
        try {
            // Replace constants first
            expr = expr.replace(/π/g, Math.PI.toString());
            expr = expr.replace(/e(?![a-z])/g, Math.E.toString());
            expr = expr.replace(/φ/g, ((1 + Math.sqrt(5)) / 2).toString());
            
            // Replace display operators
            expr = expr.replace(/×/g, '*');
            expr = expr.replace(/÷/g, '/');
            expr = expr.replace(/−/g, '-');
            
            // Handle power operations
            expr = expr.replace(/\^2/g, '**2');
            expr = expr.replace(/\^3/g, '**3');
            expr = expr.replace(/\^/g, '**');
            
            // Handle mathematical functions
            expr = this.replaceMathFunctions(expr);
            
            // Use Function constructor for safe evaluation
            const result = Function(`"use strict"; return (${expr})`)();
            return result;
        } catch (error) {
            throw new Error('Invalid expression');
        }
    }
    
    replaceMathFunctions(expr) {
        const mathFunctions = {
            'sin': (x) => Math.sin(this.toRadians(x)),
            'cos': (x) => Math.cos(this.toRadians(x)),
            'tan': (x) => Math.tan(this.toRadians(x)),
            'asin': (x) => this.fromRadians(Math.asin(x)),
            'acos': (x) => this.fromRadians(Math.acos(x)),
            'atan': (x) => this.fromRadians(Math.atan(x)),
            'sinh': (x) => Math.sinh(x),
            'cosh': (x) => Math.cosh(x),
            'tanh': (x) => Math.tanh(x),
            'log': (x) => Math.log10(x),
            'ln': (x) => Math.log(x),
            'exp': (x) => Math.exp(x),
            'sqrt': (x) => Math.sqrt(x),
            'cbrt': (x) => Math.cbrt(x),
            'factorial': (x) => this.factorial(Math.floor(x))
        };
        
        // Process functions from longest to shortest to avoid conflicts
        const sortedFunctions = Object.keys(mathFunctions).sort((a, b) => b.length - a.length);
        
        for (const funcName of sortedFunctions) {
            const func = mathFunctions[funcName];
            // Match function calls like sin(30) or sqrt(16)
            const regex = new RegExp(`\\b${funcName}\\(([^()]+)\\)`, 'g');
            
            expr = expr.replace(regex, (match, args) => {
                try {
                    // Recursively evaluate the argument
                    const argValue = this.evaluateExpression(args);
                    const result = func(argValue);
                    return result.toString();
                } catch (e) {
                    throw new Error(`Error in function ${funcName}`);
                }
            });
        }
        
        return expr;
    }
    
    factorial(n) {
        if (n < 0 || n !== Math.floor(n)) return NaN;
        if (n === 0 || n === 1) return 1;
        if (n > 170) return Infinity; // Prevent overflow
        let result = 1;
        for (let i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }
    
    toRadians(degrees) {
        return this.angleUnit === 'deg' ? degrees * Math.PI / 180 : degrees;
    }
    
    fromRadians(radians) {
        return this.angleUnit === 'deg' ? radians * 180 / Math.PI : radians;
    }
    
    formatNumber(num) {
        if (Math.abs(num) > 1e10 || (Math.abs(num) < 1e-6 && num !== 0)) {
            return num.toExponential(6);
        }
        return parseFloat(num.toFixed(10)).toString();
    }
    
    clear() {
        this.expression = '';
        this.result = '0';
        this.isResultDisplayed = false;
        this.updateDisplay();
    }
    
    clearEntry() {
        this.expression = '';
        this.updateDisplay();
    }
    
    backspace() {
        if (!this.isResultDisplayed) {
            this.expression = this.expression.slice(0, -1);
            this.updateDisplay();
        }
    }
    
    handleMemory(action) {
        switch (action) {
            case 'MS':
                this.memory = parseFloat(this.result) || 0;
                this.showMemoryIndicator();
                break;
            case 'MR':
                this.expression = this.memory.toString();
                this.updateDisplay();
                break;
            case 'M+':
                this.memory += parseFloat(this.result) || 0;
                this.showMemoryIndicator();
                break;
            case 'M-':
                this.memory -= parseFloat(this.result) || 0;
                this.showMemoryIndicator();
                break;
            case 'MC':
                this.memory = 0;
                this.hideMemoryIndicator();
                break;
        }
    }
    
    showMemoryIndicator() {
        document.getElementById('memoryIndicator').classList.remove('hidden');
    }
    
    hideMemoryIndicator() {
        document.getElementById('memoryIndicator').classList.add('hidden');
    }
    
    toggleAngleUnit() {
        this.angleUnit = this.angleUnit === 'deg' ? 'rad' : 'deg';
        const button = document.getElementById('angleToggle');
        const indicator = document.getElementById('angleUnit');
        
        button.textContent = this.angleUnit === 'deg' ? 'RAD' : 'DEG';
        indicator.textContent = this.angleUnit.toUpperCase();
    }
    
    updateDisplay() {
        document.getElementById('expression').textContent = this.expression || '0';
        document.getElementById('result').textContent = this.result;
    }
    
    addToHistory(expression, result) {
        const historyItem = { expression, result, timestamp: Date.now() };
        this.history.unshift(historyItem);
        
        // Limit history to 50 items
        if (this.history.length > 50) {
            this.history = this.history.slice(0, 50);
        }
        
        this.updateHistoryDisplay();
    }
    
    updateHistoryDisplay() {
        const historyList = document.getElementById('historyList');
        historyList.innerHTML = '';
        
        this.history.forEach((item, index) => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.innerHTML = `
                <div class="history-expression">${item.expression}</div>
                <div class="history-result">${item.result}</div>
            `;
            
            historyItem.addEventListener('click', () => {
                this.expression = item.result;
                this.isResultDisplayed = true;
                this.updateDisplay();
                this.toggleHistory();
            });
            
            historyList.appendChild(historyItem);
        });
    }
    
    toggleHistory() {
        const panel = document.getElementById('historyPanel');
        panel.classList.toggle('active');
        panel.classList.toggle('hidden');
    }
    
    clearHistory() {
        this.history = [];
        this.updateHistoryDisplay();
    }
    
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-color-scheme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-color-scheme', newTheme);
        
        const themeButton = document.getElementById('themeToggle');
        themeButton.textContent = newTheme === 'dark' ? '☀️' : '🌙';
        
        localStorage.setItem('calculator-theme', newTheme);
    }
    
    loadTheme() {
        const savedTheme = localStorage.getItem('calculator-theme') || 'light';
        document.documentElement.setAttribute('data-color-scheme', savedTheme);
        
        const themeButton = document.getElementById('themeToggle');
        themeButton.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
    }
    
    copyResult() {
        navigator.clipboard.writeText(this.result).then(() => {
            this.showCopyFeedback();
        }).catch(() => {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = this.result;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showCopyFeedback();
        });
    }
    
    showCopyFeedback() {
        const feedback = document.createElement('div');
        feedback.className = 'copy-feedback';
        feedback.textContent = 'Copied!';
        document.querySelector('.display-section').appendChild(feedback);
        
        setTimeout(() => {
            feedback.remove();
        }, 1500);
    }
    
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        document.querySelector('.display-section').appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 3000);
    }
    
    handleKeyboard(e) {
        const keyMap = {
            '0': () => this.inputNumber('0'),
            '1': () => this.inputNumber('1'),
            '2': () => this.inputNumber('2'),
            '3': () => this.inputNumber('3'),
            '4': () => this.inputNumber('4'),
            '5': () => this.inputNumber('5'),
            '6': () => this.inputNumber('6'),
            '7': () => this.inputNumber('7'),
            '8': () => this.inputNumber('8'),
            '9': () => this.inputNumber('9'),
            '.': () => this.inputDecimal(),
            '+': () => this.inputOperator('+'),
            '-': () => this.inputOperator('-'),
            '*': () => this.inputOperator('*'),
            '/': () => this.inputOperator('/'),
            '^': () => this.inputOperator('^'),
            '(': () => this.inputBracket('('),
            ')': () => this.inputBracket(')'),
            'Enter': () => this.calculate(),
            '=': () => this.calculate(),
            'Escape': () => this.clear(),
            'Backspace': () => this.backspace(),
            'Delete': () => this.clearEntry()
        };
        
        if (keyMap[e.key]) {
            e.preventDefault();
            keyMap[e.key]();
        }
    }
    
    // Unit Converter Functions
    setupConverter() {
        this.updateUnitOptions();
        this.generateMatrixInputs();
    }
    
    updateUnitOptions() {
        const type = document.getElementById('conversionType').value;
        const fromUnit = document.getElementById('fromUnit');
        const toUnit = document.getElementById('toUnit');
        
        fromUnit.innerHTML = '';
        toUnit.innerHTML = '';
        
        const units = Object.keys(this.unitConversions[type]);
        units.forEach(unit => {
            fromUnit.appendChild(new Option(unit.charAt(0).toUpperCase() + unit.slice(1), unit));
            toUnit.appendChild(new Option(unit.charAt(0).toUpperCase() + unit.slice(1), unit));
        });
        
        // Set different default values
        if (units.length > 1) {
            toUnit.selectedIndex = 1;
        }
        
        // Clear values when type changes
        document.getElementById('fromValue').value = '';
        document.getElementById('toValue').value = '';
    }
    
    performConversion() {
        const type = document.getElementById('conversionType').value;
        const fromValue = parseFloat(document.getElementById('fromValue').value);
        const fromUnit = document.getElementById('fromUnit').value;
        const toUnit = document.getElementById('toUnit').value;
        
        if (isNaN(fromValue) || fromValue === '') {
            document.getElementById('toValue').value = '';
            return;
        }
        
        let result;
        
        if (type === 'temperature') {
            result = this.convertTemperature(fromValue, fromUnit, toUnit);
        } else {
            const conversions = this.unitConversions[type];
            const baseValue = fromValue / conversions[fromUnit];
            result = baseValue * conversions[toUnit];
        }
        
        document.getElementById('toValue').value = this.formatNumber(result);
    }
    
    convertTemperature(value, from, to) {
        // Convert to Celsius first
        let celsius;
        switch (from) {
            case 'celsius':
                celsius = value;
                break;
            case 'fahrenheit':
                celsius = (value - 32) * 5/9;
                break;
            case 'kelvin':
                celsius = value - 273.15;
                break;
        }
        
        // Convert from Celsius to target
        switch (to) {
            case 'celsius':
                return celsius;
            case 'fahrenheit':
                return celsius * 9/5 + 32;
            case 'kelvin':
                return celsius + 273.15;
        }
    }
    
    // Matrix Calculator Functions
    generateMatrixInputs() {
        const size = parseInt(document.getElementById('matrixSize').value);
        const container = document.getElementById('matrixInputs');
        
        container.innerHTML = '';
        container.className = `matrix-inputs matrix-${size}x${size}`;
        
        for (let i = 0; i < size * size; i++) {
            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'form-control';
            input.placeholder = '0';
            input.value = '0';
            container.appendChild(input);
        }
    }
    
    getMatrixValues() {
        const size = parseInt(document.getElementById('matrixSize').value);
        const inputs = document.querySelectorAll('#matrixInputs input');
        const matrix = [];
        
        for (let i = 0; i < size; i++) {
            matrix[i] = [];
            for (let j = 0; j < size; j++) {
                matrix[i][j] = parseFloat(inputs[i * size + j].value) || 0;
            }
        }
        
        return matrix;
    }
    
    performMatrixOperation(operation) {
        const matrix = this.getMatrixValues();
        const resultDiv = document.getElementById('matrixResult');
        
        try {
            let result;
            switch (operation) {
                case 'determinant':
                    result = `Determinant: ${this.formatNumber(this.calculateDeterminant(matrix))}`;
                    break;
                case 'transpose':
                    result = this.formatMatrix(this.transposeMatrix(matrix));
                    break;
                case 'inverse':
                    const inverse = this.inverseMatrix(matrix);
                    result = inverse ? this.formatMatrix(inverse) : 'Matrix is not invertible';
                    break;
            }
            resultDiv.textContent = result;
        } catch (error) {
            resultDiv.textContent = 'Error: ' + error.message;
        }
    }
    
    calculateDeterminant(matrix) {
        const size = matrix.length;
        
        if (size === 2) {
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
        } else if (size === 3) {
            return matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
                 - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
                 + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]);
        }
        
        throw new Error('Determinant calculation only supported for 2x2 and 3x3 matrices');
    }
    
    transposeMatrix(matrix) {
        const size = matrix.length;
        const transposed = [];
        
        for (let i = 0; i < size; i++) {
            transposed[i] = [];
            for (let j = 0; j < size; j++) {
                transposed[i][j] = matrix[j][i];
            }
        }
        
        return transposed;
    }
    
    inverseMatrix(matrix) {
        const det = this.calculateDeterminant(matrix);
        if (Math.abs(det) < 1e-10) return null;
        
        const size = matrix.length;
        
        if (size === 2) {
            return [
                [matrix[1][1] / det, -matrix[0][1] / det],
                [-matrix[1][0] / det, matrix[0][0] / det]
            ];
        }
        
        // For 3x3 matrices, use adjugate matrix method
        if (size === 3) {
            const adj = this.adjugateMatrix(matrix);
            return adj.map(row => row.map(val => val / det));
        }
        
        return null;
    }
    
    adjugateMatrix(matrix) {
        const size = matrix.length;
        const adj = [];
        
        for (let i = 0; i < size; i++) {
            adj[i] = [];
            for (let j = 0; j < size; j++) {
                const minor = this.getMinor(matrix, i, j);
                adj[i][j] = Math.pow(-1, i + j) * this.calculateDeterminant(minor);
            }
        }
        
        return this.transposeMatrix(adj);
    }
    
    getMinor(matrix, row, col) {
        const size = matrix.length;
        const minor = [];
        
        for (let i = 0; i < size; i++) {
            if (i === row) continue;
            const minorRow = [];
            for (let j = 0; j < size; j++) {
                if (j === col) continue;
                minorRow.push(matrix[i][j]);
            }
            minor.push(minorRow);
        }
        
        return minor;
    }
    
    formatMatrix(matrix) {
        return matrix.map(row => 
            '[' + row.map(val => this.formatNumber(val).padStart(8)).join(' ') + ']'
        ).join('\n');
    }
    
    // Statistics Calculator Functions
    calculateStatistics() {
        const input = document.getElementById('statsData').value;
        const resultDiv = document.getElementById('statsResults');
        
        try {
            const data = input.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
            
            if (data.length === 0) {
                resultDiv.innerHTML = '<div class="error-message">Please enter valid numbers</div>';
                return;
            }
            
            const stats = {
                'Count': data.length,
                'Sum': data.reduce((a, b) => a + b, 0),
                'Mean': data.reduce((a, b) => a + b, 0) / data.length,
                'Median': this.calculateMedian(data),
                'Mode': this.calculateMode(data),
                'Range': Math.max(...data) - Math.min(...data),
                'Min': Math.min(...data),
                'Max': Math.max(...data),
                'Variance': this.calculateVariance(data),
                'Std Deviation': this.calculateStandardDeviation(data)
            };
            
            resultDiv.innerHTML = Object.entries(stats).map(([label, value]) => 
                `<div class="stat-row">
                    <span class="stat-label">${label}:</span>
                    <span class="stat-value">${typeof value === 'number' ? this.formatNumber(value) : value}</span>
                </div>`
            ).join('');
            
        } catch (error) {
            resultDiv.innerHTML = '<div class="error-message">Error calculating statistics</div>';
        }
    }
    
    calculateMedian(data) {
        const sorted = [...data].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        
        return sorted.length % 2 === 0 
            ? (sorted[mid - 1] + sorted[mid]) / 2 
            : sorted[mid];
    }
    
    calculateMode(data) {
        const frequency = {};
        data.forEach(val => {
            frequency[val] = (frequency[val] || 0) + 1;
        });
        
        const maxFreq = Math.max(...Object.values(frequency));
        const modes = Object.keys(frequency).filter(key => frequency[key] === maxFreq);
        
        return modes.length === data.length ? 'No mode' : modes.join(', ');
    }
    
    calculateVariance(data) {
        const mean = data.reduce((a, b) => a + b, 0) / data.length;
        const squaredDiffs = data.map(x => Math.pow(x - mean, 2));
        return squaredDiffs.reduce((a, b) => a + b, 0) / data.length;
    }
    
    calculateStandardDeviation(data) {
        return Math.sqrt(this.calculateVariance(data));
    }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AdvancedCalculator();
});