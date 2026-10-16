"""
Auto Bug Report Generator - Sample Demonstrations
=================================================
This file demonstrates various ways to use the Auto Bug Report Generator
in real-world Python code.

It includes 3 common bug scenarios:
1. ZeroDivisionError   - Demonstrated using the @auto_report decorator
2. FileNotFoundError   - Demonstrated using the MonitorErrors context manager
3. KeyError            - Demonstrated using the global sys.excepthook
"""

from bug_reporter import auto_report, MonitorErrors, install_global_hook


# ----------------------------------------------------------------------
# Scenario 1: ZeroDivisionError with @auto_report Decorator
# ----------------------------------------------------------------------
@auto_report(reports_dir="reports", reraise=False)
def calculate_average(total_score, number_of_students):
    """
    Computes an average score.
    Fails with ZeroDivisionError when number_of_students is 0.
    The @auto_report decorator intercepts the error and logs a report.
    """
    print(f"\n[Demo 1] Calculating average for {number_of_students} students...")
    average = total_score / number_of_students
    print(f"Average: {average}")
    return average


# ----------------------------------------------------------------------
# Scenario 2: FileNotFoundError with MonitorErrors Context Manager
# ----------------------------------------------------------------------
def load_configuration_file(file_name="missing_settings.json"):
    """
    Attempts to read a configuration file.
    Uses 'with MonitorErrors' so the program generates a report
    and keeps running without crashing.
    """
    print(f"\n[Demo 2] Attempting to read config file '{file_name}'...")
    with MonitorErrors(reports_dir="reports", reraise=False) as monitor:
        with open(file_name, "r") as f:
            content = f.read()
            print(f"Config loaded: {content}")

    if monitor.report_path:
        print(f"-> Handled FileNotFoundError safely! Saved report: {monitor.report_path}")


# ----------------------------------------------------------------------
# Scenario 3: KeyError with Global Exception Hook
# ----------------------------------------------------------------------
def parse_user_profile():
    """
    Processes a dictionary that lacks a mandatory key.
    """
    print("\n[Demo 3] Parsing user profile dictionary...")
    user_data = {
        "username": "alex99",
        "email": "alex@example.com"
    }
    # Attempting to access non-existent key 'account_id'
    account_id = user_data["account_id"]
    return account_id


def run_all_samples():
    """Run all demonstration scenarios sequentially."""
    print("=" * 65)
    print(" Running Auto Bug Report Generator Demos")
    print("=" * 65)

    # 1. Run decorator demo (safe, reraise=False)
    calculate_average(total_score=500, number_of_students=0)

    # 2. Run context manager demo (safe, reraise=False)
    load_configuration_file("non_existent_database.ini")

    # 3. Direct demo with context manager for KeyError
    print("\n[Demo 3] Handling unexpected KeyError safely...")
    with MonitorErrors(reports_dir="reports", reraise=False) as monitor:
        parse_user_profile()
    if monitor.report_path:
        print(f"-> Handled KeyError safely! Saved report: {monitor.report_path}")

    print("\n" + "=" * 65)
    print(" Demos completed! Check the 'reports/' folder for generated .txt reports.")
    print("=" * 65)


if __name__ == "__main__":
    run_all_samples()
