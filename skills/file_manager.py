"""
Skill: file_manager
Read, write, list, and delete files in a safe workspace directory.
"""

import os
from core.base_skill import BaseSkill

# All file operations are sandboxed to this directory
WORKSPACE = os.path.expanduser("~/.nanoclaw/workspace")


class FileManagerSkill(BaseSkill):
    name = "file_manager"
    description = (
        "Read, write, list, or delete files in your personal workspace. "
        "Useful for saving notes, reading documents, or managing data."
    )
    args_schema = {
        "action": "One of: read, write, list, delete, append",
        "filename": "Name of the file (e.g. 'notes.txt'). Not needed for 'list'.",
        "content": "Content to write (only for 'write' and 'append' actions).",
    }

    def __init__(self):
        os.makedirs(WORKSPACE, exist_ok=True)

    def run(self, action: str, filename: str = "", content: str = "") -> str:
        action = action.lower().strip()

        if action == "list":
            return self._list_files()
        elif action == "read":
            return self._read_file(filename)
        elif action == "write":
            return self._write_file(filename, content)
        elif action == "append":
            return self._append_file(filename, content)
        elif action == "delete":
            return self._delete_file(filename)
        else:
            return f"❌ Unknown action '{action}'. Use: read, write, list, delete, append"

    def _safe_path(self, filename: str) -> str:
        """Prevent path traversal attacks."""
        safe_name = os.path.basename(filename)
        return os.path.join(WORKSPACE, safe_name)

    def _list_files(self) -> str:
        files = os.listdir(WORKSPACE)
        if not files:
            return "📂 Workspace is empty."
        file_list = []
        for f in sorted(files):
            path = os.path.join(WORKSPACE, f)
            size = os.path.getsize(path)
            file_list.append(f"  📄 {f} ({size} bytes)")
        return "📂 Workspace files:\n" + "\n".join(file_list)

    def _read_file(self, filename: str) -> str:
        if not filename:
            return "❌ Please provide a filename."
        path = self._safe_path(filename)
        if not os.path.exists(path):
            return f"❌ File '{filename}' not found."
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            return f"📄 Contents of '{filename}':\n\n{content}"
        except Exception as e:
            return f"❌ Error reading file: {e}"

    def _write_file(self, filename: str, content: str) -> str:
        if not filename:
            return "❌ Please provide a filename."
        path = self._safe_path(filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"✅ File '{filename}' saved successfully ({len(content)} chars)."
        except Exception as e:
            return f"❌ Error writing file: {e}"

    def _append_file(self, filename: str, content: str) -> str:
        if not filename:
            return "❌ Please provide a filename."
        path = self._safe_path(filename)
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(content + "\n")
            return f"✅ Content appended to '{filename}'."
        except Exception as e:
            return f"❌ Error appending to file: {e}"

    def _delete_file(self, filename: str) -> str:
        if not filename:
            return "❌ Please provide a filename."
        path = self._safe_path(filename)
        if not os.path.exists(path):
            return f"❌ File '{filename}' not found."
        try:
            os.remove(path)
            return f"🗑️ File '{filename}' deleted."
        except Exception as e:
            return f"❌ Error deleting file: {e}"