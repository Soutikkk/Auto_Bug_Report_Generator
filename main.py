"""
Auto Bug Report Generator - Command Line Interface (CLI)
========================================================
This module serves as the user-facing entry point. It allows running:
- Sample bug demonstrations.
- Any arbitrary Python script with auto-reporting enabled.
- Listing and viewing generated .txt bug reports.

Both interactive menu mode and direct command-line arguments are supported.
"""

import os
import sys
import argparse
import runpy
from pathlib import Path
from bug_reporter import BugReportGenerator, install_global_hook, logger
import sample_code


REPORTS_DIR = "reports"


def list_reports(reports_dir=REPORTS_DIR):
    """List all generated bug report files in the reports folder."""
    path = Path(reports_dir)
    if not path.exists():
        print(f"\n[Info] Reports directory '{reports_dir}' does not exist yet.")
        return []

    report_files = sorted(path.glob("*.txt"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not report_files:
        print(f"\n[Info] No bug reports found in '{reports_dir}'.")
        return []

    print("\n" + "=" * 65)
    print(f" Saved Bug Reports in '{reports_dir}':")
    print("=" * 65)
    for index, file in enumerate(report_files, start=1):
        file_size = file.stat().st_size
        print(f" {index}. {file.name} ({file_size} bytes)")
    print("=" * 65)
    return report_files


def view_report(file_path):
    """Display the contents of a specific report file."""
    path = Path(file_path)
    if not path.exists():
        print(f"\n[Error] Report file '{file_path}' was not found.")
        return

    print("\n" + "~" * 78)
    print(f" DISPLAYING REPORT: {path.name}")
    print("~" * 78)
    try:
        with open(path, "r", encoding="utf-8") as f:
            print(f.read())
    except OSError as e:
        print(f"[Error] Could not read file '{path}': {e}")
    print("~" * 78)


def run_target_script(script_path, reports_dir=REPORTS_DIR):
    """
    Execute a target Python script with the Auto Bug Reporter active.
    If the target script encounters any unhandled exception,
    a bug report is automatically generated and saved.
    """
    path = Path(script_path)
    if not path.is_file():
        print(f"[Error] Script '{script_path}' does not exist or is not a valid file.")
        return

    print(f"\n[Runner] Executing '{path.name}' with Auto Bug Reporter active...")
    print("-" * 65)

    # Attach global exception hook for unhandled exceptions in the script
    install_global_hook(reports_dir=reports_dir)

    # Execute target script in its own namespace
    try:
        runpy.run_path(str(path), run_name="__main__")
        print("-" * 65)
        print(f"[Runner] '{path.name}' finished successfully without unhandled errors.")
    except Exception as exc:
        print("-" * 65)
        generator = BugReportGenerator(reports_dir=reports_dir)
        report_path, _ = generator.generate_report(type(exc), exc, exc.__traceback__)
        print(f"[Runner] Script raised an uncaught exception: {type(exc).__name__}: {exc}")
        if report_path:
            print(f"[Runner] Bug report generated and saved to: {report_path}")


def interactive_menu():
    """Run a beginner-friendly interactive console menu."""
    while True:
        print("\n" + "=" * 50)
        print("    AUTO BUG REPORT GENERATOR - MAIN MENU")
        print("=" * 50)
        print(" 1. Run sample bug demonstrations")
        print(" 2. Run a Python script with bug monitoring")
        print(" 3. List all saved bug reports")
        print(" 4. View a bug report")
        print(" 5. Exit")
        print("=" * 50)

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            sample_code.run_all_samples()
        elif choice == "2":
            target = input("Enter the path to the Python script to run: ").strip().strip('"').strip("'")
            if target:
                run_target_script(target)
            else:
                print("[Warning] No file path entered.")
        elif choice == "3":
            list_reports()
        elif choice == "4":
            reports = list_reports()
            if reports:
                sub_choice = input(f"Enter report number (1-{len(reports)}) or filename: ").strip()
                if sub_choice.isdigit() and 1 <= int(sub_choice) <= len(reports):
                    view_report(reports[int(sub_choice) - 1])
                elif sub_choice:
                    view_report(sub_choice)
        elif choice == "5":
            print("\nExiting Auto Bug Report Generator. Goodbye!\n")
            break
        else:
            print("[Invalid Choice] Please select a number between 1 and 5.")


def parse_arguments():
    """Parse command-line arguments using Python's standard argparse."""
    parser = argparse.ArgumentParser(
        description="Auto Bug Report Generator: Automatically detect Python errors and generate detailed .txt bug reports."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run built-in sample error demonstrations (ZeroDivisionError, FileNotFoundError, KeyError)."
    )
    parser.add_argument(
        "--run",
        metavar="SCRIPT_PATH",
        type=str,
        help="Run a Python script with automatic bug report interception."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all saved bug reports."
    )
    parser.add_argument(
        "--view",
        metavar="REPORT_FILE",
        type=str,
        help="Display the contents of a specific bug report .txt file."
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start the interactive menu (default if no flags are provided)."
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    # If flags were supplied, execute corresponding actions
    if args.demo:
        sample_code.run_all_samples()
    elif args.run:
        run_target_script(args.run)
    elif args.list:
        list_reports()
    elif args.view:
        view_report(args.view)
    elif args.interactive or len(sys.argv) == 1:
        interactive_menu()


if __name__ == "__main__":
    main()
