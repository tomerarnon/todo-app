# Todo App

A lightweight, local todo list with a clean web UI. Designed to stay open in a small browser window and be updated both manually and programmatically (e.g. by [Claude Code](https://claude.com/claude-code)).

## Features

- Add, check off, edit, and delete tasks
- Organize tasks into collapsible categories
- No dependencies for the server — Python stdlib only
- MCP server for Claude Code integration
- Data stored in a plain `tasks.json` file
- UI auto-refreshes every 3 seconds to pick up external edits

## Quick Start

```bash
python3 server.py
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

Optionally, add a shell alias to launch with one command from anywhere:

```bash
# Add to ~/.zshrc or ~/.bashrc
alias todo='cd <path-to-todo-app> && python3 server.py & open http://localhost:8080'
```

Then just run `todo`.

## Claude Code Integration

An MCP server (`mcp_server.py`) exposes the todo app as native Claude Code tools:

- **list_tasks** — list all tasks, optionally filtered by category
- **add_task** — add a new task with optional category
- **complete_task** — mark a task as done
- **delete_task** — delete a task

### Setup

1. Create a venv and install the `mcp` package:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install mcp
   ```

2. Add to `~/.claude/settings.json`:
   ```json
   {
     "mcpServers": {
       "todo": {
         "command": "<path-to-todo-app>/.venv/bin/python3",
         "args": ["<path-to-todo-app>/mcp_server.py"]
       }
     }
   }
   ```

3. Restart Claude Code. The tools will be available automatically.

The MCP server calls the REST API under the hood, so the todo app server must be running.
