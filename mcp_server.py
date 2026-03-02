#!/usr/bin/env python3
"""MCP server for the todo app. Exposes tools to list, add, complete, and delete tasks."""

import json
import urllib.request
from mcp.server.fastmcp import FastMCP

API = "http://localhost:8080/api/tasks"

mcp = FastMCP("todo")


def _request(path="", method="GET", data=None):
    url = f"{API}/{path}" if path else API
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    if body:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


@mcp.tool()
def list_tasks(category: str | None = None) -> str:
    """List all tasks, optionally filtered by category."""
    tasks = _request()
    if category:
        tasks = [t for t in tasks if t.get("category", "").lower() == category.lower()]
    if not tasks:
        return "No tasks found."
    lines = []
    for t in tasks:
        check = "x" if t["done"] else " "
        lines.append(f"[{check}] {t['text']} (id: {t['id']}, category: {t.get('category', 'General')})")
    return "\n".join(lines)


@mcp.tool()
def add_task(text: str, category: str = "General") -> str:
    """Add a new task."""
    task = _request(method="POST", data={"text": text, "category": category})
    return f"Added: {task['text']} (id: {task['id']}, category: {task['category']})"


@mcp.tool()
def complete_task(task_id: str) -> str:
    """Mark a task as done."""
    task = _request(path=task_id, method="PUT", data={"done": True})
    return f"Completed: {task['text']}"


@mcp.tool()
def delete_task(task_id: str) -> str:
    """Delete a task."""
    _request(path=task_id, method="DELETE")
    return f"Deleted task {task_id}"


if __name__ == "__main__":
    mcp.run()
