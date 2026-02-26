"""
LLM Client - Abstraction layer for multiple AI providers.
Supports: OpenRouter, Anthropic, OpenAI, Gemini, Groq
"""

import os
import requests
from typing import Optional


class LLMClient:
    def __init__(self, config: dict):
        self.config = config
        self.provider, self.provider_config = self._resolve_provider()
        self.model = config.get("agent", {}).get("model", self._default_model())
        self.max_tokens = config.get("agent", {}).get("max_tokens", 4096)
        self.temperature = config.get("agent", {}).get("temperature", 0.7)

        print(f"🤖 LLM: {self.provider} / {self.model}")

    def _resolve_provider(self) -> tuple[str, dict]:
        """Find which provider is configured."""
        providers = self.config.get("providers", {})
        priority = ["openrouter", "anthropic", "openai", "gemini", "groq"]

        for name in priority:
            if name in providers and providers[name].get("api_key"):
                return name, providers[name]

        raise ValueError(
            "❌ No LLM provider configured. Add at least one API key to config.json.\n"
            "   Recommended: OpenRouter (free tier available) → https://openrouter.ai"
        )

    def _default_model(self) -> str:
        defaults = {
            "openrouter": "openai/gpt-4o-mini",
            "anthropic": "claude-haiku-4-5-20251001",
            "openai": "gpt-4o-mini",
            "gemini": "gemini-1.5-flash",
            "groq": "llama-3.1-8b-instant",
        }
        return defaults.get(self.provider, "openai/gpt-4o-mini")

    def complete(self, system: str, messages: list) -> str:
        """Send messages to the LLM and get a response."""
        if self.provider == "anthropic":
            return self._call_anthropic(system, messages)
        else:
            return self._call_openai_compatible(system, messages)

    def _call_openai_compatible(self, system: str, messages: list) -> str:
        """Works for OpenRouter, OpenAI, Groq, Gemini (OpenAI-compatible)."""
        base_urls = {
            "openrouter": "https://openrouter.ai/api/v1",
            "openai": "https://api.openai.com/v1",
            "groq": "https://api.groq.com/openai/v1",
            "gemini": "https://generativelanguage.googleapis.com/v1beta/openai",
        }

        api_base = self.provider_config.get(
            "api_base", base_urls.get(self.provider, "https://openrouter.ai/api/v1")
        )
        api_key = self.provider_config["api_key"]

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [{"role": "system", "content": system}] + messages,
        }

        resp = requests.post(
            f"{api_base}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        if not resp.ok:
            print(f"❌ Error {resp.status_code}: {resp.text}")
            resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def _call_anthropic(self, system: str, messages: list) -> str:
        """Native Anthropic API call."""
        api_key = self.provider_config["api_key"]

        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "max_tokens": self.max_tokens,
                "system": system,
                "messages": messages,
            },
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]