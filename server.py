#!/usr/bin/env python3
"""Tiny todo-app server. No dependencies beyond the Python stdlib."""

import json
import os
import uuid
from datetime import datetime, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

PORT = 8080
TASKS_FILE = Path(__file__).parent / "tasks.json"


def normalize_category(name):
    return " ".join(w.capitalize() for w in name.strip().split())


def read_tasks():
    if not TASKS_FILE.exists():
        return []
    with open(TASKS_FILE) as f:
        return json.load(f)


def write_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)
        f.write("\n")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/tasks":
            self._json_response(read_tasks())
        elif self.path == "/":
            self.path = "/index.html"
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/tasks":
            body = json.loads(self._read_body())
            tasks = read_tasks()
            task = {
                "id": uuid.uuid4().hex[:8],
                "text": body.get("text", ""),
                "done": False,
                "category": normalize_category(body.get("category", "General")),
                "created": datetime.now(timezone.utc).isoformat(),
            }
            tasks.append(task)
            write_tasks(tasks)
            self._json_response(task, 201)
        else:
            self.send_error(404)

    def do_PUT(self):
        if self.path.startswith("/api/tasks/"):
            task_id = self.path.split("/")[-1]
            body = json.loads(self._read_body())
            tasks = read_tasks()
            for t in tasks:
                if t["id"] == task_id:
                    if "text" in body:
                        t["text"] = body["text"]
                    if "done" in body:
                        t["done"] = body["done"]
                    if "category" in body:
                        t["category"] = normalize_category(body["category"])
                    write_tasks(tasks)
                    self._json_response(t)
                    return
            self.send_error(404, "Task not found")
        else:
            self.send_error(404)

    def do_DELETE(self):
        if self.path.startswith("/api/tasks/"):
            task_id = self.path.split("/")[-1]
            tasks = read_tasks()
            tasks = [t for t in tasks if t["id"] != task_id]
            write_tasks(tasks)
            self._json_response({"ok": True})
        else:
            self.send_error(404)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length).decode()

    def _json_response(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # suppress request logs


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Todo app running at http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
