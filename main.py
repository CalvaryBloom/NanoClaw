#!/usr/bin/env python3
"""
NanoClaw - Ultra-extensible AI Assistant
Usage:
    python main.py                  # Interactive chat
    python main.py -m "your msg"    # Single message
    python main.py --list-skills    # Show loaded skills
    python main.py --reset          # Clear conversation history
"""

import argparse
import json
import os
import sys


CONFIG_PATH = os.path.expanduser("~/.nanoclaw/config.json")
DEFAULT_CONFIG_PATH = "config.example.json"


def load_config() -> dict:
    """Load configuration from ~/.nanoclaw/config.json"""
    if not os.path.exists(CONFIG_PATH):
        print(f"⚙️  Config not found at {CONFIG_PATH}")
        print("   Run: python main.py --init   to create it.")
        print(f"   Or copy config.example.json to {CONFIG_PATH} and add your API keys.\n")

        # Try local config.json as fallback
        if os.path.exists("config.json"):
            with open("config.json") as f:
                return json.load(f)

        sys.exit(1)

    with open(CONFIG_PATH) as f:
        return json.load(f)


def init_config():
    """Create default config file."""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    if os.path.exists(CONFIG_PATH):
        print(f"✅ Config already exists at {CONFIG_PATH}")
        return

    example = {
        "agent": {
            "model": "openai/gpt-4o-mini",
            "max_tokens": 4096,
            "temperature": 0.7
        },
        "providers": {
            "openrouter": {
                "api_key": "YOUR_OPENROUTER_KEY_HERE",
                "api_base": "https://openrouter.ai/api/v1"
            }
        },
        "tools": {
            "web_search": {
                "api_key": "YOUR_BRAVE_SEARCH_KEY_HERE"
            }
        }
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(example, f, indent=2)

    print(f"✅ Config created at {CONFIG_PATH}")
    print("   Edit it and add your API keys to get started.")
    print()
    print("   Get free API keys:")
    print("   🔑 LLM:    https://openrouter.ai/keys  (200K tokens/month free)")
    print("   🔍 Search: https://brave.com/search/api  (2000 queries/month free)")


def main():
    parser = argparse.ArgumentParser(
        description="NanoClaw - Ultra-extensible AI Assistant"
    )
    parser.add_argument("-m", "--message", help="Send a single message and exit")
    parser.add_argument("--list-skills", action="store_true", help="List all loaded skills")
    parser.add_argument("--init", action="store_true", help="Initialize config file")
    args = parser.parse_args()

    if args.init:
        init_config()
        return

    config = load_config()

    # Import here so errors show after config check
    from core.agent import Agent

    agent = Agent(config)

    if args.list_skills:
        print("\n📦 Loaded skills:")
        for name, skill in agent.skills.items():
            print(f"\n  🔧 {name}")
            print(f"     {skill.description}")
            if skill.args_schema:
                for arg, desc in skill.args_schema.items():
                    print(f"     • {arg}: {desc}")
        return

    if args.message:
        response = agent.chat(args.message)
        print(f"\n{response}")
        return

    # Interactive mode
    print("\n🤖 NanoClaw ready! Type your message (Ctrl+C or 'exit' to quit, 'reset' to clear history)\n")
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "bye"):
                print("👋 Goodbye!")
                break
            if user_input.lower() == "reset":
                agent.reset_history()
                continue

            response = agent.chat(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
