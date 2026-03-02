# Todo App

A lightweight, local todo list with a clean web UI. Designed to stay open in a small browser window and be updated both manually and programmatically (e.g. by [Claude Code](https://claude.com/claude-code)).

## Features

- Add, check off, edit, and delete tasks
- Organize tasks into collapsible categories
- No dependencies — Python stdlib only
- Data stored in a plain `tasks.json` file
- UI auto-refreshes every 3 seconds to pick up external edits

## Quick Start

```bash
python3 server.py
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

## Claude Code Integration

Claude can read and write tasks directly by editing `tasks.json`:

```json
[
  {
    "id": "abc123",
    "text": "Buy groceries",
    "done": false,
    "category": "Personal",
    "created": "2026-03-01T10:00:00+00:00"
  }
]
```

Changes appear in the UI within a few seconds.
