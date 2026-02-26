"""
Skill: system_info
Get information about the system: time, date, OS, disk usage, memory, etc.
"""

import os
import platform
import datetime
from core.base_skill import BaseSkill


class SystemInfoSkill(BaseSkill):
    name = "system_info"
    description = (
        "Get system information: current date/time, OS details, "
        "disk usage, memory usage, CPU info, and environment info."
    )
    args_schema = {
        "query": "What to check: 'datetime', 'os', 'disk', 'memory', 'all'",
    }

    def run(self, query: str = "all") -> str:
        query = query.lower().strip()

        if query in ("datetime", "date", "time"):
            return self._get_datetime()
        elif query in ("os", "system", "platform"):
            return self._get_os_info()
        elif query == "disk":
            return self._get_disk_info()
        elif query == "memory":
            return self._get_memory_info()
        else:
            # Return everything
            parts = [
                self._get_datetime(),
                self._get_os_info(),
                self._get_disk_info(),
            ]
            return "\n\n".join(parts)

    def _get_datetime(self) -> str:
        now = datetime.datetime.now()
        utc_now = datetime.datetime.utcnow()
        return (
            f"🕐 **Date & Time**\n"
            f"  Local: {now.strftime('%A, %B %d %Y at %H:%M:%S')}\n"
            f"  UTC:   {utc_now.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"  Week:  #{now.isocalendar()[1]} of {now.year}"
        )

    def _get_os_info(self) -> str:
        uname = platform.uname()
        return (
            f"💻 **System Info**\n"
            f"  OS:       {uname.system} {uname.release}\n"
            f"  Machine:  {uname.machine}\n"
            f"  Python:   {platform.python_version()}\n"
            f"  Hostname: {uname.node}"
        )

    def _get_disk_info(self) -> str:
        try:
            stat = os.statvfs(os.path.expanduser("~"))
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bavail * stat.f_frsize
            used = total - free
            pct = (used / total * 100) if total > 0 else 0

            def human(n):
                for unit in ["B", "KB", "MB", "GB", "TB"]:
                    if n < 1024:
                        return f"{n:.1f} {unit}"
                    n /= 1024
                return f"{n:.1f} PB"

            return (
                f"💾 **Disk Usage (home)**\n"
                f"  Total: {human(total)}\n"
                f"  Used:  {human(used)} ({pct:.1f}%)\n"
                f"  Free:  {human(free)}"
            )
        except Exception as e:
            return f"💾 Disk info unavailable: {e}"

    def _get_memory_info(self) -> str:
        try:
            with open("/proc/meminfo") as f:
                lines = f.readlines()
            mem = {}
            for line in lines[:5]:
                key, val = line.split(":")
                mem[key.strip()] = val.strip()

            return (
                f"🧠 **Memory**\n"
                + "\n".join(f"  {k}: {v}" for k, v in mem.items())
            )
        except Exception:
            return "🧠 Memory info: only available on Linux."