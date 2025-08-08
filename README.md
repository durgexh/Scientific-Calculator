# Advanced Scientific Calculator

**The most advanced scientific calculator app in C for Android Play Store and GitHub**

## 🚀 Project Overview

This project implements a comprehensive scientific calculator with advanced mathematical capabilities, built using C for the core computational engine and Android Java/Kotlin for the user interface. The calculator is designed to be published on the Google Play Store and open-sourced on GitHub.

## ✨ Key Features

### Core Mathematical Functions
- **Basic Arithmetic**: Addition, subtraction, multiplication, division, modulo
- **Advanced Operations**: Power, root (square, cube, nth), factorial
- **Trigonometric Functions**: sin, cos, tan, sec, csc, cot (and their inverses)
- **Hyperbolic Functions**: sinh, cosh, tanh, sech, csch, coth (and their inverses)
- **Logarithmic Functions**: ln, log10, log2, arbitrary base logarithms
- **Exponential Functions**: exp, 10^x, 2^x, e^x

### Advanced Features
- **Complex Numbers**: Full support for complex number arithmetic
- **Matrix Operations**: Basic matrix calculations (determinant, multiplication, inverse)
- **Statistical Functions**: Mean, median, mode, standard deviation, variance
- **Combinatorics**: Permutations and combinations
- **Number Theory**: GCD, LCM, prime factorization
- **Unit Conversions**: Length, area, volume, mass, temperature
- **Physical Constants**: π, e, φ (golden ratio), and more

### User Interface Features
- **Multiple Themes**: Dark and light mode support
- **Memory Functions**: Store, recall, add, subtract memory operations
- **History**: Complete calculation history with recall functionality
- **Expression Parser**: Natural mathematical expression input
- **Error Handling**: Comprehensive error detection and user feedback
- **Multi-language Support**: Localization ready

## 🏗️ Architecture

### C Core Engine
```
calculator_engine.c/h    - Main calculation engine
expression_parser.c/h    - Mathematical expression parser
math_functions.c/h       - Extended mathematical functions
complex_numbers.c/h      - Complex number operations
matrix_operations.c/h    - Matrix calculations
statistics.c/h           - Statistical functions
unit_converter.c/h       - Unit conversion utilities
constants.h              - Mathematical constants
```

### Android Integration
```
MainActivity.java        - Main Android activity
jni_bridge.c            - JNI interface between Java and C
CMakeLists.txt          - CMake build configuration
Application.mk          - NDK build settings
Android.mk              - Alternative build system
activity_main.xml       - Android UI layout
```

## 🛠️ Building the Project

### Prerequisites
- **Android Studio** 4.0+
- **Android NDK** r21+
- **CMake** 3.18.1+
- **Android SDK** API 21+ (Android 5.0+)

### Build Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/advanced-scientific-calculator
cd advanced-scientific-calculator
```

#### 2. Open in Android Studio
1. Open Android Studio
2. Select "Open an existing Android Studio project"
3. Navigate to the cloned directory and select it

#### 3. Configure NDK
1. Go to File → Project Structure → SDK Location
2. Set the NDK location if not already configured
3. Ensure CMake is installed via SDK Manager

#### 4. Build the Project
```bash
# Using Android Studio: Build → Make Project
# Or using command line:
./gradlew assembleDebug
```

#### 5. Install on Device/Emulator
```bash
./gradlew installDebug
```

## 📱 Android App Structure

### Main Components
- **Calculator UI**: Modern, intuitive interface with scientific function layout
- **Expression Display**: Shows both input expression and calculated result
- **Function Buttons**: Organized by category (basic, trig, log, advanced)
- **Memory Panel**: Memory operations with visual indicators
- **Settings**: Theme selection, angle units, precision settings
- **History**: Calculation history with export functionality

### Supported Android Versions
- **Minimum SDK**: API 21 (Android 5.0)
- **Target SDK**: API 34 (Android 14)
- **Architecture Support**: ARM64, ARM, x86_64, x86

## 🧮 Usage Examples

### Basic Calculations
```
2 + 3 * 4        → 14
(2 + 3) * 4      → 20
sqrt(16)         → 4
2^3              → 8
```

### Scientific Functions
```
sin(30)          → 0.5 (in degree mode)
log(100)         → 2
exp(1)           → 2.71828...
factorial(5)     → 120
```

### Advanced Expressions
```
sin(π/4) + cos(π/4)           → 1.41421...
log(e^3)                      → 3
sqrt(3^2 + 4^2)              → 5
comb(10, 3)                   → 120
```

### Complex Numbers
```
(2+3i) + (1-2i)  → 3+i
(2+3i) * (1-2i)  → 8-i
```

## 📚 API Documentation

### Core Calculator Functions

#### Basic Operations
```c
calc_result_t calc_add(double a, double b);
calc_result_t calc_subtract(double a, double b);
calc_result_t calc_multiply(double a, double b);
calc_result_t calc_divide(double a, double b);
calc_result_t calc_power(double base, double exponent);
```

#### Trigonometric Functions
```c
calc_result_t calc_sin(double x, bool degrees);
calc_result_t calc_cos(double x, bool degrees);
calc_result_t calc_tan(double x, bool degrees);
// ... and inverse functions
```

#### Memory Operations
```c
void calc_memory_store(calc_state_t* state, double value);
void calc_memory_add(calc_state_t* state, double value);
double calc_memory_recall(calc_state_t* state);
void calc_memory_clear(calc_state_t* state);
```

### Error Handling
The calculator provides comprehensive error handling for:
- Division by zero
- Domain errors (e.g., sqrt of negative number)
- Overflow/underflow conditions
- Invalid function arguments
- Parse errors in expressions

## 🎨 Customization

### Adding New Functions
1. Define the function in `math_functions.c`
2. Add the declaration to `math_functions.h`
3. Update the parser in `expression_parser.c`
4. Add UI button in Android layout
5. Update JNI bridge if needed

### Theming
The app supports multiple themes defined in:
- `colors.xml` - Color definitions
- `styles.xml` - Theme styles
- `themes.xml` - Day/night themes

## 🧪 Testing

### Unit Tests
```bash
# Run C library tests
gcc -o test_calculator test_calculator.c calculator_engine.c -lm
./test_calculator

# Run Android tests
./gradlew test
```

### Test Coverage
- Mathematical function accuracy
- Expression parsing edge cases
- Memory operations
- Error handling scenarios
- UI interaction tests

## 📦 Publishing to Google Play Store

### Prerequisites
1. **Google Play Developer Account** ($25 registration fee)
2. **App Signing**: Configure app signing in Play Console
3. **Privacy Policy**: Required for apps with data collection
4. **Content Rating**: Complete content rating questionnaire

### Preparation Steps

#### 1. App Bundle Generation
```bash
./gradlew bundleRelease
```

#### 2. Play Console Setup
1. Create new app in Play Console
2. Complete app information
3. Upload app bundle
4. Set pricing and distribution
5. Complete content rating
6. Add store listing (descriptions, screenshots)

#### 3. Release Configuration
- **Target API Level**: Must target API 34+ (Android 14)
- **App Size**: Optimize for <150MB
- **Permissions**: Minimize required permissions
- **64-bit Support**: Required for new apps

### Store Listing Optimization
- **Title**: "Advanced Scientific Calculator Pro"
- **Short Description**: "Most advanced scientific calculator with 100+ functions"
- **Keywords**: scientific calculator, math, engineering, statistics
- **Screenshots**: Show different calculator modes and features
- **App Icon**: Professional, recognizable calculator icon

## 🌟 Advanced Features

### 1. Expression History
- Stores up to 1000 recent calculations
- Search and filter functionality
- Export history to CSV/TXT
- Favorite expressions

### 2. Customizable Interface
- Resizable buttons for accessibility
- Custom function shortcuts
- Landscape/portrait optimized layouts
- Haptic feedback

### 3. Graphing Capabilities (Future)
- 2D function plotting
- Parametric equations
- Statistical plotting
- Export graphs as images

### 4. Programming Mode (Future)
- Binary, octal, hexadecimal calculations
- Bitwise operations
- Integer arithmetic modes
- Programming constants

## 🔒 Security & Privacy

### Data Collection
- **No Personal Data**: The app doesn't collect personal information
- **Local Storage Only**: All data stored locally on device
- **No Network Access**: Fully offline operation
- **Open Source**: Complete transparency in code

### Permissions Required
- **NONE** - The calculator requires no special permissions

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- **C Code**: Follow C99 standard, use consistent naming
- **Java Code**: Follow Android coding conventions
- **Documentation**: Update both inline and README documentation
- **Testing**: Add tests for new features

### Issue Reporting
Please use GitHub Issues to report:
- Bugs with detailed reproduction steps
- Feature requests with clear use cases
- Performance issues with benchmarks
- Documentation improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Mathematical Libraries**: Built upon standard C math library
- **Android Team**: For excellent NDK and development tools
- **Open Source Community**: For inspiration and best practices
- **Beta Testers**: For valuable feedback and bug reports

## 📞 Support

- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Comprehensive API and user documentation
- **Community**: Join our discussions on GitHub
- **Email**: support@advancedcalculator.com

## 🗺️ Roadmap

### Version 1.1 (Q2 2024)
- [ ] Graphing functionality
- [ ] Enhanced matrix operations
- [ ] Calculus operations (derivatives, integrals)
- [ ] Programming mode

### Version 1.2 (Q3 2024)
- [ ] Cloud backup/sync
- [ ] Tablet optimization
- [ ] Voice input
- [ ] LaTeX export

### Version 2.0 (Q4 2024)
- [ ] AI-powered math solving
- [ ] 3D graphing
- [ ] Scientific notation improvements
- [ ] Plugin architecture

---

**Made with ❤️ by the Advanced Calculator Team**

*Star this repository if you find it useful!*
