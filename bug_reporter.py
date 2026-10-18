"""
Auto Bug Report Generator - Core Engine
=======================================
Automatically captures exceptions, extracts diagnostic information,
and saves structured bug reports to text files.

Uses Python's standard library:
- os, sys: System and environment information
- logging: Application logging
- datetime: Timestamps
- traceback: Exception diagnostics
- pathlib: Cross-platform file handling
- functools: Decorator metadata preservation
- threading: Thread-safe report file generation
"""

import os
import sys
import logging
import datetime
import traceback
import threading
from pathlib import Path
from functools import wraps


# ============================================================
# LOGGER CONFIGURATION
# ============================================================

logger = logging.getLogger("AutoBugReporter")

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.setLevel(logging.INFO)
logger.propagate = False


class BugReportGenerator:
    """Extract, format, and save exception reports."""

    _file_lock = threading.Lock()

    def __init__(self, reports_dir="reports"):
        self.reports_dir = Path(reports_dir)
        self._ensure_reports_directory()

    def _ensure_reports_directory(self):
        """Create the report directory if it does not exist."""
        try:
            self.reports_dir.mkdir(parents=True, exist_ok=True)
            return True
        except OSError:
            logger.exception(
                "Unable to create reports directory: %s",
                self.reports_dir,
            )
            return False

    def extract_error_details(
        self, exc_type, exc_value, exc_traceback
    ):
        """Extract exception information and traceback details."""

        try:
            error_type = (
                exc_type.__name__ if exc_type else "UnknownError"
            )
            error_message = (
                str(exc_value)
                if exc_value is not None
                else "No error message provided."
            )

            file_name = "Unknown"
            line_number = "Unknown"
            function_name = "Unknown"
            code_line = "N/A"

            if exc_traceback is not None:
                frames = traceback.extract_tb(exc_traceback)

                if frames:
                    frame = frames[-1]
                    file_name = os.path.abspath(frame.filename)
                    line_number = frame.lineno
                    function_name = frame.name
                    code_line = frame.line or "N/A"

            formatted_traceback = (
                "".join(
                    traceback.format_exception(
                        exc_type, exc_value, exc_traceback
                    )
                ).strip()
                if exc_traceback is not None
                else "No traceback available."
            )

            return {
                "error_type": error_type,
                "error_message": error_message,
                "file_name": file_name,
                "line_number": line_number,
                "function_name": function_name,
                "code_line": code_line,
                "traceback": formatted_traceback,
            }

        except Exception:
            logger.exception("Failed to extract exception details.")

            return {
                "error_type": "ExtractorFailure",
                "error_message": "Could not extract exception details.",
                "file_name": "Unknown",
                "line_number": "Unknown",
                "function_name": "Unknown",
                "code_line": "N/A",
                "traceback": "Traceback extraction failed.",
            }

    def build_report_text(self, details, timestamp=None):
        """Build a readable text report."""

        timestamp = timestamp or datetime.datetime.now().astimezone()
        formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")

        separator = "=" * 78

        report_lines = [
            separator,
            "                    AUTO BUG REPORT GENERATOR",
            separator,
            f"1. Date & Time       : {formatted_date}",
            f"2. Error Type        : {details['error_type']}",
            f"3. Error Message     : {details['error_message']}",
            f"4. File Name         : {details['file_name']}",
            f"5. Line Number       : {details['line_number']}",
            f"6. Function / Scope  : {details['function_name']}",
            f"7. Failing Code Line : {details['code_line']}",
            separator,
            "TRACEBACK:",
            separator,
            details["traceback"],
            separator,
            "SYSTEM CONTEXT:",
            separator,
            f"Python Version       : {sys.version.split()[0]}",
            f"Operating System     : {sys.platform}",
            f"Execution Directory  : {os.getcwd()}",
            separator,
            "                       END OF REPORT",
            separator,
            "",
        ]

        return "\n".join(report_lines)

    @staticmethod
    def _sanitize_filename(value):
        """Keep filename components safe and portable."""
        cleaned = "".join(
            char for char in value
            if char.isalnum() or char in ("_", "-")
        )
        return cleaned[:80] or "Bug"

    def save_report(self, report_text, error_type="Error", timestamp=None):
        """Save a report to a uniquely named UTF-8 text file."""

        timestamp = timestamp or datetime.datetime.now().astimezone()
        clean_error_type = self._sanitize_filename(error_type)

        timestamp_string = timestamp.strftime("%Y%m%d_%H%M%S_%f")
        filename = (
            f"bug_report_{clean_error_type}_{timestamp_string}.txt"
        )

        try:
            if not self._ensure_reports_directory():
                return None

            # Protect filename selection and file creation between
            # threads using this class in the current process.
            with self._file_lock:
                file_path = self.reports_dir / filename
                counter = 1

                while file_path.exists():
                    filename = (
                        f"bug_report_{clean_error_type}_"
                        f"{timestamp_string}_{counter}.txt"
                    )
                    file_path = self.reports_dir / filename
                    counter += 1

                with file_path.open(
                    "x", encoding="utf-8", newline="\n"
                ) as report_file:
                    report_file.write(report_text)

            logger.info("Bug report saved: %s", file_path)
            return str(file_path)

        except OSError:
            logger.exception("Failed to save bug report.")
            return None

    def generate_report(self, exc_type, exc_value, exc_traceback):
        """Extract, format, and save a report."""

        try:
            timestamp = datetime.datetime.now().astimezone()

            details = self.extract_error_details(
                exc_type, exc_value, exc_traceback
            )

            logger.warning(
                "Detected %s at line %s in %s: %s",
                details["error_type"],
                details["line_number"],
                os.path.basename(details["file_name"]),
                details["error_message"],
            )

            report_text = self.build_report_text(
                details, timestamp=timestamp
            )

            saved_path = self.save_report(
                report_text,
                error_type=details["error_type"],
                timestamp=timestamp,
            )

            return saved_path, details

        except Exception:
            # Do not replace the original application exception
            # with an exception raised by the reporting engine.
            logger.exception("Unexpected bug-report generation failure.")
            return None, {}


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

default_generator = BugReportGenerator()


def generate_bug_report(
    exc_type, exc_value, exc_traceback, reports_dir="reports"
):
    """Generate a report using the requested output directory."""

    generator = BugReportGenerator(reports_dir=reports_dir)
    return generator.generate_report(
        exc_type, exc_value, exc_traceback
    )


# ============================================================
# GLOBAL EXCEPTION HOOK
# ============================================================

def install_global_hook(reports_dir="reports"):
    """
    Install a hook for uncaught exceptions in the main thread.

    KeyboardInterrupt and SystemExit are delegated to Python's
    default exception handler without generating bug reports.
    """

    generator = BugReportGenerator(reports_dir=reports_dir)

    def auto_bug_report_excepthook(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, (KeyboardInterrupt, SystemExit)):
            sys.__excepthook__(exc_type, exc_value, exc_tb)
            return

        try:
            logger.error("Intercepted an unhandled exception.")
            generator.generate_report(exc_type, exc_value, exc_tb)
        except Exception:
            logger.exception("The global exception hook failed.")
        finally:
            # Preserve Python's normal traceback output.
            sys.__excepthook__(exc_type, exc_value, exc_tb)

    sys.excepthook = auto_bug_report_excepthook
    logger.info("Global exception hook installed.")


# ============================================================
# CONTEXT MANAGER
# ============================================================

class MonitorErrors:
    """
    Monitor a block of code and generate a report on failure.

    Example:
        with MonitorErrors(reraise=False) as monitor:
            risky_operation()

        print(monitor.report_path)
    """

    def __init__(self, reports_dir="reports", reraise=True):
        self.generator = BugReportGenerator(reports_dir=reports_dir)
        self.reraise = reraise
        self.report_path = None
        self.details = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            return False

        self.report_path, self.details = (
            self.generator.generate_report(
                exc_type, exc_value, exc_tb
            )
        )

        # Returning True suppresses the exception.
        return not self.reraise


# ============================================================
# DECORATOR
# ============================================================

def auto_report(reports_dir="reports", reraise=True):
    """
    Automatically generate reports when a function raises an error.

    Example:
        @auto_report(reraise=True)
        def divide(a, b):
            return a / b
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except Exception as exc:
                generator = BugReportGenerator(
                    reports_dir=reports_dir
                )
                generator.generate_report(
                    type(exc), exc, exc.__traceback__
                )

                if reraise:
                    raise

                return None

        return wrapper

    return decorator


# ============================================================
# EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":

    @auto_report(reports_dir="reports", reraise=True)
    def divide_numbers(a, b):
        return a / b

    try:
        divide_numbers(10, 0)

    except ZeroDivisionError:
        print("An error occurred. Check the reports directory.")

    # Example of using the context manager:
    with MonitorErrors(
        reports_dir="reports", reraise=False
    ) as monitor:
        result = 10 / 0

    if monitor.report_path:
        print("Generated report:", monitor.report_path)
