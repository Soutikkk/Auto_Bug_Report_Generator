```python
"""
Auto Bug Report Generator - Command Line Interface (CLI)
========================================================
Features:
- Run sample bug demonstrations.
- Execute Python scripts with automatic error reporting.
- List and view saved bug reports.
- Support interactive and command-line modes.
"""

import argparse
import runpy
import sys
from pathlib import Path

from bug_reporter import BugReportGenerator, install_global_hook, logger
import sample_code


REPORTS_DIR = Path("reports")


# ============================================================
# REPORT MANAGEMENT
# ============================================================

def list_reports(reports_dir=REPORTS_DIR):
    """List saved bug reports, newest first."""

    reports_path = Path(reports_dir)

    if not reports_path.is_dir():
        print(
            f"\n[Info] Reports directory "
            f"'{reports_path}' does not exist yet."
        )
        return []

    try:
        report_files = sorted(
            reports_path.glob("*.txt"),
            key=lambda file: file.stat().st_mtime,
            reverse=True,
        )
    except OSError as err:
        logger.error("Could not list reports: %s", err)
        print(f"\n[Error] Could not list reports: {err}")
        return []

    if not report_files:
        print(f"\n[Info] No bug reports found in '{reports_path}'.")
        return []

    print("\n" + "=" * 75)
    print(f" SAVED BUG REPORTS: {reports_path}")
    print("=" * 75)

    for index, file_path in enumerate(report_files, start=1):
        try:
            size = file_path.stat().st_size
            print(f" {index:>3}. {file_path.name} ({size} bytes)")
        except OSError:
            print(f" {index:>3}. {file_path.name} (size unavailable)")

    print("=" * 75)
    return report_files


def view_report(file_path, reports_dir=REPORTS_DIR):
    """Display a report from the configured reports directory."""

    reports_path = Path(reports_dir).resolve()
    requested_path = Path(file_path)

    # Allow a filename or a path relative to the reports directory.
    if not requested_path.is_absolute():
        requested_path = reports_path / requested_path

    try:
        resolved_path = requested_path.resolve()

        # Prevent accidentally opening files outside the reports folder.
        if not resolved_path.is_relative_to(reports_path):
            print("[Error] The requested file is outside the reports directory.")
            return False

        if not resolved_path.is_file():
            print(f"\n[Error] Report file not found: {resolved_path.name}")
            return False

        if resolved_path.suffix.lower() != ".txt":
            print("[Error] Only .txt report files can be viewed.")
            return False

        with resolved_path.open("r", encoding="utf-8") as report_file:
            content = report_file.read()

        print("\n" + "~" * 78)
        print(f" REPORT: {resolved_path.name}")
        print("~" * 78)
        print(content)
        print("~" * 78)
        return True

    except (OSError, UnicodeError, ValueError) as err:
        logger.error("Unable to read report: %s", err)
        print(f"\n[Error] Could not read report: {err}")
        return False


# ============================================================
# SCRIPT EXECUTION
# ============================================================

def run_target_script(script_path, reports_dir=REPORTS_DIR):
    """
    Execute a Python script with automatic bug reporting.

    Unhandled exceptions are reported, and the CLI returns control
    to its caller without terminating the interactive menu.
    """

    target_path = Path(script_path).expanduser()

    if not target_path.is_file():
        print(
            f"\n[Error] Script does not exist or is not a file: "
            f"{target_path}"
        )
        return False

    if target_path.suffix.lower() != ".py":
        print("[Error] The target must be a Python (.py) file.")
        return False

    try:
        target_path = target_path.resolve()
    except OSError as err:
        print(f"[Error] Could not resolve script path: {err}")
        return False

    print(
        f"\n[Runner] Executing '{target_path.name}' "
        "with Auto Bug Reporter active..."
    )
    print("-" * 75)

    # Install a hook for uncaught exceptions that reach the interpreter.
    install_global_hook(reports_dir=str(reports_dir))

    try:
        runpy.run_path(str(target_path), run_name="__main__")

        print("-" * 75)
        print(
            f"[Runner] '{target_path.name}' finished "
            "without an uncaught exception."
        )
        return True

    except SystemExit as exc:
        # Preserve the target script's normal exit behavior without
        # incorrectly treating SystemExit as an application bug.
        print("-" * 75)

        if exc.code not in (None, 0):
            print(f"[Runner] Script exited with status: {exc.code}")
            return False

        print("[Runner] Script exited normally.")
        return True

    except Exception as exc:
        print("-" * 75)

        generator = BugReportGenerator(reports_dir=reports_dir)

        report_path, _ = generator.generate_report(
            type(exc),
            exc,
            exc.__traceback__,
        )

        print(
            f"[Runner] Script failed with "
            f"{type(exc).__name__}: {exc}"
        )

        if report_path:
            print(f"[Runner] Bug report saved to: {report_path}")
        else:
            print("[Runner] Failed to save the bug report.")

        return False


# ============================================================
# INTERACTIVE MENU
# ============================================================

def interactive_menu():
    """Display the interactive main menu."""

    while True:
        print("\n" + "=" * 55)
        print("       AUTO BUG REPORT GENERATOR - MAIN MENU")
        print("=" * 55)
        print(" 1. Run sample bug demonstrations")
        print(" 2. Run a Python script with bug monitoring")
        print(" 3. List saved bug reports")
        print(" 4. View a bug report")
        print(" 5. Exit")
        print("=" * 55)

        try:
            choice = input("Enter your choice (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting Auto Bug Report Generator.")
            break

        if choice == "1":
            try:
                sample_code.run_all_samples()
            except Exception as exc:
                logger.exception("Sample demonstration failed.")
                generator = BugReportGenerator(
                    reports_dir=REPORTS_DIR
                )
                report_path, _ = generator.generate_report(
                    type(exc), exc, exc.__traceback__
                )

                if report_path:
                    print(f"[Info] Bug report saved: {report_path}")

        elif choice == "2":
            target = input(
                "Enter the Python script path: "
            ).strip().strip('"').strip("'")

            if target:
                run_target_script(target)
            else:
                print("[Warning] No script path entered.")

        elif choice == "3":
            list_reports()

        elif choice == "4":
            reports = list_reports()

            if not reports:
                continue

            selection = input(
                f"Enter report number (1-{len(reports)}) "
                "or filename: "
            ).strip().strip('"').strip("'")

            if selection.isdigit():
                index = int(selection)

                if 1 <= index <= len(reports):
                    view_report(reports[index - 1].name)
                else:
                    print("[Error] Invalid report number.")

            elif selection:
                view_report(selection)

            else:
                print("[Warning] No report selected.")

        elif choice == "5":
            print("\nExiting Auto Bug Report Generator. Goodbye!\n")
            break

        else:
            print("[Error] Please select a number between 1 and 5.")


# ============================================================
# COMMAND-LINE ARGUMENTS
# ============================================================

def parse_arguments(argv=None):
    """Parse command-line options."""

    parser = argparse.ArgumentParser(
        description=(
            "Automatically detect Python exceptions "
            "and generate detailed text bug reports."
        )
    )

    actions = parser.add_mutually_exclusive_group()

    actions.add_argument(
        "--demo",
        action="store_true",
        help="Run built-in sample error demonstrations.",
    )

    actions.add_argument(
        "--run",
        metavar="SCRIPT_PATH",
        help="Execute a Python script with automatic error reporting.",
    )

    actions.add_argument(
        "--list",
        action="store_true",
        help="List saved bug reports.",
    )

    actions.add_argument(
        "--view",
        metavar="REPORT_FILE",
        help="View a report by filename or path within the reports directory.",
    )

    actions.add_argument(
        "--interactive",
        action="store_true",
        help="Launch the interactive menu.",
    )

    parser.add_argument(
        "--reports-dir",
        default=str(REPORTS_DIR),
        metavar="DIRECTORY",
        help="Directory for generated reports (default: reports).",
    )

    return parser.parse_args(argv)


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main(argv=None):
    """Run the CLI application."""

    args = parse_arguments(argv)
    reports_dir = Path(args.reports_dir).expanduser()

    if args.demo:
        try:
            sample_code.run_all_samples()
            return 0
        except Exception as exc:
            logger.exception("Sample demonstrations failed.")

            report_path, _ = BugReportGenerator(
                reports_dir=reports_dir
            ).generate_report(
                type(exc), exc, exc.__traceback__
            )

            if report_path:
                print(f"[Info] Bug report saved: {report_path}")

            return 1

    if args.run:
        return 0 if run_target_script(
            args.run, reports_dir=reports_dir
        ) else 1

    if args.list:
        list_reports(reports_dir)
        return 0

    if args.view:
        return 0 if view_report(
            args.view, reports_dir=reports_dir
        ) else 1

    # Default behavior: interactive menu.
    interactive_menu()
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
