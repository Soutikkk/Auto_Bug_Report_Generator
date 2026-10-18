# 🐞 Auto Bug Report Generator & Web Diagnostic Studio

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-Zero%20External-brightgreen.svg)](#)
[![Interface](https://img.shields.io/badge/ui-Modern%20Glassmorphism-6366f1.svg)](#)

An intelligent, zero-overhead diagnostic framework that intercepts uncaught Python exceptions, isolates stack frames, extracts system context, and writes standardized, human-readable bug reports in real-time.

Now includes **AutoBug.io Studio**, a modern glassmorphic web dashboard to visualize runtime errors, simulate bug scenarios, inspect call stacks, and synthesize issue reports with automated remediation insights.

---

## ✨ Features

- **Automated Exception Capture**: Intercepts unhandled errors at the function, block, or global interpreter level.
- **Precision Diagnostics**: Records timestamp, exception type, error message, failing file, line number, scope, isolated failing statement, full traceback, and OS context.
- **Zero External Dependencies**: Powered entirely by the Python standard library (`traceback`, `datetime`, `logging`, `pathlib`, `http.server`).
- **Interactive Web Dashboard**:
  - **Metrics & KPIs**: Track total isolated crashes, frequent exception classes, and diagnostic coverage.
  - **Report Explorer**: Filter, search, and inspect `.txt` bug reports with syntax highlighting.
  - **Live Bug Studio**: Test custom tracebacks or preset templates (ZeroDivisionError, KeyError, FileNotFoundError, etc.) and generate production-grade reports with a single click.
  - **Automated Remediation Insights**: Contextual suggestions to help patch bugs immediately.
  - **One-Click Export**: Copy raw report text, GitHub-flavored markdown issue snippets, or export as `.txt`.

---

## 🚀 Quick Start

### 1. Launch the Web Dashboard & Studio
Launch the local web server and open the interactive dashboard in your browser:

```bash
# Directly via web server:
python web_server.py

# Or via the CLI runner:
python main.py --web
```
Open your browser to: **`http://localhost:8080/`**

### 2. Interactive CLI Mode
If you prefer running inside the terminal:

```bash
python main.py
```
This presents an interactive menu to run demos, monitor scripts, or inspect saved `.txt` reports.

### 3. Run Sample Bug Demonstrations
```bash
python main.py --demo
```

### 4. Monitor Any Python Script
Execute any target Python script with automatic crash reporting active:
```bash
python main.py --run path/to/your_script.py
```

---

## 🛠️ Integration Methods

### Method 1: Decorator (`@auto_report`)
Wrap functions to automatically generate reports whenever an uncaught exception is raised:

```python
from bug_reporter import auto_report

@auto_report(reports_dir="reports", reraise=False)
def calculate_average(total, count):
    return total / count  # Catches ZeroDivisionError if count is 0
```

### Method 2: Context Manager (`MonitorErrors`)
Scope a sensitive code block (e.g. network requests, file I/O) without decorating the full function:

```python
from bug_reporter import MonitorErrors

with MonitorErrors(reports_dir="reports", reraise=False) as monitor:
    with open("config.json", "r") as f:
        data = f.read()

if monitor.report_path:
    print(f"Handled safely! Report created: {monitor.report_path}")
```

### Method 3: Global Interpreter Hook (`install_global_hook`)
Attach a safety net across the entire application. Any crash before process termination will be saved:

```python
from bug_reporter import install_global_hook

install_global_hook(reports_dir="reports")

# Application entry point continues normally...
```

---

## 📁 Repository Structure

```text
├── bug_reporter.py        # Core engine: BugReportGenerator, decorators, hooks
├── main.py                # Command-line interface & interactive menu
├── sample_code.py         # Sample test scenarios (ZeroDivisionError, KeyError, etc.)
├── web_server.py          # Lightweight REST server & static file provider
├── reports/               # Auto-generated .txt bug reports
│   └── bug_report_*.txt
└── frontend/              # Web Dashboard & Studio
    ├── index.html         # Main dashboard interface
    ├── css/
    │   └── style.css      # Modern dark-mode glassmorphism styling
    └── js/
        └── app.js         # Reactive UI, studio synthesizer, and REST bindings
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
