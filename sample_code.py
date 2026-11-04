
"""
Auto Bug Report Generator - Sample Demonstrations
==================================================

Demonstrates three ways to automatically generate bug reports:

1. ZeroDivisionError  - Using @auto_report decorator
2. FileNotFoundError  - Using MonitorErrors context manager
3. KeyError           - Using global sys.excepthook

All generated reports are stored in the 'reports/' directory.
"""

from pathlib import Path
from bug_reporter import auto_report, MonitorErrors, install_global_hook


# Configuration
REPORTS_DIR = "reports"


# ------------------------------------------------------------------
# Scenario 1: ZeroDivisionError using Decorator
# ------------------------------------------------------------------

@auto_report(reports_dir=REPORTS_DIR, reraise=False)
def calculate_average(total_score, number_of_students):
    """Calculate average marks of students."""

    print("\n[DEMO 1] Calculating student average...")

    average = total_score / number_of_students

    print(f"Average score: {average:.2f}")
    return average


# ------------------------------------------------------------------
# Scenario 2: FileNotFoundError using Context Manager
# ------------------------------------------------------------------

def load_configuration_file(file_name="missing_settings.json"):
    """Load configuration from a file safely."""

    print(f"\n[DEMO 2] Loading configuration: {file_name}")

    with MonitorErrors(
        reports_dir=REPORTS_DIR,
        reraise=False
    ) as monitor:

        with open(file_name, "r", encoding="utf-8") as file:
            content = file.read()
            print("Configuration loaded successfully!")
            print(content)

    if monitor.report_path:
        print(f"Bug report generated: {monitor.report_path}")


# ------------------------------------------------------------------
# Scenario 3: KeyError using Global Exception Hook
# ------------------------------------------------------------------

def parse_user_profile():
    """Extract account information from a user dictionary."""

    print("\n[DEMO 3] Processing user profile...")

    user_data = {
        "username": "alex99",
        "email": "alex@example.com"
    }

    # This key does not exist, causing KeyError.
    account_id = user_data["account_id"]

    return account_id


# ------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------

def run_all_samples():

    print("=" * 65)
    print("       AUTO BUG REPORT GENERATOR - DEMONSTRATION")
    print("=" * 65)

    # Create reports directory if it does not exist.
    Path(REPORTS_DIR).mkdir(parents=True, exist_ok=True)

    # Scenario 1
    print("\nRunning Scenario 1: ZeroDivisionError")

    try:
        calculate_average(
            total_score=500,
            number_of_students=0
        )
    except Exception as error:
        print(f"Unexpected error: {error}")

    # Scenario 2
    print("\nRunning Scenario 2: FileNotFoundError")

    load_configuration_file("non_existent_database.ini")

    # Scenario 3
    print("\nRunning Scenario 3: KeyError")

    with MonitorErrors(
        reports_dir=REPORTS_DIR,
        reraise=False
    ) as monitor:

        parse_user_profile()

    if monitor.report_path:
        print(f"Bug report generated: {monitor.report_path}")

    # Completion message
    print("\n" + "=" * 65)
    print("       ALL DEMONSTRATIONS COMPLETED")
    print("=" * 65)
    print(f"Check the '{REPORTS_DIR}/' directory for bug reports.")


# ------------------------------------------------------------------
# Program Entry Point
# ------------------------------------------------------------------

if __name__ == "__main__":
    run_all_samples()
