"""
BaseSkill - Every skill must inherit from this class.

To create a new skill:
1. Create a new file in /skills/
2. Create a class that inherits from BaseSkill
3. Fill in name, description, args_schema
4. Implement the run() method
5. That's it! The agent will discover it automatically.

Example:
    class MySkill(BaseSkill):
        name = "my_skill"
        description = "Does something useful"
        args_schema = {"query": "The search query"}

        def run(self, query: str) -> str:
            return f"Result for: {query}"
"""

from abc import ABC, abstractmethod


class BaseSkill(ABC):
    # Required: short unique identifier (snake_case)
    name: str = ""

    # Required: what this skill does (shown to the LLM)
    description: str = ""

    # Required: dict of {arg_name: description} the skill accepts
    args_schema: dict = {}

    @abstractmethod
    def run(self, **kwargs) -> str:
        """
        Execute the skill and return a string result.
        The result will be passed back to the LLM for interpretation.
        """
        pass

    def __repr__(self):
        return f"<Skill: {self.name}>"