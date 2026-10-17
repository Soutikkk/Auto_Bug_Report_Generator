
# 🐞 Auto Bug Report Generator

A lightweight Python tool that automatically generates detailed bug reports when exceptions occur. It captures error information, traceback details, source code location, and system information to help developers debug problems faster.

## ✨ Features

- **Automatic Bug Reporting:** Generates reports when exceptions occur.
- **Multiple Monitoring Methods:** Supports decorators, context managers, and a global exception hook.
- **Sample Error Demonstrations:** Includes examples of `ZeroDivisionError`, `FileNotFoundError`, and `KeyError`.
- **Custom Script Execution:** Runs Python scripts with automatic bug reporting enabled.
- **Report Management:** Lists and displays previously generated bug reports.
- **Timestamped Reports:** Saves reports as text files in the `reports/` directory.
- **No External Dependencies:** Uses Python's built-in standard library.

## 📂 Project Structure

```text
Auto_Bug_Report_Generator/
├── bug_reporter.py
├── main.py
├── sample_code.py
├── reports/
└── README.md
```

## 🛠️ Requirements

- Python 3.8 or newer
- Visual Studio Code or another Python editor
- No additional Python packages required

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Navigate to the project directory

```bash
cd Auto_Bug_Report_Generator-main
```

### 3. Run the application

```bash
python main.py
```

If your system uses `python3`, run:

```bash
python3 main.py
```

## 💻 Usage

### Run the interactive menu

```bash
python main.py
```

### Run the sample demonstrations

```bash
python main.py --demo
```

### Run a Python script with automatic bug reporting

```bash
python main.py --run path/to/your_script.py
```

### List generated bug reports

```bash
python main.py --list
```

### View a specific bug report

```bash
python main.py --view reports/your_report_filename.txt
```

Replace the example filename with an existing report in the `reports/` directory.

### Display available command-line options

```bash
python main.py --help
```

## 🔍 Monitoring Methods

### 1. Decorator

Use the `auto_report` decorator to monitor a function for exceptions.

```python
from bug_reporter import auto_report

@auto_report(reports_dir="reports", reraise=True)
def divide(a, b):
    return a / b

try:
    divide(10, 0)
except ZeroDivisionError:
    print("Bug report generated!")
```

### 2. Context Manager

Use `MonitorErrors` to monitor a block of code.

```python
from bug_reporter import MonitorErrors

with MonitorErrors(reports_dir="reports", reraise=True):
    result = 10 / 0
```

### 3. Global Exception Hook

Automatically report uncaught exceptions in the running Python process.

```python
from bug_reporter import install_global_hook

install_global_hook(reports_dir="reports")

# Unhandled exceptions will generate bug reports.
```

## 📄 Bug Report Information

Generated reports can contain:

- Date and time of the exception
- Exception type and error message
- Source file and line number
- Function name
- Failing source code line, when available
- Full traceback
- Python version
- Operating system information
- Current working directory

Reports are saved in the `reports/` directory with filenames similar to:

```text
bug_report_<ErrorType>_<YYYYMMDD_HHMMSS>.txt
```

## 🎯 Project Objective

The objective of this project is to simplify debugging by automating the collection of useful error information. Instead of manually searching through tracebacks, developers can use generated reports to understand and investigate exceptions more efficiently.

## ⚠️ Limitations

- The tool focuses on Python exceptions and does not detect every logical or design bug.
- Caught exceptions are not automatically reported by the global exception hook.
- Bug reports may contain sensitive information, such as file paths and source code. Review reports before sharing them.
- Only execute trusted Python scripts.

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome!

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes.
5. Submit a pull request.

## 📜 License

No license file is currently included. Add a license to specify the terms for using, modifying, and distributing this project.

---

**Built with Python 🐍**
