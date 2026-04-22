#!/usr/bin/env python3
"""General personal AI assistant (offline-first).

Features:
- Task management (add/list/complete)
- Notes and simple keyword search
- Daily briefing (date + pending tasks)
- Intent-style command routing for natural text prompts
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class Task:
    id: int
    text: str
    completed: bool = False
    created_at: str = ""


@dataclass
class Note:
    id: int
    text: str
    created_at: str = ""


class PersonalAssistant:
    """A lightweight personal assistant with local persistence."""

    def __init__(self, db_path: str = "assistant_data.json") -> None:
        self.db_path = Path(db_path)
        self.data = {"tasks": [], "notes": []}
        self._load()

    def _load(self) -> None:
        if self.db_path.exists():
            self.data = json.loads(self.db_path.read_text())

    def _save(self) -> None:
        self.db_path.write_text(json.dumps(self.data, indent=2))

    def _next_id(self, key: str) -> int:
        entries = self.data[key]
        return (max(item["id"] for item in entries) + 1) if entries else 1

    def add_task(self, text: str) -> str:
        text = text.strip()
        if not text:
            return "Please provide a task description."
        task = Task(
            id=self._next_id("tasks"),
            text=text,
            created_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        )
        self.data["tasks"].append(asdict(task))
        self._save()
        return f"Added task #{task.id}: {task.text}"

    def list_tasks(self) -> str:
        if not self.data["tasks"]:
            return "No tasks yet."
        lines = ["Tasks:"]
        for task in self.data["tasks"]:
            mark = "✓" if task["completed"] else "•"
            lines.append(f"{mark} [{task['id']}] {task['text']}")
        return "\n".join(lines)

    def complete_task(self, task_id: int) -> str:
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                if task["completed"]:
                    return f"Task #{task_id} is already completed."
                task["completed"] = True
                self._save()
                return f"Completed task #{task_id}."
        return f"Task #{task_id} not found."

    def add_note(self, text: str) -> str:
        text = text.strip()
        if not text:
            return "Please provide note text."
        note = Note(
            id=self._next_id("notes"),
            text=text,
            created_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        )
        self.data["notes"].append(asdict(note))
        self._save()
        return f"Saved note #{note.id}."

    def list_notes(self) -> str:
        if not self.data["notes"]:
            return "No notes yet."
        return "\n".join(["Notes:"] + [f"[{n['id']}] {n['text']}" for n in self.data["notes"]])

    def search_notes(self, query: str) -> str:
        query = query.strip().lower()
        if not query:
            return "Please provide search text."
        matches = [n for n in self.data["notes"] if query in n["text"].lower()]
        if not matches:
            return f"No notes found for '{query}'."
        return "\n".join([f"[{n['id']}] {n['text']}" for n in matches])

    def daily_briefing(self) -> str:
        now = datetime.utcnow().strftime("%A, %B %d, %Y")
        pending = [t for t in self.data["tasks"] if not t["completed"]]
        lines = [f"Good day! Today is {now}.", f"Pending tasks: {len(pending)}"]
        for task in pending[:5]:
            lines.append(f"- [{task['id']}] {task['text']}")
        if len(pending) > 5:
            lines.append(f"...and {len(pending) - 5} more.")
        return "\n".join(lines)

    def help_text(self) -> str:
        return (
            "Commands:\n"
            "- add task <text>\n"
            "- list tasks\n"
            "- complete task <id>\n"
            "- add note <text>\n"
            "- list notes\n"
            "- search notes <text>\n"
            "- briefing\n"
            "- help\n"
            "- quit"
        )

    def handle(self, user_input: str) -> str:
        text = user_input.strip()
        lower = text.lower()

        if lower in {"help", "?"}:
            return self.help_text()
        if lower in {"briefing", "daily briefing"}:
            return self.daily_briefing()
        if lower in {"list tasks", "show tasks", "what are my tasks"}:
            return self.list_tasks()
        if lower in {"list notes", "show notes"}:
            return self.list_notes()

        if m := re.match(r"(?:add\s+)?task\s+(.+)", text, flags=re.IGNORECASE):
            return self.add_task(m.group(1))
        if m := re.match(r"complete\s+task\s+(\d+)", lower):
            return self.complete_task(int(m.group(1)))
        if m := re.match(r"(?:add\s+)?note\s+(.+)", text, flags=re.IGNORECASE):
            return self.add_note(m.group(1))
        if m := re.match(r"search\s+notes\s+(.+)", text, flags=re.IGNORECASE):
            return self.search_notes(m.group(1))

        # Basic fallback chatbot behavior
        if any(greet in lower for greet in ["hi", "hello", "hey"]):
            return "Hi! I can help with tasks, notes, and your daily briefing. Type 'help' to begin."
        return (
            "I didn't understand that yet. Try 'help' to see supported commands, "
            "or phrase it like 'add task call dentist'."
        )


def run_cli() -> None:
    assistant = PersonalAssistant()
    print("Personal AI Assistant — type 'help' for commands, 'quit' to exit.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"quit", "exit"}:
            print("Assistant: Goodbye!")
            return
        print(f"Assistant: {assistant.handle(user_input)}")


if __name__ == "__main__":
    run_cli()
