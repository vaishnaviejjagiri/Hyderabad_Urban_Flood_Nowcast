import json
import sqlite3
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_ROOT / "notifications.db"

HOST = "127.0.0.1"
PORT = 8000


class FloodDashboardHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            directory=str(PROJECT_ROOT),
            **kwargs
        )

    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/health":
            self.send_json({
                "status": "ok",
                "service": "Hyderabad Urban Flood Nowcast backend",
                "database_exists": DB_FILE.exists(),
                "time": datetime.now().astimezone().isoformat()
            })
            return

        if path == "/api/notifications":
            self.get_notifications()
            return

        # Serve the existing dashboard and its other project files.
        if path == "/":
            self.path = "/index.html"

        super().do_GET()

    def get_notifications(self):
        if not DB_FILE.exists():
            self.send_json({
                "status": "ok",
                "count": 0,
                "notifications": [],
                "message": "Notification database has not been created yet."
            })
            return

        try:
            with sqlite3.connect(DB_FILE) as db:
                db.row_factory = sqlite3.Row

                # Handle a database where the table has not been created.
                table = db.execute("""
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table'
                      AND name = 'notification_log'
                """).fetchone()

                if table is None:
                    self.send_json({
                        "status": "ok",
                        "count": 0,
                        "notifications": [],
                        "message": "No notification records table exists yet."
                    })
                    return

                rows = db.execute("""
                    SELECT
                        area_name,
                        risk_level,
                        message,
                        created_at,
                        status
                    FROM notification_log
                    ORDER BY created_at DESC
                    LIMIT 10
                """).fetchall()

            notifications = [dict(row) for row in rows]

            self.send_json({
                "status": "ok",
                "count": len(notifications),
                "notifications": notifications,
                "message": (
                    "Saved notification records loaded."
                    if notifications
                    else "No saved notifications yet."
                )
            })

        except sqlite3.Error as error:
            self.send_json({
                "status": "error",
                "message": "Database error: " + str(error),
                "notifications": []
            }, 500)


if __name__ == "__main__":
    server = ThreadingHTTPServer(
        (HOST, PORT),
        FloodDashboardHandler
    )

    print("=" * 55)
    print("HYDERABAD URBAN FLOOD NOWCAST BACKEND")
    print("=" * 55)
    print(f"Dashboard:     http://{HOST}:{PORT}/")
    print(f"API health:    http://{HOST}:{PORT}/api/health")
    print(f"Notifications: http://{HOST}:{PORT}/api/notifications")
    print(f"Database:      {DB_FILE}")
    print("Press Ctrl+C to stop the server.")
    print("=" * 55)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
    finally:
        server.server_close()