"""
Auto Bug Report Generator - Core Engine
=======================================
This module provides utilities to automatically catch exceptions, extract
critical error diagnostics, and write clean, formatted bug reports to text files.

Built using Python's standard library:
- traceback: For extracting stack frames and formatting tracebacks.
- datetime:  For timestamping the bug reports.
- logging:   For logging operations, warnings, and error detection events.
"""

import os
import sys
import logging
import datetime
import traceback
from pathlib import Path
from functools import wraps

# Setup module-level logger
logger = logging.getLogger("AutoBugReporter")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class BugReportGenerator:
    """
    Manages error inspection, formatting, and file generation for bug reports.
    """

    def __init__(self, reports_dir="reports"):
        """
        Initialize the generator with a destination directory for reports.
        
        :param reports_dir: Directory where report text files will be stored.
        """
        self.reports_dir = Path(reports_dir)
        self._ensure_reports_directory()

    def _ensure_reports_directory(self):
        """Safely create the reports directory if it doesn't already exist."""
        try:
            self.reports_dir.mkdir(parents=True, exist_ok=True)
        except OSError as err:
            logger.error(f"Failed to create reports directory '{self.reports_dir}': {err}")

    def extract_error_details(self, exc_type, exc_value, exc_traceback):
        """
        Extract key details from an exception:
        - Error type and message
        - File name and line number
        - Originating function/scope and code line
        - Short formatted traceback
        """
        try:
            # 1. Error type and message
            error_type = exc_type.__name__ if exc_type else "UnknownError"
            error_message = str(exc_value) if exc_value else "No error message provided."

            # 2. Extract file name and line number from the traceback
            file_name = "Unknown"
            line_number = "Unknown"
            code_line = "N/A"
            function_name = "Unknown"

            if exc_traceback:
                extracted_frames = traceback.extract_tb(exc_traceback)
                if extracted_frames:
                    # The last frame is where the exception was directly raised
                    last_frame = extracted_frames[-1]
                    file_name = os.path.abspath(last_frame.filename)
                    line_number = last_frame.lineno
                    function_name = last_frame.name
                    code_line = last_frame.line or "N/A"

            # 3. Format traceback
            if exc_traceback:
                formatted_tb = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            else:
                formatted_tb = "No traceback available."

            return {
                "error_type": error_type,
                "error_message": error_message,
                "file_name": file_name,
                "line_number": line_number,
                "function_name": function_name,
                "code_line": code_line,
                "traceback": formatted_tb.strip(),
            }
        except Exception as internal_err:
            logger.error(f"Failed to extract error details safely: {internal_err}")
            return {
                "error_type": "ExtractorFailure",
                "error_message": str(internal_err),
                "file_name": "Unknown",
                "line_number": "Unknown",
                "function_name": "Unknown",
                "code_line": "N/A",
                "traceback": "Traceback extraction encountered an internal error.",
            }

    def build_report_text(self, details, timestamp=None):
        """
        Format extracted error details into a structured, human-readable text report.
        """
        if timestamp is None:
            timestamp = datetime.datetime.now()

        formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        report_lines = [
            "=" * 78,
            "                        AUTO BUG REPORT GENERATOR",
            "=" * 78,
            f"1. Date & Time       : {formatted_date}",
            f"2. Error Type        : {details['error_type']}",
            f"3. Error Message     : {details['error_message']}",
            f"4. File Name         : {details['file_name']}",
            f"5. Line Number       : {details['line_number']}",
            f"6. Function / Scope  : {details['function_name']}()",
            f"7. Failing Code Line : {details['code_line']}",
            "=" * 78,
            "SHORT TRACEBACK:",
            "=" * 78,
            details["traceback"],
            "=" * 78,
            "SYSTEM CONTEXT:",
            "=" * 78,
            f"Python Version       : {sys.version.split()[0]}",
            f"Operating System     : {sys.platform}",
            f"Execution Directory  : {os.getcwd()}",
            "=" * 78,
            "                     END OF REPORT",
            "=" * 78,
        ]

        return "\n".join(report_lines)

    def save_report(self, report_text, error_type="Error", timestamp=None):
        """
        Save the bug report text to a unique .txt file in the reports directory.
        
        :return: Path to the generated report file, or None if saving failed.
        """
        if timestamp is None:
            timestamp = datetime.datetime.now()

        # Sanitize error type for filename
        clean_error_type = "".join(c for c in error_type if c.isalnum() or c in ("_", "-"))
        if not clean_error_type:
            clean_error_type = "Bug"

        filename = f"bug_report_{clean_error_type}_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = self.reports_dir / filename

        # Avoid collision if multiple reports generated in the same second
        counter = 1
        while file_path.exists():
            file_path = self.reports_dir / f"bug_report_{clean_error_type}_{timestamp.strftime('%Y%m%d_%H%M%S')}_{counter}.txt"
            counter += 1

        try:
            self._ensure_reports_directory()
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(report_text)
            logger.info(f"Bug report successfully saved to: {file_path}")
            return str(file_path)
        except OSError as err:
            logger.critical(f"Failed to write bug report to '{file_path}': {err}")
            return None

    def generate_report(self, exc_type, exc_value, exc_traceback):
        """
        High-level helper: extracts details, builds text, and writes to a .txt file.
        
        :return: Tuple of (report_file_path, details_dict)
        """
        try:
            timestamp = datetime.datetime.now()
            details = self.extract_error_details(exc_type, exc_value, exc_traceback)
            
            logger.warning(
                f"Detected {details['error_type']} at line {details['line_number']} in {os.path.basename(details['file_name'])}: {details['error_message']}"
            )
            
            report_text = self.build_report_text(details, timestamp=timestamp)
            saved_path = self.save_report(report_text, error_type=details["error_type"], timestamp=timestamp)
            return saved_path, details
        except Exception as unexpected_err:
            logger.critical(f"Unexpected failure inside generate_report: {unexpected_err}")
            return None, {}


# Default global instance
default_generator = BugReportGenerator()


def generate_bug_report(exc_type, exc_value, exc_traceback, reports_dir="reports"):
    """Convenience functional wrapper around BugReportGenerator.generate_report."""
    generator = BugReportGenerator(reports_dir=reports_dir)
    return generator.generate_report(exc_type, exc_value, exc_traceback)


def install_global_hook(reports_dir="reports"):
    """
    Install a global system exception hook using sys.excepthook.
    Whenever any uncaught exception occurs anywhere in Python,
    a bug report is automatically generated and saved.
    """
    generator = BugReportGenerator(reports_dir=reports_dir)

    def auto_bug_report_excepthook(exc_type, exc_value, exc_traceback):
        # Do not catch keyboard interrupt (Ctrl+C) as a bug report
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.error("Intercepted unhandled exception via global excepthook.")
        generator.generate_report(exc_type, exc_value, exc_traceback)
        
        # Call Python's standard exception handler to also print to stderr
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    sys.excepthook = auto_bug_report_excepthook
    logger.info("Auto Bug Report Generator global hook installed.")


class MonitorErrors:
    """
    Context manager to monitor a specific block of code for errors.
    
    Usage:
        with MonitorErrors(reraise=False):
            risky_operation()
    """

    def __init__(self, reports_dir="reports", reraise=True):
        self.generator = BugReportGenerator(reports_dir=reports_dir)
        self.reraise = reraise
        self.report_path = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None:
            self.report_path, _ = self.generator.generate_report(exc_type, exc_value, exc_traceback)
            # If reraise is False, suppress exception and allow code to continue safely
            return not self.reraise
        return False


def auto_report(reports_dir="reports", reraise=True):
    """
    Decorator to wrap any function with automatic bug reporting.
    
    Usage:
        @auto_report(reraise=False)
        def my_function():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                generator = BugReportGenerator(reports_dir=reports_dir)
                generator.generate_report(type(exc), exc, exc.__traceback__)
                if reraise:
                    raise
        return wrapper
    return decorator
