"""
Skill Loader - Auto-discovers and loads all skills from the /skills directory.
Adding a new skill is as simple as dropping a .py file in /skills.
"""

import importlib
import inspect
import os
from core.base_skill import BaseSkill


class SkillLoader:
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = skills_dir

    def load_all(self) -> dict[str, BaseSkill]:
        """Scan the skills directory and load every valid skill."""
        skills = {}
        skills_path = os.path.abspath(self.skills_dir)

        if not os.path.exists(skills_path):
            print(f"⚠️  Skills directory '{skills_path}' not found.")
            return skills

        for filename in sorted(os.listdir(skills_path)):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue

            module_name = f"skills.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)

                # Find all BaseSkill subclasses in the module
                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if (
                        issubclass(obj, BaseSkill)
                        and obj is not BaseSkill
                        and not inspect.isabstract(obj)
                    ):
                        instance = obj()
                        skills[instance.name] = instance
                        print(f"  📦 Loaded skill: {instance.name}")

            except Exception as e:
                print(f"  ❌ Failed to load skill '{filename}': {e}")

        return skills