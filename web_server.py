"""
Auto Bug Report Generator - Web Dashboard Server
================================================
A zero-dependency local web server built using Python's standard library
(http.server, json, pathlib).

Serves the modern frontend dashboard and exposes a clean REST API:
- GET  /api/reports           -> Lists all parsed reports from the 'reports/' folder.
- GET  /api/reports/<name>    -> Fetches raw content of a specific report.
- POST /api/simulate          -> Triggers live Python bug scenarios and generates reports.
- POST /api/generate          -> Accepts custom error details and writes a new report file.
"""

import sys
import os
import json
import mimetypes
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import urllib.parse

from bug_reporter import BugReportGenerator
import sample_code

DEFAULT_PORT = 8080
DEFAULT_HOST = "127.0.0.1"
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
REPORTS_DIR = BASE_DIR / "reports"


def parse_report_file(file_path: Path) -> dict:
    """Parse a .txt bug report file into structured dictionary metadata."""
    data = {
        "filename": file_path.name,
        "error_type": "UnknownError",
        "error_message": "",
        "date_time": "",
        "file_name": "",
        "line_number": "",
        "function_name": "",
        "code_line": "",
        "traceback": "",
        "python_version": "",
        "os_platform": "",
        "raw_text": ""
    }

    try:
        content = file_path.read_text(encoding="utf-8")
        data["raw_text"] = content
        lines = content.splitlines()

        in_traceback = False
        traceback_lines = []
        in_system = False

        for line in lines:
            line_stripped = line.strip()

            if "SHORT TRACEBACK:" in line:
                in_traceback = True
                in_system = False
                continue
            elif "SYSTEM CONTEXT:" in line:
                in_traceback = False
                in_system = True
                continue
            elif "END OF REPORT" in line or line_stripped.startswith("==="):
                if in_traceback and not line_stripped.startswith("==="):
                    traceback_lines.append(line)
                continue

            if in_traceback:
                traceback_lines.append(line)
                continue

            if in_system:
                if line.startswith("Python Version"):
                    data["python_version"] = line.split(":", 1)[-1].strip()
                elif line.startswith("Operating System"):
                    data["os_platform"] = line.split(":", 1)[-1].strip()
                continue

            # Standard fields
            if line.startswith("1. Date & Time"):
                data["date_time"] = line.split(":", 1)[-1].strip()
            elif line.startswith("2. Error Type"):
                data["error_type"] = line.split(":", 1)[-1].strip()
            elif line.startswith("3. Error Message"):
                data["error_message"] = line.split(":", 1)[-1].strip()
            elif line.startswith("4. File Name"):
                data["file_name"] = line.split(":", 1)[-1].strip()
            elif line.startswith("5. Line Number"):
                data["line_number"] = line.split(":", 1)[-1].strip()
            elif line.startswith("6. Function / Scope"):
                data["function_name"] = line.split(":", 1)[-1].strip()
            elif line.startswith("7. Failing Code Line"):
                data["code_line"] = line.split(":", 1)[-1].strip()

        data["traceback"] = "\n".join(traceback_lines).strip()
    except Exception as err:
        data["error_message"] = f"Failed to read report: {err}"

    return data


class AutoBugRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler serving frontend assets and REST API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # REST API: List all reports
        if path == "/api/reports":
            self.handle_get_reports()
            return

        # REST API: Get specific report file
        if path.startswith("/api/reports/"):
            filename = urllib.parse.unquote(path.replace("/api/reports/", ""))
            self.handle_get_single_report(filename)
            return

        # Serve Frontend Static Assets
        if path == "/" or path == "":
            self.path = "/index.html"

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/simulate":
            self.handle_simulate()
            return

        if path == "/api/generate":
            self.handle_generate()
            return

        self.send_error(404, "Endpoint not found")

    def handle_get_reports(self):
        """Retrieve and return all bug report summaries as JSON."""
        reports = []
        if REPORTS_DIR.exists():
            files = sorted(REPORTS_DIR.glob("*.txt"), key=lambda f: f.stat().st_mtime, reverse=True)
            for file in files:
                reports.append(parse_report_file(file))

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(reports).encode("utf-8"))

    def handle_get_single_report(self, filename: str):
        """Return the raw text of a specific report."""
        target_file = REPORTS_DIR / filename
        if not target_file.exists() or not target_file.is_file():
            self.send_error(404, "Report file not found")
            return

        try:
            content = target_file.read_text(encoding="utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except OSError:
            self.send_error(500, "Could not read report file")

    def handle_simulate(self):
        """Run simulated exception scenario and return newly created report."""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode("utf-8") or "{}")
        scenario = payload.get("scenario", "zero_division")

        generator = BugReportGenerator(reports_dir=str(REPORTS_DIR))
        created_file_path = None

        if scenario == "zero_division":
            try:
                sample_code.calculate_average(100, 0)
            except Exception as exc:
                created_file_path, _ = generator.generate_report(type(exc), exc, exc.__traceback__)
        elif scenario == "missing_file":
            try:
                sample_code.load_configuration_file("missing_config_test.ini")
            except Exception as exc:
                created_file_path, _ = generator.generate_report(type(exc), exc, exc.__traceback__)
        else: # missing_key
            try:
                sample_code.parse_user_profile()
            except Exception as exc:
                created_file_path, _ = generator.generate_report(type(exc), exc, exc.__traceback__)

        if not created_file_path:
            # Check latest file created in reports
            files = sorted(REPORTS_DIR.glob("*.txt"), key=lambda f: f.stat().st_mtime, reverse=True)
            if files:
                created_file_path = files[0]

        if created_file_path:
            parsed = parse_report_file(Path(created_file_path))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(parsed).encode("utf-8"))
        else:
            self.send_error(500, "Failed to simulate exception")

    def handle_generate(self):
        """Accept user-defined error report payload and write to disk."""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode("utf-8") or "{}")

        filename = payload.get("filename")
        raw_text = payload.get("raw_text")

        if not filename or not raw_text:
            self.send_error(400, "Missing filename or raw_text")
            return

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        safe_path = REPORTS_DIR / Path(filename).name
        try:
            safe_path.write_text(raw_text, encoding="utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "saved", "path": str(safe_path)}).encode("utf-8"))
        except OSError as e:
            self.send_error(500, f"Failed to write file: {e}")


def run_web_server(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Start the HTTP server on specified host and port."""
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, AutoBugRequestHandler)

    print("\n" + "=" * 65)
    print(" AUTO BUG REPORT GENERATOR - WEB DASHBOARD")
    print("=" * 65)
    print(f" Web Studio running at: http://{host}:{port}/")
    print(f" Serving frontend from: {FRONTEND_DIR}")
    print(f" Reading reports from : {REPORTS_DIR}")
    print(" Press Ctrl+C to stop the web server.")
    print("=" * 65 + "\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Web Server] Shutting down...")
        httpd.server_close()


if __name__ == "__main__":
    port = DEFAULT_PORT
    host = DEFAULT_HOST
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_web_server(host=host, port=port)
