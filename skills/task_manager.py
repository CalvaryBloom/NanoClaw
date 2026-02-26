"""
Skill: task_manager
Create, list, complete, and delete tasks/reminders.
Persists tasks to disk so they survive restarts.
"""

import json
import os
from datetime import datetime
from core.base_skill import BaseSkill

TASKS_FILE = os.path.expanduser("~/.nanoclaw/tasks.json")


class TaskManagerSkill(BaseSkill):
    name = "task_manager"
    description = (
        "Manage a personal to-do list. Add tasks, mark them as done, "
        "list pending tasks, or clear completed ones."
    )
    args_schema = {
        "action": "One of: add, list, done, delete, clear_done",
        "task": "Task description (for 'add') or task ID number (for 'done'/'delete').",
        "due": "Optional due date for the task (e.g. 'tomorrow', '2025-12-01')",
    }

    def run(self, action: str, task: str = "", due: str = "") -> str:
        action = action.lower().strip()

        if action == "add":
            return self._add_task(task, due)
        elif action == "list":
            return self._list_tasks()
        elif action == "done":
            return self._complete_task(task)
        elif action == "delete":
            return self._delete_task(task)
        elif action == "clear_done":
            return self._clear_done()
        else:
            return f"❌ Unknown action '{action}'. Use: add, list, done, delete, clear_done"

    def _load(self) -> list:
        if not os.path.exists(TASKS_FILE):
            return []
        try:
            with open(TASKS_FILE) as f:
                return json.load(f)
        except Exception:
            return []

    def _save(self, tasks: list):
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)

    def _add_task(self, task: str, due: str = "") -> str:
        if not task:
            return "❌ Please provide a task description."
        tasks = self._load()
        new_task = {
            "id": len(tasks) + 1,
            "text": task,
            "done": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "due": due or None,
        }
        tasks.append(new_task)
        self._save(tasks)
        due_str = f" (due: {due})" if due else ""
        return f"✅ Task #{new_task['id']} added: '{task}'{due_str}"

    def _list_tasks(self) -> str:
        tasks = self._load()
        if not tasks:
            return "📋 No tasks yet. Add one with action='add'!"

        pending = [t for t in tasks if not t["done"]]
        done = [t for t in tasks if t["done"]]

        lines = []
        if pending:
            lines.append("📋 **Pending tasks:**")
            for t in pending:
                due_str = f" ⏰ {t['due']}" if t.get("due") else ""
                lines.append(f"  [{t['id']}] {t['text']}{due_str}")

        if done:
            lines.append(f"\n✅ **Completed:** {len(done)} task(s)")

        if not pending and not done:
            return "📋 No tasks found."

        return "\n".join(lines)

    def _complete_task(self, task_id: str) -> str:
        tasks = self._load()
        try:
            tid = int(task_id)
        except ValueError:
            return f"❌ Invalid task ID '{task_id}'. Provide a number."

        for t in tasks:
            if t["id"] == tid:
                if t["done"]:
                    return f"ℹ️ Task #{tid} is already completed."
                t["done"] = True
                t["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self._save(tasks)
                return f"✅ Task #{tid} marked as done: '{t['text']}'"

        return f"❌ Task #{tid} not found."

    def _delete_task(self, task_id: str) -> str:
        tasks = self._load()
        try:
            tid = int(task_id)
        except ValueError:
            return f"❌ Invalid task ID '{task_id}'."

        new_tasks = [t for t in tasks if t["id"] != tid]
        if len(new_tasks) == len(tasks):
            return f"❌ Task #{tid} not found."

        self._save(new_tasks)
        return f"🗑️ Task #{tid} deleted."

    def _clear_done(self) -> str:
        tasks = self._load()
        pending = [t for t in tasks if not t["done"]]
        removed = len(tasks) - len(pending)
        self._save(pending)
        return f"🧹 Cleared {removed} completed task(s). {len(pending)} pending remain."