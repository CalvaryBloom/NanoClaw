"""
NanoClaw - Core Agent Loop
Inspired by PicoClaw, built with extensibility in mind.
"""

import json
import os
from typing import Any

from core.llm import LLMClient
from core.skill_loader import SkillLoader


class Agent:
    def __init__(self, config: dict):
        self.config = config
        self.llm = LLMClient(config)
        self.skill_loader = SkillLoader()
        self.skills = self.skill_loader.load_all()
        self.history = []

        print(f"✅ Agent ready with {len(self.skills)} skills loaded.")

    def chat(self, user_message: str) -> str:
        """Main agent loop: receive message → pick tool → execute → respond."""
        self.history.append({"role": "user", "content": user_message})

        # Build system prompt with available tools
        system_prompt = self._build_system_prompt()

        # Ask the LLM what to do
        response = self.llm.complete(
            system=system_prompt,
            messages=self.history,
        )

        # Check if LLM wants to use a tool
        if "<tool>" in response:
            response = self._handle_tool_call(response)

        self.history.append({"role": "assistant", "content": response})
        return response

    def _handle_tool_call(self, response: str) -> str:
        """Parse and execute a tool call from the LLM response."""
        try:
            start = response.index("<tool>") + 6
            end = response.index("</tool>")
            tool_data = json.loads(response[start:end].strip())

            tool_name = tool_data.get("name")
            tool_args = tool_data.get("args", {})

            if tool_name not in self.skills:
                return f"❌ Tool '{tool_name}' not found."

            print(f"🔧 Using tool: {tool_name} with args: {tool_args}")
            result = self.skills[tool_name].run(**tool_args)

            # Give result back to LLM for a final natural language answer
            self.history.append({
                "role": "assistant",
                "content": response
            })
            self.history.append({
                "role": "user",
                "content": f"[Tool result for '{tool_name}']: {result}\n\nNow give the user a helpful, natural response based on this result."
            })

            final_response = self.llm.complete(
                system=self._build_system_prompt(),
                messages=self.history,
            )

            # Clean up internal tool messages from history
            self.history.pop()
            self.history.pop()

            return final_response

        except (ValueError, json.JSONDecodeError) as e:
            return f"⚠️ Error parsing tool call: {e}\n\n{response}"

    def _build_system_prompt(self) -> str:
        """Build the system prompt including all available tools."""
        tools_description = "\n".join(
            f"- **{name}**: {skill.description}\n  Args: {skill.args_schema}"
            for name, skill in self.skills.items()
        )

        return f"""You are a helpful, efficient AI assistant.

You have access to the following tools:
{tools_description}

To use a tool, respond with this exact format:
<tool>{{"name": "tool_name", "args": {{"arg1": "value1"}}}}</tool>

Only use a tool if it genuinely helps answer the user's request.
If you don't need a tool, just respond normally in plain text.
Be concise and helpful.
"""

    def reset_history(self):
        """Clear conversation history."""
        self.history = []
        print("🗑️ Conversation history cleared.")